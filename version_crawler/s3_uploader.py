import boto3


class S3Uploader:
    def __init__(self, aws_credential: dict, s3_bucket_name: str, s3_object_key):
        self.aws_credential = aws_credential
        self.s3_bucket_name = s3_bucket_name
        self.s3_object_key = s3_object_key

    def upload_to_s3(self, file_name):
        # S3에 파일 업로드
        s3_client = boto3.client('s3', **self.aws_credential)
        s3_client.upload_file(file_name, self.s3_bucket_name, self.s3_object_key,
                              ExtraArgs={'ContentType': 'text/html'})

        print("Uploaded to AWS S3")
