from git import Repo, GitCommandError
import json


class RepoStore:

    def __init__(self, link: str, dir_location: str):
        self.link = link
        self.dir_location = dir_location
        self.package_location = dir_location + '/package.json'

    def clone_repo(self):
        try:
            print("Cloning...")
            Repo.clone_from(self.link, self.dir_location)
        except GitCommandError:
            print("Repository already cloned!")

    def get_dependencies(self) -> dict:
        try:
            with open(self.package_location, 'r') as json_file:
                data = json.load(json_file)
                try:
                    data.get('dependencies').pop('github', None)
                except AttributeError:
                    print("Module has no dependencies listed!")
                    return {}
                return data.get('dependencies')
        except FileNotFoundError:
            print("No package.json file found! Please use clone_repo() first.")
            return {}
