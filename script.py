import httpx
import re
import base64
import os
import boto3
import datetime

GITHUB_API_URL = "https://api.github.com"
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
s3_bucket_name = os.environ.get('AWS_S3_BUCKET')
s3_object_key = os.environ.get('RESULT_FILE')
s3_region = os.environ.get('AWS_S3_REGION')

s3_bucket_uri = f"https://{s3_bucket_name}.s3.{s3_region}.amazonaws.com"

# Personal access token 설정
token = os.environ.get('GITHUB_TOKEN')
headers = {'Authorization': f'token {token}'}

# organization 이름 설정
org_name = 'birdviewdev'

## 타겟 디펜던시 설정
target_libs = {
    'python_version': r'^[Pp]ython_version\s*=\s*[\'"]?(.*?)[\'"]?$',
    'django_version': r'^[Dd]jango\s*=\s*[\'"]?(.*?)[\'"]?$',
    'drf_version': r'^[Dd]jangorestframework\s*=\s*[\'"]?(.*?)[\'"]?$'
}

## 사용하지 않는 레포지토리 설정
deprecated_repos = [
    'drf-api-common'
]

## Github API는 최대 응답 길이 제한이 100이고, 현재 114개의 레포지토리가 있어서 Pagination 필요
async def get_all_repos_from_org(org_name):
    all_repos = []
    page_number = 1
    per_page = 100

    async with httpx.AsyncClient() as client:
        while True:
            url = f"{GITHUB_API_URL}/orgs/{org_name}/repos"
            params = {
                'per_page': per_page,
                'page': page_number
            }
            response = await client.get(url, headers=headers, params=params)

            if response.status_code != 200:
                print(f"Failed to retrieve repos for {org_name}.")
                return None

            repos = response.json()
            all_repos.extend(repos)

            if len(repos) < per_page:
                break

            page_number += 1

    return all_repos


async def main():
    # GitHub API에서 organization에 속한 레포지토리 정보 가져오기
    repos_data = await get_all_repos_from_org(org_name)
    if repos_data is None:
        return

    repo_nums = len(repos_data)
    print(f"Total {repo_nums} repositories exist\n")

    # 각 레포지토리의 Pipfile에서 python_version, django 버전 추출하기
    target_repo_nums = 0
    rows = []
    async with httpx.AsyncClient() as client:
        for repo in repos_data:
            repo_name = repo['name']
            if repo_name in deprecated_repos:
                continue

            pipfile_api_url = f'{GITHUB_API_URL}/repos/{org_name}/{repo_name}/contents/Pipfile'
            response = await client.get(pipfile_api_url, headers=headers)

            if response.status_code == 200:
                target_repo_nums += 1
                content = response.json()['content']
                decoded_content = base64.b64decode(content).decode('utf-8')

                versions = {}
                versions['Repository'] = f"<a href='https://github.com/{org_name}/{repo_name}'>{repo_name}</a>"  # 레포지토리 이름 추가

                for key, pattern in target_libs.items():
                    match = re.search(pattern, decoded_content, re.MULTILINE)
                    if match:
                        versions[key] = match.group(1).replace("==", "")
                    else:
                        versions[key] = None
                rows.append(versions)
                print(f'{repo_name}: {versions}')

    print(f"\nTotal {target_repo_nums} repositories have dependencies on target libraries")

    # 현재 시간 계산
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # HTML 템플릿 생성
    table_rows = ""
    for row in rows:
        table_row = "<tr>"
        for value in row.values():
            table_row += f"<td>{value}</td>"
        table_row += "</tr>"
        table_rows += table_row

    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
            }}
            .container {{
                display: flex;
                align-items: flex-start;
                justify-content: center;
                margin: 20px;
            }}
            .title {{
                display: flex;
                align-items: center;
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 20px;
            }}
            .title img {{
                margin-right: 10px;
                width: 180px;
                height: 180px;
            }}
            .title-text {{
                margin-left: 10px;
            }}
            .time {{
                font-size: 16px;
                margin-top: 5px;
                color: #888;  
                text-align: center;
            }}
            table {{
                border-collapse: collapse;
                flex: 1;
                margin-right: 20px;
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 4px;
            }}
            th, td {{
                padding: 10px;
                border: 1px solid #ddd;
                text-align: center;
            }}
            th {{
                background-color: #f5f5f5;
                cursor: pointer;
            }}
            .image-container {{
                flex: 0 0 300px;
            }}
            .image-container p {{
                font-weight: bold;
                margin-bottom: 10px;
                text-align: center;
            }}
            .image-divider {{
                border-top: 1px solid #ddd;
                margin-top: 20px;
                padding-top: 10px;
            }}
        </style>
        <script>
            function sortTable(column) {{
                const table = document.getElementById("repositories-table");
                const rows = Array.from(table.rows).slice(1);  // 테이블 행을 배열로 변환하고 첫 번째 행(헤더) 제외

                rows.sort(function(a, b) {{
                    const textA = a.cells[column].textContent.trim();
                    const textB = b.cells[column].textContent.trim();
                    return textA.localeCompare(textB, 'en', {{ numeric: true, sensitivity: 'base' }});
                }});

                // 정렬된 행을 테이블에 다시 추가
                rows.forEach(function(row) {{
                    table.appendChild(row);
                }});
            }}
        </script>
    </head>
    <body>
        <div class="container">
            <div class="title">
                <img src="{s3_bucket_uri}/bep_logo.png" alt="Logo">
                <div class="title-text">
                    Birdview Backend Repositories Version Dashboard
                    <div class="time">Recently updated at {current_time}</div>
                </div>
                <img src="{s3_bucket_uri}/bep_logo.png" alt="Logo" style="transform: scaleX(-1);">
            </div>
        </div>
        <div class="container">
            <div>
                <h2>Current Repositories Status</h2>
                <p> -> Click on column title to sort by that column</p>
                <table id="repositories-table">
                    <tr>
                        <th onclick="sortTable(0)">Repository</th>
                        <th onclick="sortTable(1)">Python Version</th>
                        <th onclick="sortTable(2)">Django Version</th>
                        <th onclick="sortTable(3)">DRF Version</th>
                    </tr>
                    {table_rows}
                </table>
            </div>
            
            <div class="image-container">
                <p><a href="https://www.python.org/downloads/">Python Version Support</a></p>
                <img src="{s3_bucket_uri}/python_version_info.png" alt="Python Version">
                <div class="image-divider"></div>
                <p><a href="https://www.djangoproject.com/download/">Django Version Support</a></p>
                <img src="{s3_bucket_uri}/django_version_info.png" alt="Django Version">
            </div>
        </div>
    </body>
    </html>
    """

    # HTML 파일로 저장
    with open("result.html", "w", encoding="utf-8") as file:
        file.write(html)

    # S3에 파일 업로드
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    s3_client.upload_file("result.html", s3_bucket_name, s3_object_key, ExtraArgs={'ContentType': 'text/html'})

    print("Uploaded to AWS S3")


# 비동기 함수 실행
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
