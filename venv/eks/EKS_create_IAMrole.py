#! /usr/bin/python3.6
import boto3
import boto3.ec2
import sys
import json
import time
import yaml
import subprocess
import os
from EKS_config import k8s_admin_role_name,region

# Connect to AWS, EC2, cloudformation, IAM and EKS
s = boto3.Session(region_name=region)
iam = s.client("iam")


############################################################################
# IAM role for K8s
############################################################################

print("*** IAM role***********")

try:

    # See if role exists.
    role = iam.get_role(RoleName=k8s_admin_role_name)
    print("IAM role exists.")

except:
    print("IAM role does not exist.  Creating...")

    # This is an AWS role policy document.  Allows access for EKS.
    policy_doc = json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Effect": "Allow",
                "Principal": {
                    "Service": "eks.amazonaws.com"
                }
            }
        ]
    })

    # Create role.
    iam.create_role(
        RoleName=k8s_admin_role_name,
        AssumeRolePolicyDocument=policy_doc,
        Description="Role providing access to EKS resources from EKS"
    )

    print("Role created.")
    print("Attaching policies...")

    # Add policies allowing access to EKS API.

    iam.attach_role_policy(
        RoleName=k8s_admin_role_name,
        PolicyArn="arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
    )

    iam.attach_role_policy(
        RoleName=k8s_admin_role_name,
        PolicyArn="arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
    )

    print("Attached.")

# Get role ARN for later.
role = iam.get_role(RoleName=k8s_admin_role_name)
role_arn = role["Role"]["Arn"]

print(role_arn)