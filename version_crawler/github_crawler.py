import httpx

GITHUB_API_URL = "https://api.github.com"


class GithubCrawler:
    def __init__(self, token: str):
        self.headers = {'Authorization': f'token {token}'}

    ## Github API는 최대 응답 길이 제한이 100이고, 현재 114개의 레포지토리가 있어서 Pagination 필요
    async def get_all_repos_from_org(self, org_name):
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
                response = await client.get(url, headers=self.headers, params=params)

                if response.status_code != 200:
                    print(f"Failed to retrieve repos for {org_name}.")
                    return None

                repos = response.json()
                all_repos.extend(repos)

                if len(repos) < per_page:
                    break

                page_number += 1

        return all_repos
