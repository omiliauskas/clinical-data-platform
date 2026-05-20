terraform {
    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = "~> 5.0"
        }
    }
}

provider "aws" {
    region = "eu-north-1"
}

resource "aws_s3_bucket" "clinical_data_lake" {
    bucket = "clinical-data-platform-omiliauskas"

    tags = {
        Project     = "clinical-data-platform"
        Environment = "dev"
    }
}

resource "aws_s3_bucket_versioning" "clinical_data_lake_versioning" {
    bucket = aws_s3_bucket.clinical_data_lake.id

    versioning_configuration {
        status = "Enabled"
    }
}

resource "aws_iam_role" "glue_role" {
    name = "clinical-data-platform-glue-role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Action = "sts:AssumeRole"
                Effect = "Allow"
                Principal = {
                    Service = "glue.amazonaws.com"
                }
            }
        ]
    })
}

resource "aws_iam_role_policy_attachment" "glue_s3_access" {
    role        = aws_iam_role.glue_role.name
    policy_arn  = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "glue_service_access" {
    role        = aws_iam_role.glue_role.name
    policy_arn  = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

resource "aws_glue_catalog_database" "clinical_database" {
    name = "clinical_data_platform"
}

resource "aws_glue_crawler" "clinical_crawler" {
    name            = "clinical-data-platform-crawler"
    role            = aws_iam_role.glue_role.arn
    database_name   = aws_glue_catalog_database.clinical_database.name

    s3_target {
      path = "s3://clinical-data-platform-omiliauskas/raw/"
    }

    schedule = "cron(0 12 * * ? *)"
}