import boto3
import logging
from botocore.exceptions import ClientError


def s3_upload(id):
    logging.basicConfig(level=logging.INFO)

    try:
        s3_resource = boto3.resource(
            's3',
            endpoint_url='https://hanamo.s3.ir-thr-at1.arvanstorage.ir',
            aws_access_key_id='bf8d871b-baa2-4d39-97f9-3475f199cfec',
            aws_secret_access_key='932f6010d69c7b0018f4e82dc1657822917acdd4d2f9716b25146aced84bb3df'
        )

    except Exception as exc:
        logging.error(exc)
    else:
        try:
            bucket = s3_resource.Bucket('hanamo')
            file_path = 'H:\\cloud\\Tamrin 1\\image_upload\\' + id + '.jpg'
            object_name = id + ".jpg"

            with open(file_path, "rb") as image:
                bucket.put_object(
                    ACL='private',
                    Body=image,
                    Key=object_name
                )
        except ClientError as e:
            logging.error(e)


def s3_download(id):
    logging.basicConfig(level=logging.INFO)

    try:
        s3_resource = boto3.resource(
            's3',
            endpoint_url='https://hanamo.s3.ir-thr-at1.arvanstorage.ir',
            aws_access_key_id='bf8d871b-baa2-4d39-97f9-3475f199cfec',
            aws_secret_access_key='932f6010d69c7b0018f4e82dc1657822917acdd4d2f9716b25146aced84bb3df'
        )
    except Exception as exc:
        logging.error(exc)
    else:
        try:
            # bucket
            bucket = s3_resource.Bucket('hanamo')

            object_name = id + ".jpg"
            download_path = 'H:\\cloud\\Tamrin 1\\image_upload'

            bucket.download_file(
                object_name,
                download_path
            )
        except ClientError as e:
            logging.error(e)
