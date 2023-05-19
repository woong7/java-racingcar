import base64
import re


class PipFileParser:
    def __init__(self, target_libs: dict):
        self.target_libs = target_libs

    def parse_pip_file(self, response, org_name: str, repo_name: str):
        content = response.json()['content']
        decoded_content = base64.b64decode(content).decode('utf-8')

        versions = {'Repository': f"<a href='https://github.com/{org_name}/{repo_name}'>{repo_name}</a>"}

        for key, pattern in self.target_libs.items():
            match = re.search(pattern, decoded_content, re.MULTILINE)
            if match:
                versions[key] = match.group(1).replace("==", "")
            else:
                versions[key] = None

        return versions
