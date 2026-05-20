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