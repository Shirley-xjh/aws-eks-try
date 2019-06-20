# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# This file is licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License. A copy of the
# License is located at
#
# http://aws.amazon.com/apache2.0/
#
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import boto3


def delete_cluster(cluster_name):
    """Retrieve information about an Amazon EKS cluster

    :param cluster_name: string
    :return: Dictionary containing information of cluster. If error, return None.
    """

    eks = boto3.client('eks')

    try:
        response = eks.delete_cluster(name=cluster_name)
    except Exception as e:
        # e.response['Error']['Code'] == 'ResourceNotFoundException'
        return None
    return response['cluster']


def main():
    delete_cluster_name = 'aaa2'
    #test_cluster_name = 'aaa2'
    result = delete_cluster(delete_cluster_name)
    if result is None:
        print('ERROR: Could not find information about cluster {}'.format(delete_cluster_name))
    else:
        print('Cluster Name: {}'.format(result['name']))
        print('Status: {}'.format(result['status']))
        # Some information is not available until after the cluster has been created
        if result['status'] != 'DELETING':
            print('ARN: {}'.format(result['arn']))
            print('Endpoint: {}'.format(result['endpoint']))
            print('Certificate Authority (truncated): {}...'.format(result['certificateAuthority']['data'][:40]))
            print('all information:{}'.format(result))

if __name__ == '__main__':
    main()
