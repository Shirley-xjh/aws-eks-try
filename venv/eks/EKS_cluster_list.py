import boto3


def list_clusters(max_clusters=10, iter_marker=''):
    """List the Amazon EKS clusters in the AWS account's default region.

    :param max_clusters: Maximum number of clusters to retrieve.
    :param iter_marker: Marker used to identify start of next batch of clusters to retrieve
    :return: List of cluster names
    :return: String marking the start of next batch of clusters to retrieve. Pass this string as the iter_marker
        argument in the next invocation of list_clusters().
    """

    eks = boto3.client('eks')

    clusters = eks.list_clusters(maxResults=max_clusters, nextToken=iter_marker)
    marker = clusters.get('nextToken')       # None if no more clusters to retrieve
    return clusters['clusters'], marker


def main():
    clusters, marker = list_clusters()
    if not clusters:
        print('No clusters exist.')
    else:
        while True:
            # Print cluster names
            for cluster in clusters:
                print(cluster)

            # If no more clusters exist, exit loop, otherwise retrieve the next batch
            if marker is None:
                break
            clusters, marker = list_clusters(iter_marker=marker)


if __name__ == '__main__':
    main()
