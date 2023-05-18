import requests
import re
import base64
import os

GITHUB_API_URL = "https://api.github.com"

# Personal access token 설정
token = os.environ.get('GH_PAT')
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
def get_all_repos_from_org(org_name):
    all_repos = []
    page_number = 1
    per_page = 100

    while True:
        url = f"{GITHUB_API_URL}/orgs/{org_name}/repos"
        params = {
            'per_page': per_page,
            'page': page_number
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Failed to retrieve repos for {org_name}.")
            return None

        repos = response.json()
        all_repos.extend(repos)

        if len(repos) < per_page:
            break

        page_number += 1

    return all_repos


def main():
    # GitHub API에서 organization에 속한 레포지토리 정보 가져오기
    repos_data = get_all_repos_from_org(org_name)
    if repos_data is None:
        return

    repo_nums = len(repos_data)
    print(f"Total {repo_nums} repositories exist\n")

    # 각 레포지토리의 Pipfile에서 python_version, django 버전 추출하기
    target_repo_nums = 0
    rows = []
    for repo in repos_data:
        repo_name = repo['name']
        if repo_name in deprecated_repos:
            continue

        pipfile_api_url = f'{GITHUB_API_URL}/repos/{org_name}/{repo_name}/contents/Pipfile'
        response = requests.get(pipfile_api_url, headers=headers)

        if response.status_code == 200:
            target_repo_nums += 1
            content = response.json()['content']
            decoded_content = base64.b64decode(content).decode('utf-8')

            versions = {}
            versions['Repository'] = f"<a href='https://github.com/birdviewdev/{repo_name}'>{repo_name}</a>"  # 레포지토리 이름 추가

            for key, pattern in target_libs.items():
                match = re.search(pattern, decoded_content, re.MULTILINE)
                if match:
                    versions[key] = match.group(1).replace("==", "")
                else:
                    versions[key] = None
            rows.append(versions)
            print(f'{repo_name}: {versions}')

    print(f"\nTotal {target_repo_nums} repositories have dependencies on target libraries")

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
        <style>
            table {{border-collapse: collapse;}}
            th, td {{padding: 8px; border: 1px solid #ddd;}}
        </style>
    </head>
    <body>
        <table>
            <tr>
                <th>Repository</th>
                <th>Python Version</th>
                <th>Django Version</th>
                <th>DRF Version</th>
            </tr>
            {table_rows}
        </table>
    </body>
    </html>
    """

    # HTML 파일로 저장
    with open("result.html", "w") as file:
        file.write(html)

    print("HTML 파일로 저장되었습니다.")


# 동기 함수 실행
if __name__ == "__main__":
    main()
