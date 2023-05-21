import os

aws_credential = {
    'aws_access_key_id': os.environ.get('AWS_ACCESS_KEY_ID'),
    'aws_secret_access_key': os.environ.get('AWS_SECRET_ACCESS_KEY')
}

s3_bucket_name = os.environ.get('AWS_S3_BUCKET')
s3_region = os.environ.get('AWS_S3_REGION')

s3_bucket_uri = f"https://{s3_bucket_name}.s3.{s3_region}.amazonaws.com"

# Personal access token 설정
token = os.environ.get('GH_PAT')

# organization 이름 설정
org_name = 'birdviewdev'

## 타겟 디펜던시 설정
python_target_libs = {
    'python_version': r'^[Pp]ython_version\s*=\s*[\'"]?(.*?)[\'"]?$',
    'django_version': r'^[Dd]jango\s*=\s*[\'"]?(.*?)[\'"]?$',
    'drf_version': r'^[Dd]jangorestframework\s*=\s*[\'"]?(.*?)[\'"]?$'
}

js_target_libs = {
    'node_version': r'"node"\s*:\s*"([^\s]+)"',
    'ts_version': r'"typescript"\s*:\s*"([^\s]+)"',
    'jest_version': r'"jest"\s*:\s*"([^\s]+)"'
}

## 사용하지 않는 레포지토리 설정
deprecated_repos = [
    'drf-api-common'
]
