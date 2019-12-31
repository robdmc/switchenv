# switchenv: An environment manger for bash
Switchenv allows you to manage your bash environment with user-defined profiles.

## The way you do it now
Take as an example the case where you are doing interactive work that requires
you to be connected to either a production or development database.  Instead
of remembering your credentials, you have two bash scripts that you source.  These
scripts will populate environment variables so that your db client will
automatically connect without you having to manually specify credentials.  You also
occasionally need to download data from Salesforce and have a third file you can source for loading those credentials.  Examples of what those files might look like
are shown below.

`rc_development_db.sh`
```bash
export GPORT=5432
export GPASSWORD=my_dev_password
export GUSER=my_dev_username
export GDATABASE=my_dev_database
export GHOST=my_dev_host
```

`rc_production_db.sh`
```bash
export PGPORT=5432
export PGPASSWORD=my_prod_password
export PGUSER=my_prod_username
export PGDATABASE=my_prod_database
export PGHOST=my_prod_host
```

`rc_salesforce.sh`
```bash
export SALESFORCE_SECURITY_TOKEN=my_long_sfdc_token
export SALESFORCE_PASSWORD=my_sfdc_password
export SALESFORCE_USERNAME=my_sfdc_username
```

Your current workflow might look something like
```bash
# Set up your credentials
source rc_development_db.sh
source rc_salesforce.sh

# Run a script that needs salesforce and db connection
python push_my_salesforce_stuff_to_db.py

# Run a notebook for interactively working with db and salesforce
jupyter notebook
```

This workflow is fine, and as long as you keep track of all the different
files you need to source for each task, it works pretty well.  `switchenv` is designed to make this workflow easier.

## The way you could be doing it.
Different components of your environment setup can be stored and sourced with
`switchenv`.  Invoking `switchenv` will drop you into a bash subshell with an environment that includes all specifications in that profile.  You can also compose profiles as we will show below.

### Set up profiles
First, define all the profiles you might care about
```
# Use the rc_developement script to define a profile named dev
switchenv add -p dev -f ./rc_development_db.sh

# Use the rc_production script to define a profile named dev
switchenv add -p dev -f ./rc_production_db.sh

# Define a salesforce profile
switchenv add -p salesforce -f ./rc_salesforce.sh
```

### Use profiles
