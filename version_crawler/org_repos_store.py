import httpx

from pip_parser import PipFileParser

GITHUB_API_URL = "https://api.github.com"


class OrganizationRepositoriesStore:
    def __init__(self, repos_data: list, org_name: str, token: str):
        self.repos_data = repos_data
        self.org_name = org_name
        self.headers = {'Authorization': f'token {token}'}

    async def analyze_repos(self, deprecated_repos: list, pip_parser: PipFileParser):
        target_repo_nums = 0
        rows = []

        async with httpx.AsyncClient() as client:
            for repo in self.repos_data:
                repo_name = repo['name']
                if repo_name in deprecated_repos:
                    continue

                pipfile_api_url = f'{GITHUB_API_URL}/repos/{self.org_name}/{repo_name}/contents/Pipfile'
                response = await client.get(pipfile_api_url, headers=self.headers)

                if response.status_code == 200:
                    target_repo_nums += 1

                    versions = pip_parser.parse_pip_file(response, self.org_name, repo_name)

                    rows.append(versions)
                    print(f'{repo_name}: {versions}')

        return target_repo_nums, rows
