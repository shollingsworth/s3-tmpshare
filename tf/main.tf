provider "aws" {
  region = "us-east-2"
}

data "aws_caller_identity" "current" {}

## change this prefix to fit your needs
locals {
  prefix = "shollingsworth-s3-tmpshare"
}

## Change these backend values to fit your needs. You can keep a separate TF repo just for storing you
## terraform states, see: https://gist.github.com/shollingsworth/1bb7b78e5fa20bfe55a28b91904b42ae
## Or you can just remove this block all together to store it locally, be sure to exclude the state from your .gitignore file
## if you do so.
terraform {
  backend "s3" {
    bucket         = "shollingsworth-terraform-tfstate"
    dynamodb_table = "shollingsworth-terraform-state-lock"
    key            = "s3-tmpshare/terraform.tfstate"
    region         = "us-east-2"
    encrypt        = true
  }
}

resource "aws_s3_bucket" "tmpstore" {
  bucket = "${local.prefix}-store"
}

resource "aws_s3_bucket_public_access_block" "public-access" {
  bucket = aws_s3_bucket.tmpstore.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# This deletes all files after 1 day
resource "aws_s3_bucket_lifecycle_configuration" "destination" {
  bucket = aws_s3_bucket.tmpstore.id

  rule {
    id = "onlytmp"

    expiration {
      days = 1
    }
    status = "Enabled"
  }
}

resource "aws_iam_user" "tmp_user" {
    name = "${local.prefix}-user"
}

resource "aws_iam_access_key" "tmp_user" {
    user = aws_iam_user.tmp_user.name
}

# limited IAM permissions just for this bucket
resource "aws_iam_user_policy" "tmp_user" {
    name = "${local.prefix}-user-policy"
    user = aws_iam_user.tmp_user.name
    policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Stmt1588210000000",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::${aws_s3_bucket.tmpstore.id}",
                "arn:aws:s3:::${aws_s3_bucket.tmpstore.id}/*"
            ]
        }
    ]
}
EOF
}

output "access_id" {
    value = aws_iam_access_key.tmp_user.id
}

output "access_key" {
    value = aws_iam_access_key.tmp_user.secret
    sensitive = true
}

output "bucket" {
  value = aws_s3_bucket.tmpstore.id
}
