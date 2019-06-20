import logging
import boto3
from botocore.exceptions import ClientError
from eks_config import  keypair_name, instance_type, ADC_image_id, ADC_subnet, ADC_sg

def create_ec2_instance( ADC_image_id, instance_type, keypair_name, ADC_subnet, ADC_sg):

    ec2_client = boto3.client('ec2')
    try:
        response = ec2_client.run_instances(
                                            ImageId=ADC_image_id,
                                            InstanceType=instance_type,
                                            KeyName=keypair_name,
                                            SubnetId=ADC_subnet,
                                            SecurityGroupIds=ADC_sg,
                                            MinCount=1,
                                            MaxCount=1)
    except ClientError as e:
        logging.error(e)
        return None
    return response['Instances'][0]


def main():
    """Exercise create_ec2_instance()"""


    # Set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # Provision and launch the EC2 instance
    instance_info = create_ec2_instance(ADC_image_id, instance_type, keypair_name,ADC_subnet, ADC_sg)
    if instance_info is not None:
        logging.info(f'Launched EC2 Instance {instance_info["InstanceId"]}')
        logging.info(f'    VPC ID: {instance_info["VpcId"]}')
        logging.info(f'    Private IP Address: {instance_info["PrivateIpAddress"]}')
        logging.info(f'    Current State: {instance_info["State"]["Name"]}')


if __name__ == '__main__':
    main()
