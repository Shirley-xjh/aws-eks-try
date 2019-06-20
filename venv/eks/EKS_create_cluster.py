#! /usr/bin/python3.6

import boto3
import boto3.ec2
import sys
import json
import time
import subprocess
import os
import yaml
from EKS_create_IAMrole import role_arn
from EKS_config import vpc_subnet_ids,vpc_sg,cluster_name,region, k8s_version
############################################################################
# EKS cluster
############################################################################

print("*** EKS cluster********")

# Connect to AWS EKS
s = boto3.Session(region_name=region)
eks = s.client("eks")

try:
    cluster = eks.describe_cluster(name=cluster_name)
    print("Cluster already exists.")

except:

    print("Creating cluster (ETA ~10 minutes)...")

    # Create Kubernetes cluster.
    response = eks.create_cluster(
        name=cluster_name,
        version=k8s_version,
        roleArn=role_arn,
        resourcesVpcConfig={
            "subnetIds": vpc_subnet_ids,
            "securityGroupIds": [vpc_sg]
        }
    )

    print("Cluster creation initiated.")
    print("Waiting for completion (ETA 10 minutes)...")

    # Wait for two minutes before doing the checking.
    time.sleep(120)

    # Going to give up after 40 times 20 seconds.  Btw, EKS API / boto3 doesn't
    # currently support a 'waiter' object to wait for the cluster to start,
    # which would be nice.
    i = 40
    while True:

        # Wait 20 seconds
        time.sleep(20)

        try:

            # Get cluster status
            cluster = eks.describe_cluster(name=cluster_name)
            status = cluster["cluster"]["status"]

            print("Cluster status: %s" % status)

            # Is it active? If so break out of loop
            if status == "ACTIVE":
                break

            # Maybe give up after so many goes.
            i = i - 1
            if i <= 0:
                print("Given up waiting for cluster to go ACTIVE.")
                sys.exit(1)

        except (Exception, e):
            print("Exception:", e)

    print("Cluster active.")

# Get cluster stuff
cluster = eks.describe_cluster(name=cluster_name)

# This spots the case where the cluster isn't in an expected state.
status = cluster["cluster"]["status"]
if status != "ACTIVE":
    print("Cluster status %s, should be ACTIVE!" % status)
    sys.exit(1)
