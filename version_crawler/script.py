import datetime

from constants import token, org_name, deprecated_repos, aws_credential, s3_bucket_name, s3_bucket_uri, python_target_libs, js_target_libs
from github_crawler import GithubCrawler
from org_repos_store import OrganizationRepositoriesStore
from s3_uploader import S3Uploader

from version_crawler.file_parser import FileParser
from version_crawler.html_generator.html_generator import HTMLGenerator
from version_crawler.html_generator.js_html_generator import JSHTMLGenerator
from version_crawler.html_generator.python_html_generator import PythonHTMLGenerator


# GitHub API에서 organization에 속한 레포지토리 정보 가져오기
async def crawl_repos_in_org():
    repos_data = await GithubCrawler(token).get_all_repos_from_org(org_name)
    if repos_data is None:
        return

    repo_nums = len(repos_data)
    print(f"Total {repo_nums} repositories exist\n")

    return OrganizationRepositoriesStore(repos_data, org_name, token)


async def parse_data_from_org_repos_store(org_repos_store: OrganizationRepositoriesStore, target_libs: dict, file_name: str):
    file_parser = FileParser(target_libs)

    target_repo_nums, rows = await org_repos_store.analyze_repos(deprecated_repos, file_parser, file_name)

    print(f"\nTotal {target_repo_nums} repositories have dependencies on target libraries")

    return rows


def generate_html_and_upload_to_s3(rows: list, html_generator: HTMLGenerator, s3_object_key: str):
    # 현재 시간 계산
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = html_generator.generate_html(rows, current_time)

    # HTML 파일로 저장
    with open(s3_object_key, "w", encoding="utf-8") as file:
        file.write(html)

    S3Uploader(aws_credential, s3_bucket_name, s3_object_key).upload_to_s3(s3_object_key)


async def main():
    org_repos_store = await crawl_repos_in_org()

    rows_python = await parse_data_from_org_repos_store(org_repos_store, python_target_libs, 'Pipfile')

    generate_html_and_upload_to_s3(rows_python, PythonHTMLGenerator(s3_bucket_uri), 'backend-version-info.html')

    rows_js = await parse_data_from_org_repos_store(org_repos_store, js_target_libs, 'package.json')

    generate_html_and_upload_to_s3(rows_js, JSHTMLGenerator(s3_bucket_uri), 'js-version-info.html')


# 비동기 함수 실행
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
