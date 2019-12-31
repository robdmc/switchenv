# `switchenv`: An environment manger for bash
In my analysis work, I will frequently put auth credentials into environment
variables.  This allows me to check my code into Github without divulging any
secrets.  So, for example, I might have code in a Jupyter notebook that looks
something like
```python
import os
from my_module import get_database_connection

connection = get_database_connection(
    port=os.environ('PGPORT'),
    password=os.environ('PGPASSWORD'),
    user=os.environ('PGUSER'),
    database=os.environ('PGDATABASE'),
    host=os.environ('PGHOST'),
)
```
The database I connect to will be completely determined by the environment
variables I have defined.

`switchenv` gives me a way to easily navigate between different environments so
that, for example, I can quickly switch between development and production
databases.

# Install
`switchenv` is written in python.  You can install it with
```bash
pip install switchenv
```

# Use Case
Imagine I have the following bash files I can source in order to set up my bash
environment the way I'd like.  Typically I would just run `source
rc_development_db.sh` before running my code in order to set up my dev
environment.  However, I have to be very careful about where I place my rc files
so that I don't accidentally check them into Github.  Furthermore, it can be
annoying to keep track of these files when I'd like to reuse them for different
projects.  This is where `switchenv` comes in.

`rc_development_db.sh`
```bash
export MY_MESSAGE="You are in dev profile"
export PGPORT=5432
export PGPASSWORD=my_dev_password
export PGUSER=my_dev_username
export PGDATABASE=my_dev_database
export PGHOST=my_dev_host
```

`rc_production_db.sh`
```bash
export MY_MESSAGE="You are in prod profile"
export PGPORT=5432
export PGPASSWORD=my_prod_password
export PGUSER=my_prod_username
export PGDATABASE=my_prod_database
export PGHOST=my_prod_host
```

`rc_bash_functions.sh`
```bash

print_message () {
   echo "Current message is ${MY_MESSAGE}"
}
```

# Setting up `switchenv`
Below is copy-paste from an interactive bash session showing how to set up the
`switchenv` workflow.


```bash
bash>
bash> # Make sure I'm in a directory with the rc files I want
bash> ls *.sh
rc_development_db.sh  rc_production_db.sh  rc_bash_functions.sh
bash>
bash> # Load my rc scripts into switchenv giving them profile names
bash> switchenv add -p dev -f ./rc_development_db.sh
bash> switchenv add -p prod -f ./rc_production_db.sh
bash>
bash> # Profiles can hold any legal bash code, including function definitions.
bash> switchenv add -p func -f ./rc_bash_functions.sh
bash>
bash> # Show list of stored profile names
bash> switchenv list
dev
prod
func
bash>
bash> # Show contents of single profile
bash> switchenv show -p prod


#========================================
# prod
#========================================
export PGPORT=5432
export PGPASSWORD=my_prod_password
export PGUSER=my_prod_username
export PGDATABASE=my_prod_database
export PGHOST=my_prod_host
```

Under the hood, switchenv placed a json file in a hidden directory off of my
home directory.
```bash
~/.switchenv/profiles.json
```
This json file serves as the centralized data-store for all of my profile
information.

# Navigating Between Environments with `switchenv`
Using `switchenv` involves interacting with a simple console-based UI, so it is
best illustrated using a gif.  Shown here is my admittedly sub-par screen
recording of how to use switchenv.

Just for my future reference, I made this recording by using the native OSX
screen recording feature to make a `.mov` file.  I then used
[Gif Brewary 3](https://apps.apple.com/us/app/gif-brewery-3-by-gfycat/id1081413713?mt=12)
![Demo Gif](https://github.com/robdmc/switchenv/blob/master/images/switchenv_demo.gif)
to convert it to a `.gif` file by manually setting the speed to 150%  and
frames-per-sec to 6.  I let the software figure it out from there.
