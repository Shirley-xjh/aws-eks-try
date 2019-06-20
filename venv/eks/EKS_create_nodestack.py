import boto3
import boto3.ec2
import sys
import json
import time
from EKS_config import vpc_subnet_ids,vpc_sg,cluster_name,region,workers_name,workers_template, node_group_min,node_group_max,keypair_name,instance_type,vpc_id,node_images



s = boto3.Session(region_name=region)
cf = s.client("cloudformation")



# Check if a stack exists.
def stack_exists(cf, name):
    try:
        stack = cf.describe_stacks(StackName=name)
        return True
    except:
        return False



print("*** Create EKS node Workers stack******")
if stack_exists(cf, workers_name):
    print("Workers stack already exists.")
else:
    print("Creating workers stack...")

# Create stack
    response = cf.create_stack(
        StackName=workers_name,
        TemplateURL=workers_template,
        Capabilities=["CAPABILITY_IAM"],
        Parameters=[
            {
                "ParameterKey": "ClusterName",
                "ParameterValue": cluster_name
            },
            {
                "ParameterKey": "ClusterControlPlaneSecurityGroup",
                "ParameterValue": vpc_sg
            },
            {
                "ParameterKey": "NodeGroupName",
                "ParameterValue": cluster_name + "-worker-group"
            },
            {
                "ParameterKey": "NodeAutoScalingGroupMinSize",
                "ParameterValue": str(node_group_min)
            },
            {
                "ParameterKey": "NodeAutoScalingGroupMaxSize",
                "ParameterValue": str(node_group_max)
            },
            {
                "ParameterKey": "NodeInstanceType",
                "ParameterValue": instance_type
            },
            {
                "ParameterKey": "NodeImageId",
                "ParameterValue": node_images[region]
            },
            {
                "ParameterKey": "KeyName",
                "ParameterValue": keypair_name
            },
            {
                "ParameterKey": "VpcId",
                "ParameterValue": vpc_id
            },
            {
                "ParameterKey": "Subnets",
                "ParameterValue": ",".join(vpc_subnet_ids)

            }
        ],
        TimeoutInMinutes=25,
        OnFailure='DELETE'
    )

    if response == None:
        print("Could not create worker group stack")
        sys.exit(1)

    if not "StackId" in response:
        print("Could not create worker group stack")
        sys.exit(1)

    print("Initiated workers (ETA 5-20 mins)...")

    print("Waiting for workers stack creation to complete...")

    try:
        # This is a waiter which waits for the stack deployment to complete.
        waiter = cf.get_waiter('stack_create_complete')
        res = waiter.wait(
            StackName=workers_name
        )
    except:
        print("Give up waiting for stack to create")
        sys.exit(1)

    print("Stack created")
