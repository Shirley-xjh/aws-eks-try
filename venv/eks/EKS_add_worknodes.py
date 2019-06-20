#! /usr/bin/python3.6

import boto3
import boto3.ec2
import sys
import json
import time
import subprocess
import os
import yaml
from EKS_config import cluster_name,region, workers_name, worker_auth, config_file


s = boto3.Session(region_name=region)
cf = s.client("cloudformation")
eks = s.client("eks")


# Get stack info.
stack = cf.describe_stacks(StackName=workers_name)
node_instance_role = None

# We need NodeInstanceRole output.
for v in stack["Stacks"][0]["Outputs"]:
    if v["OutputKey"] == "NodeInstanceRole": node_instance_role = v["OutputValue"]

print("Node instance role: %s" % node_instance_role)

############################################################################
# EKS cluster
############################################################################


# Get cluster stuff
cluster = eks.describe_cluster(name=cluster_name)

# This spots the case where the cluster isn't in an expected state.
status = cluster["cluster"]["status"]
if status != "ACTIVE":
    print("Cluster status %s, should be ACTIVE!" % status)
    sys.exit(1)

# Get cluster endpoint and security info.
cluster_cert = cluster["cluster"]["certificateAuthority"]["data"]
cluster_ep = cluster["cluster"]["endpoint"]

print("Cluster: %s" % cluster_ep)

############################################################################
# K8s config
############################################################################

print("*** EKS configuration")

# This section creates a Kubernetes kubectl configuration file if one does
# not exist.

if os.path.isfile(config_file):
    print("Config exists already.")
else:

    cluster_config = {
        "apiVersion": "v1",
        "kind": "Config",
        "clusters": [
            {
                "cluster": {
                    "server": str(cluster_ep),
                    "certificate-authority-data": str(cluster_cert)
                },
                "name": "kubernetes"
            }
        ],
        "contexts": [
            {
                "context": {
                    "cluster": "kubernetes",
                    "user": "aws"
                },
                "name": "aws"
            }
        ],
        "current-context": "aws",
        "preferences": {},
        "users": [
            {
                "name": "aws",
                "user": {
                    "exec": {
                        "apiVersion": "client.authentication.k8s.io/v1alpha1",
                        "command": "aws-iam-authenticator",
                        "args": [
                            "token", "-i", cluster_name
                        ]
                    }
                }
            }
        ]
    }

    # Write in YAML.
    config_text = yaml.dump(cluster_config, default_flow_style=False)
    open(config_file, "w").write(config_text)

    print("Written to %s." % config_file)

############################################################################
# Introduce workers to master
############################################################################

# Final step is to deploy a config map which tells the master how to
# contact the workers.

print("*** Update worker auth")

# This is horrific.  Can't get K8s to use a file created by PyYAML.
config = "apiVersion: v1\nkind: ConfigMap\nmetadata:\n  name: aws-auth\n" + \
         "  namespace: kube-system\ndata:\n  mapRoles: |\n" + \
         "    - rolearn: " + node_instance_role + "\n" + \
         "      username: system:node:{{EC2PrivateDNSName}}\n" + \
         "      groups:\n        - system:bootstrappers\n        - system:nodes\n"

print("Write config map...")

open(worker_auth, "w").write(config)
print("**************apply nodes yaml file to cluster****************")


resp1 = subprocess.call(["kubectl", "--kubeconfig=%s" % config_file, "apply", "-f", worker_auth])

if resp1 != 0:
    print("The kubectl command didn't work.")
    sys.exit(1)


print("Written......")
time.sleep(30)
print("Try:")
print(" kubectl --kubeconfig=%s get nodes" % config_file)

resp2 = subprocess.call(['kubectl', "--kubeconfig=%s" %config_file, "get", "nodes"])



'''
resp2 = subprocess.Popen(['kubectl', "--kubeconfig=%s" %config_file, "get", "nodes"], stdout=subprocess.PIPE)
out= resp2.communicate()[0]
print(out)


if out == "NotReady":
    print("The K8S nodes are not ready.")
    sys.exit(1)





import shutil
kubectl_path = shutil.which('kubectl')
print('kubectl_path is : {0}'.format(kubectl_path))


'''