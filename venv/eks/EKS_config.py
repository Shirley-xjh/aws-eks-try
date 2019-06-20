#! /usr/bin/python3.6
import boto3
import boto3.ec2
import sys
import json
import time
import yaml
import subprocess
import os



############################################################################
# Config you might want to change
############################################################################

# AWS Region
region="us-west-2"

# Cluster name
cluster_name = "qafinal"

# K8s version to deploy
k8s_version = "1.11"

# Size of cluster.
node_group_min = 1
node_group_max = 3

# Worker instance types to deploy
instance_type="t2.small"


############################################################################
# Config you might not want to change
############################################################################

# Names for VPC and worker stack
vpc_name = cluster_name + "-vpc"
workers_name = cluster_name + "-workers"

# CloudFormation templates for VPC and worker nodes
#vpc_template = "https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/amazon-eks-vpc-sample.yaml"
workers_template = "https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-01-09/amazon-eks-nodegroup.yaml"

# K8s IAM role name to use
k8s_admin_role_name = "EksServiceManagement"

# Config file to write kubectl configuration to.
config_file = "kubeconfig.yaml"

# Keypair for accessing workers.  Keypair name and filename.
keypair_name = "eks-ec2"
#secret_file = "secret.pem"

# Image names for AMIs providing workers.
node_images = {
    "us-west-2": "ami-05ecac759c81e0b0c",
   # "us-east-1": "ami-dea4d5a1"
}

# Filename to write internal auth thing to.
worker_auth="aws-auth-cm.yaml"

#subnet and EKS security group
vpc_subnet_ids = ['subnet-0ddd4a920bddbc35a', 'subnet-047366517fbb8208b', 'subnet-0e5b0a8ba1adf8f86', ]
vpc_sg = 'sg-0c2e653e3738693a0'
vpc_id = 'vpc-0b9dffdcf7b6d9ace'

#images and subnets,security group  for ADC
ADC_image_id = 'ami-03e90a03889acb0c0'
ADC_subnet = 'subnet-0ddd4a920bddbc35a'
ADC_sg = ['sg-09065a9d409c4e50e']

#images and subnets,security group  for Linux Client

Linux_image_id = 'ami-03e90a03889acb0c0'
Linux_subnet = 'subnet-0ddd4a920bddbc35a'
Linux_sg = ['sg-09065a9d409c4e50e']


