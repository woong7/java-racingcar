import datetime

from constants import token, org_name, target_libs, deprecated_repos, aws_credential, s3_bucket_name, s3_object_key, \
    s3_bucket_uri
from github_crawler import GithubCrawler
from html_generator import HTMLGenerator
from org_repos_store import OrganizationRepositoriesStore
from pip_parser import PipFileParser
from s3_uploader import S3Uploader


# GitHub API에서 organization에 속한 레포지토리 정보 가져오기
async def crawl_repos_in_org():
    repos_data = await GithubCrawler(token).get_all_repos_from_org(org_name)
    if repos_data is None:
        return

    repo_nums = len(repos_data)
    print(f"Total {repo_nums} repositories exist\n")

    return OrganizationRepositoriesStore(repos_data, org_name, token)


async def parse_data_from_org_repos_store(org_repos_store: OrganizationRepositoriesStore):
    pip_parser = PipFileParser(target_libs)

    target_repo_nums, rows = await org_repos_store.analyze_repos(deprecated_repos, pip_parser)

    print(f"\nTotal {target_repo_nums} repositories have dependencies on target libraries")

    return rows


def generate_html_and_upload_to_s3(rows: list):
    # 현재 시간 계산
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = HTMLGenerator(s3_bucket_uri=s3_bucket_uri).generate_html(rows, current_time)

    file_name = "result.html"

    # HTML 파일로 저장
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(html)

    S3Uploader(aws_credential, s3_bucket_name, s3_object_key).upload_to_s3(file_name)


async def main():
    org_repos_store = await crawl_repos_in_org()

    rows = await parse_data_from_org_repos_store(org_repos_store)

    generate_html_and_upload_to_s3(rows)


# 비동기 함수 실행
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
