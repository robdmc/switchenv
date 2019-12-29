#! /usr/bin/env python


import os
import sys
import json
import click
import shutil
from typing import Optional, List
import fuzzypicker


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

    def __init__(self):
        # Ensure directory structure every time class is instantiate4d
        os.makedirs(self.BLOB_DIR, exist_ok=True)

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
        return fuzzypicker.picker(self.keys)

    def _reset(self):
        """
        Bust the cache for all cached properties
        """
        for attr in ['blob', 'keys']:
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
        print('=' * 40)
        print(key)
        print('=' * 40)
        print(self.blob[key])


def run_switch_env(profile: Optional[str] = None):
    print('Switchimng to profile', profile)


@click.group()
def cli():
    pass


@cli.command(help='List all profile names')
def list():
    swenv = SwitchEnv()
    if not swenv.keys:
        print('No saved profies')
    for key in swenv.keys:
        print(key)


@cli.command(help='Show contents of a single profile')
@click.option('-p', '--profiles', multiple=True)
def show(profiles):
    swenv = SwitchEnv()
    swenv.show(key_list=profiles)


@cli.command(help='Delete a profile')
def delete():
    click.echo('delete')


@cli.command(help='Create a profile from file')
@click.option('-p', '--profile_name', required=True)
@click.option('-f', '--file_name', required=True)
def create(profile_name, file_name):
    if not os.path.isfile(file_name):
        print(f"\nThe file '{file_name}' does not exist\n")
        sys.exit(1)

    with open(file_name, 'r') as code_file:
        code = code_file.read()

    blob = {profile_name: code}

    swenv = SwitchEnv()
    swenv.update(blob)






if __name__ == '__main__':
    if len(sys.argv) > 1:
        cli()
    else:
        run_switch_env()
