import boto3

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)

s3.put_object(Bucket='change-rates', Key='object_name', Body='TEST', StorageClass='COLD')
