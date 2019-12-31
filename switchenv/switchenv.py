#! /usr/bin/env python


import os
import sys
import json
import click
import shutil
from typing import Optional
import fuzzypicker
import textwrap


class cached_property(object):
    """
    This is a direct copy-paste of Django's cached property from
    https://github.com/django/django/blob/2456ffa42c33d63b54579eae0f5b9cf2a8cd3714/django/utils/functional.py#L38-50
    """
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, type=None):
        if instance is None:
            return self
        res = instance.__dict__[self.func.__name__] = self.func(instance)
        return res


class SwitchEnv:
    # Define the file locations for persisting environments
    BLOB_DIR = os.path.realpath(os.path.expanduser('~/.switchenv'))
    BLOB_FILE = os.path.join(BLOB_DIR, 'profiles.json')
    TEMP_FILE = os.path.join(BLOB_DIR, '__temp_profiles__.json')
    BASH_RC_FILE = os.path.realpath(os.path.expanduser('~/.bashrc'))
    TEMP_RC_FILE = os.path.join(BLOB_DIR, 'switchenvrc.sh')

    def __init__(self):
        # Ensure directory structure every time class is instantiate4d
        os.makedirs(self.BLOB_DIR, exist_ok=True)

    def make_temp_rc_file(self, profile, code):

        input_code_lines = code.split('\n')
        # Save off the PS1 variable before anything can change it
        pre_code_lines = ['export __PSSWE__="$PS1"']

        # Add the profile name to the front of PS1
        post_code_lines = [f'PS1="•{profile}•$__PSSWE__"']

        # Create lines that will store the current env
        env_lines = []
        for key, val in self.env.items():
            env_lines.append(f'export {key}="{val}"')
        env_code = '\n'.join(env_lines)

        # Build code from the stored profile
        code_lines = pre_code_lines + input_code_lines + post_code_lines
        code = '\n'.join(code_lines)

        # Load in the user's bashrc file
        bashrc = ''
        if os.path.isfile(self.BASH_RC_FILE):
            with open(self.BASH_RC_FILE) as bashrc_file:
                bashrc = bashrc_file.read()

        # The order here is important.  The users .bashrc can reset
        # the path variable overriding any currently set envs vars.
        # So:
        #    1) Run their .bashrc
        #    2) export all current environment variables
        #    3) source the custom profile code
        bashrc = textwrap.dedent(f'{bashrc}\n{env_code}\n{code}')
        bashrc = '\n'.join([f' {line}' for line in bashrc.split('\n') if line])
        with open(self.TEMP_RC_FILE, 'w') as temp_rc_file:
            temp_rc_file.write(bashrc)

    @cached_property
    def blob(self):
        """
        Returns the currently saved blob.  Empty dict if nothing saved.
        """
        return self._load_file(self.BLOB_FILE)

    @cached_property
    def keys(self):
        """
        Returns list of profile names
        """
        return sorted(self.blob.keys())

    def get_key(self):
        key = fuzzypicker.picker(self.keys)
        if key is None:
            sys.exit(0)
        return key

    def _reset(self):
        """
        Bust the cache for all cached properties
        """
        for attr in ['keys', 'blob']:
            try:
                delattr(self, attr)
            except AttributeError:
                pass

    def _load_file(self, file_name):
        """
        Load a json file with provided name.
        Returns blank dict if file doesn't exist
        """

        if os.path.isfile(file_name):
            with open(file_name, 'r') as data_file:
                blob = json.load(data_file)
        else:
            blob = {}
        return blob

    def _save_file(self, blob, file_name):
        """
        Saves a json blob to specified file_name
        """
        with open(file_name, 'w') as out_file:
            json.dump(blob, out_file)

    def _confirm_file_contents(self, blob, file_name):
        """
        Compares the contents of a blob with those
        of a saved file
        """
        saved_blob = self._load_file(file_name)
        return blob == saved_blob

    def save(self, blob):
        """
        Atomically save a blob to the canonical file_name
        """
        # Bust the cached property caches
        self._reset()

        # Save the blob to a temp file
        self._save_file(blob, self.TEMP_FILE)

        # If temp file contents match blob, overwrite standard blob
        # file with temp file
        if self._confirm_file_contents(blob, self.TEMP_FILE):
            shutil.move(self.TEMP_FILE, self.BLOB_FILE)

    def update(self, update_blob):
        """
        Add or update blob contents
        """
        blob = self.blob
        blob.update(update_blob)
        self.save(blob)

    def delete(self, keys):
        """
        Remove profiles from the blob
        """
        blob = self.blob
        for key in keys:
            blob.pop(key, None)
        self.save(blob)

    def show(self, key_list=None, template=None):
        """
        Show a single profile.  template is a .format()
        template that will have access to the profile
        name using the 'key' variable.  Defaults to
        f'
        """
        if not key_list:
            key = self.get_key()
            key_list = [key]

        for key in key_list:
            self._show_single(key)

    def _show_single(self, key):
        if key not in self.keys:
            return

        print('\n')
        print(f"#{'=' * 40}")
        print(f'# {key}')
        print(f"#{'=' * 40}")
        print(self.blob[key])

    @property
    def env(self):
        env = dict(os.environ)

        # OSX does a weird thing by setting this variable
        # It ends up screwing up execvpe, so zap it out of
        # the environment
        # See: https://stackoverflow.com/questions/26323852/whats-the-meaning-of-pyvenv-launcher-environment-variable
        env.pop('__PYVENV_LAUNCHER__', None)
        env.pop('_', None)
        return env


