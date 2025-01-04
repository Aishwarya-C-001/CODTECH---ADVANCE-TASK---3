# Multi-Cloud Architecture Design Example

# This example demonstrates deploying services across AWS and Azure

# AWS Lambda Function (Python Example)
import json
import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'aws-bucket-name'
    key = 'example.txt'

    # Fetch file from S3
    response = s3.get_object(Bucket=bucket_name, Key=key)
    data = response['Body'].read().decode('utf-8')

    return {
        'statusCode': 200,
        'body': json.dumps(f'File content: {data}')
    }

# Azure Function (Python Example)
import logging
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Azure function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello {name}!")
    else:
        return func.HttpResponse(
            "Please pass a name in the query string or in the request body",
            status_code=400
        )

# Integration: Use API Gateway (AWS) and Azure API Management for unified endpoint

# Infrastructure as Code (IaC) using Terraform for AWS S3 and Lambda Deployment
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "example_bucket" {
  bucket = "aws-bucket-name"
}

resource "aws_lambda_function" "example_lambda" {
  filename      = "lambda_function_payload.zip"
  function_name = "example_lambda"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"
}

# Azure Resource Deployment with Terraform
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example_rg" {
  name     = "example-resources"
  location = "East US"
}

resource "azurerm_app_service_plan" "example_plan" {
  name                = "example-app-service-plan"
  location            = azurerm_resource_group.example_rg.location
  resource_group_name = azurerm_resource_group.example_rg.name
  sku {
    tier = "Standard"
    size = "S1"
  }
}

resource "azurerm_function_app" "example_func" {
  name                = "example-function-app"
  location            = azurerm_resource_group.example_rg.location
  resource_group_name = azurerm_resource_group.example_rg.name
  app_service_plan_id = azurerm_app_service_plan.example_plan.id
}
