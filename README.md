# Requirements

- [tfswitch](https://tfswitch.warrensbox.com/)
- `pip install boto3`

# How to use

Set your local `AWS_PROFILE` environment variable, or otherwise set your
environment to the aws account you want to use [see](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html)

## Setup AWS environment

_*!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!*_

_*!!!!! Be sure to change the values mentioned in [./tf/main.tf](./tf/main.tf)*_ 
_*before running apply*_

_*!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!*_

```
# fork/clone this repo
git clone <git url>

# change directory to repo terraform directory
cd <repo>/tf

# Switch to a supported version of terraform
tfswitch

# change the state to remote or remove the remote state all together if you
# don't want to go through the trouble and initialize state
# 
# Change the prefix in the `main.tf` file to fit your needs
terraform init

# tf plan / apply
terraform plan
terraform apply

# finally show the user and bucket variables that you'll be using in your
# environment variables or cli switches
terraform output -json
```


## OPTIONAL: set your environment variables to the outputs of the above command

Keep these secret, can be put in your `.bashrc` or `.zsh`
I recommend using [pass](https://www.passwordstore.org/) so they aren't
plaintext, i.e. `source <(pass show s3_tempstore_creds)>`

That file would look like this.

```sh
export S3_TMPSHARE_ID=...
export S3_TMPSHARE_SECRET=...
export S3_TMPSHARE_BUCKET=...
```

## cli tool

Link or copy the [s3_tmpshare.py]('./s3_tmpshare.py') file into your `bin`
directory.

- run `s3_tmpshare.py -h to see the cli options`

### Example
```
## Upload README.md and get back a URL good for five minutes
s3_tmpshare.py README.md -t 5
```
