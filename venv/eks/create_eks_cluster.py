import boto3


def create_cluster(cluster_name):
    client = boto3.client('eks')
    try:
        response = client.create_cluster(
            name=cluster_name,
            # version='string',
            roleArn='arn:aws:iam::697508164634:role/eksServiceRole',
            resourcesVpcConfig={
                'subnetIds': ['subnet-0ddd4a920bddbc35a','subnet-047366517fbb8208b','subnet-0e5b0a8ba1adf8f86',],
                'securityGroupIds': ['sg-0c2e653e3738693a0',],
                'endpointPublicAccess': True,
                'endpointPrivateAccess': False
            },
        )

    except Exception as e:
        # e.response['Error']['Code'] == 'ResourceNotFoundException'
        return None
    return response['cluster']


def main():

    create_cluster_name='qa8'
    result = create_cluster(create_cluster_name)
    if result is None:
        print('ERROR: Could not create cluster')
    else:
        print('Cluster Name: {}'.format(result['name']))
        print('Status: {}'.format(result['status']))
        # Some information is not available until after the cluster has been created
        if result['status'] != 'CREATING':
            print('ARN: {}'.format(result['arn']))
            print('Endpoint: {}'.format(result['endpoint']))
            print('Certificate Authority (truncated): {}...'.format(result['certificateAuthority']['data'][:40]))
            print('all information:{}'.format(result))


if __name__ == '__main__':
    main()

