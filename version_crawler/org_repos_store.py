import datetime

import httpx

from version_crawler.file_parser.file_parser import FileParser

GITHUB_API_URL = "https://api.github.com"


class OrganizationRepositoriesStore:
    def __init__(self, repos_data: list, org_name: str, token: str):
        self.repos_data = repos_data
        self.org_name = org_name
        self.headers = {'Authorization': f'token {token}'}

    async def get_last_commit_date(self, url):
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)

            if response.status_code == 200:
                branch_data = response.json()
                last_commit_date = branch_data['commit']['commit']['committer']['date']
                return datetime.datetime.strptime(last_commit_date, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")

        return None

    async def get_updated_at(self, org_name, repo_name):
        target_branches = ['develop', 'main', 'master']
        for branch in target_branches:
            url = f"https://api.github.com/repos/{org_name}/{repo_name}/branches/{branch}"
            updated_at = await self.get_last_commit_date(url)
            if updated_at is not None:
                return updated_at
        return None

    async def analyze_repos(self, deprecated_repos: list, parser: FileParser, file_name: str):
        target_repo_nums = 0
        rows = []

        async with httpx.AsyncClient() as client:
            for repo in self.repos_data:
                repo_name = repo['name']
                if repo_name in deprecated_repos:
                    continue

                pipfile_api_url = f'{GITHUB_API_URL}/repos/{self.org_name}/{repo_name}/contents/{file_name}'
                response = await client.get(pipfile_api_url, headers=self.headers)

                if response.status_code == 200:
                    target_repo_nums += 1

                    versions = parser.parse_file(response, self.org_name, repo_name)

                    versions['Updated At'] = await self.get_updated_at(self.org_name, repo_name)

                    rows.append(versions)
                    print(f'{repo_name}: {versions}')

        return target_repo_nums, rows
