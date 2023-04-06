#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AWS Temp File uploader script.

This script will upload a file to AWS S3 and make it temporarily accessible.
Environent variables can be used to set the AWS access key ID, secret and
bucket or they can be set via the cli.

S3_TMPSHARE_ID=...
S3_TMPSHARE_SECRET=...
S3_TMPSHARE_BUCKET=...

"""
import argparse
import os
from pathlib import Path
from datetime import timedelta, datetime
# mimetype
import mimetypes


import boto3
# from botocore.client import Config

KEY_S3_ID = "S3_TMPSHARE_ID"
KEY_S3_SEC = "S3_TMPSHARE_SECRET"
KEY_S3_BUCKET = "S3_TMPSHARE_BUCKET"


def run(parser, args):
    """Run the script."""
    seconds = args.time * 60
    file = Path(args.file)
    key = file.name
    if file.is_dir():
        print("File is a directory")
        exit(parser.print_help())
    if seconds < 0 or seconds > 86400:
        print("Time must be between 1 and 1440 minutes (24 hours)")
        exit(parser.print_help())

    s3 = boto3.client(
        "s3",
        endpoint_url="https://s3.us-east-2.amazonaws.com",
        aws_access_key_id=args.id,
        aws_secret_access_key=args.secret,
        region_name="us-east-2",
    )
    print("Uploading file to S3")
    s3.upload_file(
        Filename=str(file.absolute()),
        Bucket=args.bucket,
        Key=key,
        ExtraArgs={
            "ContentType": mimetypes.guess_type(str(file.absolute()))[0],
        },
    )
    print("Making file temporarily accessible")
    url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": args.bucket,
            "Key": key,
        },
        ExpiresIn=seconds,
    )
    exptime = datetime.now() + timedelta(seconds=seconds)
    print(f"s3 path: s3://{args.bucket}/{key}")
    print(f"File will be available until {exptime}")
    print(f"File uploaded to:\n{url}")


def main():
    """Run main function."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__,
    )
    parser.add_argument(
        "file",
        help="file to make temporarily accessible",
        type=str,
    )
    parser.add_argument(
        "-t",
        "--time",
        help="number of minutes to make the file accessible, 1 to 1440 minutes (24)hours",
        type=int,
        default=60,  # 1 hour
    )
    parser.add_argument(
        "-i",
        "--id",
        help="AWS access key ID",
        type=str,
        default=os.environ.get(KEY_S3_ID),
    )
    parser.add_argument(
        "-s",
        "--secret",
        help="AWS access key SECRET",
        type=str,
        default=os.environ.get(KEY_S3_SEC),
    )
    parser.add_argument(
        "-b",
        "--bucket",
        help="AWS s3 bucket",
        type=str,
        default=os.environ.get(KEY_S3_BUCKET),
    )
    args = parser.parse_args()
    if not args.id:
        print("AWS access key ID not set")
    if not args.secret:
        print("AWS access key")
    if not args.bucket:
        print("AWS s3 bucket not set")
    if not all([args.id, args.secret, args.bucket]):
        exit(parser.print_help())
    run(parser, args)


if __name__ == "__main__":
    main()