def ensure_profiles_exist(swenv):
    if len(swenv.keys) == 0:
        print('\nNo saved profiles\n')
        sys.exit(1)


def run_switch_env(profile: Optional[str] = None):
    swenv = SwitchEnv()
    ensure_profiles_exist(swenv)

    if profile is None:
        profile = swenv.get_key()

    code = swenv.blob[profile]
    swenv.make_temp_rc_file(profile, code)

    commands = ['bash', '--init-file', swenv.TEMP_RC_FILE]

    os.execvpe('bash', commands, swenv.env)


@click.group()
def cli():
    pass


@cli.command(help='Show usage examples')
def examples():
    text = textwrap.dedent("""

    # Snapshot the current environment as a profile
    switchenv snapshot -p my_snapshot_profile_name

    # Add an existing shell script as a profile
    switchenv add -p my_profile_name -f path/to/my_scrpt.sh

    # Show all profile names
    switchenv list

    # Show contents of a specific profile
    switchenv show                                # allows for fuzzysearch of profile name
    switchenv show -p profile1 [-p profile2... ]  # show a specific profile(s)

    # Drop into a subshell with a specific profile
    switchenv  # Will present you with a fuzzy searchable list of profiles

    # Delete profiles
    switchenv delete -p profile_name_1 [-p profile_name_2, ...]


    """)
    print(text)


@cli.command(help='List all profile names')
def list():
    swenv = SwitchEnv()
    ensure_profiles_exist(swenv)
    for key in swenv.keys:
        print(key)


@cli.command(help='Show contents of a single profile')
@click.option('-p', '--profiles', multiple=True)
def show(profiles):
    swenv = SwitchEnv()
    ensure_profiles_exist(swenv)
    if not profiles:
        profiles = [swenv.get_key()]
    swenv = SwitchEnv()
    swenv.show(key_list=profiles)


@cli.command(help='Delete a profile')
@click.option('-p', '--profiles', multiple=True)
def delete(profiles):
    swenv = SwitchEnv()
    ensure_profiles_exist(swenv)
    if not profiles:
        profiles = [swenv.get_key()]

    confirm = input(f"\nDelete {profiles}\ny/n: ").lower()
    if confirm[0] != 'y':
        print('Nothing done')
        return

    initial_keys = set(swenv.keys)
    swenv.delete(keys=profiles)
    final_keys = set(swenv.keys)
    deleted_keys = initial_keys - final_keys
    if deleted_keys:
        print(f'Deleted profiles: {sorted(deleted_keys)}')


@cli.command(help='Create a profile from file')
@click.option('-p', '--profile_name', required=True)
@click.option('-f', '--file_name', required=True)
def add(profile_name, file_name):
    if not os.path.isfile(file_name):
        print(f"\nThe file '{file_name}' does not exist\n")
        sys.exit(1)

    with open(file_name, 'r') as code_file:
        code = code_file.read()

    blob = {profile_name: code}

    swenv = SwitchEnv()
    swenv.update(blob)


@cli.command(help='Snapshot current env into a profile')
@click.option('-p', '--profile_name', required=True)
def snapshot(profile_name):
    swenv = SwitchEnv()

    code_lines = []
    for key, val in swenv.env.items():
        code_lines.append(f'export {key}="{val}"')

    code = '\n'.join(code_lines)
    swenv.update({profile_name: code})


def main():
    if len(sys.argv) > 1:
        cli()
    else:
        run_switch_env()


if __name__ == '__main__':
    main()
