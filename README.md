# Purpose
Give temporary file links to folks to GET (download) a file, or PUT (upload) a file that automatically expire!

This setup uses s3 as a temporary file store along with using aws presigned urls.

Terraform sets up a bucket, and a lifecycle rule that auto expires any
documents older than 24 hours, along with creating a limited service account user that
can only manipulate items in that bucket.

The [s3_tmpshare.py](./s3_tmpshare.py) script uses the outputs from the
terraform to quickly share files and provide others with a public link that
expires in a set amount of time between 1 minute and 24 hours.


# Requirements

-   [tfswitch](https://tfswitch.warrensbox.com/)
-   `pip install boto3`

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
plaintext, i.e. `source <(pass show s3_tempstore_creds)`

That file would look like this.

```sh
export S3_TMPSHARE_ID=...
export S3_TMPSHARE_SECRET=...
export S3_TMPSHARE_BUCKET=...
```

## cli tool

Link or copy the [s3_tmpshare.py](./s3_tmpshare.py) file into your `bin`
directory.

-   run `s3_tmpshare.py -h to see the cli options`

### Example

## Give HTTP GET URL (sending someone a temp url)
```
## Upload README.md and get back a URL good for five minutes
s3_tmpshare.py get README.md -t 5
```

OUTPUT:

```
-----------------------------------------
Uploading file to S3
-----------------------------------------
Making file temporarily accessible
-----------------------------------------
s3 path: s3://shollingsworth-s3-tmpshare-store/README.md
-----------------------------------------
File will be available until 2023-04-06 15:27:32.607002
-----------------------------------------
URL:
https://s3.us-east-2.amazonaws.com/shollingsworth-s3-tmpshare-store/README.md?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAZXN7Q4BXW4NDOBA2%2F20230406%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230406T222232Z&X-Amz-Expires=300&X-Amz-SignedHeaders=host&X-Amz-Signature=f277d22f968222cf127adc8414d2e9ac3c710ceb1e157946d621d1cea73a32b3
```

If expired it will return a result like this:

```
This XML file does not appear to have any style information associated with it. The document tree is shown below.
<Error>
<Code>AccessDenied</Code>
<Message>Request has expired</Message>
<X-Amz-Expires>300</X-Amz-Expires>
<Expires>2023-04-06T21:48:53Z</Expires>
<ServerTime>2023-04-06T21:48:54Z</ServerTime>
<RequestId>86C34AMV3X936RKK</RequestId>
<HostId>87XL/7ZNe9jiiLMUZ2JHZXiQ7CdDHUWUcFFiFRti73y07WC0x2k/SxFwpbwKwqlUszLJoIXh1rk=</HostId>
</Error>
```

## Give HTTP PUT URL (someone sending me a file)
```
## Upload README.md and get back a URL good for five minutes
s3_tmpshare.py post foo.md -t 5
```

OUTPUT:

```
-----------------------------------------
Getting post upload link
-----------------------------------------
s3 path: s3://shollingsworth-s3-tmpshare-store/foo.md
-----------------------------------------
File will be available until 2023-04-11 15:38:28.357796
-----------------------------------------
URL:
https://s3.us-east-2.amazonaws.com/shollingsworth-s3-tmpshare-store/foo.md?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAZXN7Q4BXW4NDOBA2%2F20230411%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230411T223328Z&X-Amz-Expires=300&X-Amz-SignedHeaders=host&X-Amz-Signature=000ff872b588b848abcd36b3b79539c543accbaac9770247422c25ad4077ef0d
-----------------------------------------
curl command:
curl -X PUT -T foo.md https://s3.us-east-2.amazonaws.com/shollingsworth-s3-tmpshare-store/foo.md?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAZXN7Q4BXW4NDOBA2%2F20230411%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230411T223328Z&X-Amz-Expires=300&X-Amz-SignedHeaders=host&X-Amz-Signature=000ff872b588b848abcd36b3b79539c543accbaac9770247422c25ad4077ef0d
-----------------------------------------
wating for file to be uploaded...
-----------------------------------------
file downloaded
```
