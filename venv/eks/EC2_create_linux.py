import logging
import boto3
from botocore.exceptions import ClientError
from eks_config import  keypair_name, instance_type, Linux_image_id, Linux_subnet, Linux_sg

def create_ec2_instance( Linux_image_id, instance_type, keypair_name, Linux_subnet, Linux_sg):

    ec2_client = boto3.client('ec2')
    try:
        response = ec2_client.run_instances(
                                            ImageId=Linux_image_id,
                                            InstanceType=instance_type,
                                            KeyName=keypair_name,
                                            SubnetId=Linux_subnet,
                                            SecurityGroupIds=Linux_sg,
                                            MinCount=1,
                                            MaxCount=1)
    except ClientError as e:
        logging.error(e)
        return None
    return response['Instances'][0]


def main():


    # Set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # Provision and launch the EC2 instance
    instance_info = create_ec2_instance(Linux_image_id, instance_type, keypair_name,Linux_subnet, Linux_sg)
    if instance_info is not None:
        logging.info(f'Launched EC2 Instance {instance_info["InstanceId"]}')
        logging.info(f'    VPC ID: {instance_info["VpcId"]}')
        logging.info(f'    Private IP Address: {instance_info["PrivateIpAddress"]}')
        logging.info(f'    Current State: {instance_info["State"]["Name"]}')


if __name__ == '__main__':
    main()
