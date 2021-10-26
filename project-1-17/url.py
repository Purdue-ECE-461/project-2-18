from datetime import datetime as dt  # pip install datetime
from git import Repo  # pip install GitPython
import shutil
import os
import re
import logging
import sys
import requests  # pip install PyGithub requests


class URL:

    # Get environment
    try:
        log_file = os.environ['LOG_FILE']
    except KeyError:
        logging.error("Couldn't find environment variable for 'LOG_FILE'")
        sys.exit()

    try:
        LOG_LEVEL = os.environ['LOG_LEVEL']
    except KeyError:
        logging.error("Couldn't find environment variable for 'LOG_LEVEL'")
        sys.exit()

    # Initialize

    if LOG_LEVEL == '0':
        log_level = logging.NOTSET
    elif LOG_LEVEL == '1':
        log_level = logging.INFO
    elif LOG_LEVEL == '2':
        log_level = logging.DEBUG
    else:
        logging.error(f"Log level %s is not defined", LOG_LEVEL)
        sys.exit()

    logging.basicConfig(filename=log_file, level=LOG_LEVEL)

    def __init__(self, url='', net_score=0, ramp_up=0, correctness=0, bus_factor=0, response=0, licen=0):
        self.url = url
        self.owner = ''
        self.repo = ''
        self.net_score = net_score
        self.ramp_up = ramp_up
        self.correctness = correctness
        self.bus_factor = bus_factor
        self.response = response
        self.license = licen

    def convert_npm_to_github(self):
        logging.info(f"Converting URL %s...", self.url)

        html = requests.get(self.url).text
        # Searches for GitHub URL in the raw html
        git_hub_url = re.search(r'("repository":".{0,100}","keywords")', html)

        # Check if repo was found
        if git_hub_url is None:
            logging.error("ERROR: GitHub URL not found from NPM site")
            return None

        repo = git_hub_url.group()[14:-12]
        self.url = repo

    def set_owner(self):
        logging.info(f"Getting owner for URL %s...", self.url)

        owner_string = re.search('.com/.*/', self.url)
        try:
            self.owner = owner_string.group()[5:-1]
        except Exception:
            logging.error(f"Invalid URL '%s', skipping tests", self.url)
            self.owner = -1

    def set_repo(self):
        logging.info(f"Getting repo for URL %s...", self.url)

        repoString = re.search(self.owner + '/.*', self.url)
        try:
            self.repo = repoString.group()[len(self.owner) + 1:]
        except Exception:
            logging.error(f"Invalid URL '%s', skipping tests", self.url)

            self.repo = -1

    def get_bus_factor(self):
        if int(os.getenv('LOG_LEVEL')) > 0:
            logging.info(f"Setting bus factor URL %s...", self.url)

        pat = os.getenv('GITHUB_TOKEN')
        if pat is None or pat == '':
            if int(os.getenv('LOG_LEVEL')) > 0:

                logging.info(f"ERROR: Bad credentials, setting net score to -1 for %s...", self.url)

            self.bus_factor = -1
            return

        header = {'Authorization': f'token {pat}'}

        # Formats URL to be in form 'https://api.github.com/repos/{owner}/{repo}/contributors'
        formattedURL = 'https://api.github.com/repos/' + self.owner + '/' + self.repo + '/contributors'

        # Obtains list of up to 100 contributors for specified repository, if possible
        # Otherwise, prints error message and exits 1
        response = requests.get(formattedURL, headers=header, params={'per_page': 100})
        try:
            numContributors = len(response.json()) + 1
        except Exception:
            logging.error(f"Error getting bus factor score with URL '%s'", self.url)

            self.bus_factor = -1
            return

        # Sets URL's bus factor score to 100 if repository has 100 or more contributors
        # Otherwise, sets bus factor score to number of contributors
        if numContributors >= 100:
            self.bus_factor = 1
        else:
            self.bus_factor = numContributors / 100

        return

    def get_responsiveness(self):
        if int(os.getenv('LOG_LEVEL')) > 0:
            logging.info(f"Getting responsiveness for URL %s...", self.url)

        pat = os.getenv('GITHUB_TOKEN')
        if pat is None or pat == '':
            if int(os.getenv('LOG_LEVEL')) > 0:

                logging.error(f"ERROR: Bad credentials, setting net score to -1 for %s...", self.url)

            self.response = -1
            return

        header = {'Authorization': f'token {pat}'}

        # Formats URL to be in form 'https://api.github.com/repos/{owner}/{repo}/releases/latest'
        formattedURL = 'https://api.github.com/repos/' + self.owner + '/' + self.repo + '/releases/latest'

        # Obtains value showing when repository was most recently updated as a datetime value, if possible
        # Otherwise, prints error message and exits 1
        response = requests.get(formattedURL, headers=header)
        try:
            last_updated_str = response.json()['published_at']
        except Exception:
            logging.error(f"Error getting responsiveness score, no release data with URL '%s'", self.url)

            self.response = 0
            return
        last_updated_dt = dt.strptime(last_updated_str, '%Y-%m-%dT%H:%M:%SZ')

        # Calculates difference between current datetime and when repository was most recently updated
        current_dt = dt.now()
        time_delta = current_dt - last_updated_dt

        # Calculates responsiveness score
        # Score starts at 100 and decreases by 5 points for every 30 days it has not been updated, starting from day 30
        responsiveness = 100 - (5 * (time_delta.days // 30))
        if responsiveness >= 0:
            self.response = responsiveness / 100
        else:
            self.response = 0

        return

    def get_ramp_up(self):
        if int(os.getenv('LOG_LEVEL')) > 0:
            logging.info(f"Getting ramp-up for URL %s...", self.url)

        if os.path.isdir("repo"):
            if int(os.getenv('LOG_LEVEL')) > 1:

                logging.info('Deleting exising repository folder...')

            shutil.rmtree('repo', ignore_errors=True)

        Repo.clone_from(self.url, "repo")

        if not os.path.isdir("repo"):
            logging.error(f"Unable to clone repository from '%s'", self.url)

            self.ramp_up = -1
            return

        readme_file = ''  # Filename of ReadMe
        for file in os.listdir('repo'):
            if 'readme' in file.lower():
                logging.error('readme found in: ' + file)

                readme_file = file
                break

        if readme_file == '':
            logging.error("Ramp Up score = 0, no README found")

            self.ramp_up = 0
            return

        with open('repo/' + readme_file, 'r') as readme:
            content = readme.read()

        if ("installation guide" in content.lower()) or ("quickstart guide" in content.lower()):
            logging.error("Ramp Up score = 100, Quickstart guide found")

            self.ramp_up = 1
        else:
            if len(content) < 1000:
                logging.error("Ramp Up score = " + str(len(content) / 1000) + " based on size of README")

                self.ramp_up = len(content) / 1000
            elif len(content) >= 1000:
                logging.error("Ramp Up score = 1 based on size of README")

                self.ramp_up = 1
            else:
                logging.error("Ramp Up score = 0.25, README found but not Quickstart guide found")

                self.ramp_up = 0.25

    def get_correctness(self):
        # REFERENCE: https://towardsdatascience.com/all-the-things-you-can-do-with-github-api-and-python-f01790fca131

        if int(os.getenv('LOG_LEVEL')) > 0:
            logging.info(f"Getting correctness for URL %s...", self.url)

        pat = os.getenv('GITHUB_TOKEN')
        if pat is None or pat == '':
            logging.error(f"ERROR: Bad credentials, setting net score to -1 for %s...", self.url)

            self.correctness = -1

        header = {'Authorization': f'token {pat}'}

        # Formats URL to be in form 'https://api.github.com/repos/{owner}/{repo}/releases/latest'
        commit_url = 'https://api.github.com/repos/' + self.owner + '/' + self.repo + '/releases/latest'
        commit_data = requests.get(commit_url, headers=header)
        commit_data = commit_data.json()

        # If there is an error acquiring the data, return a score of -1 and continue through program
        try:
            commit = commit_data["target_commitish"]
        except Exception:
            commit = 'master'

        api_url = 'https://api.github.com/repos/' + self.owner + '/' + self.repo + '/commits/' + commit
        state_url = 'https://api.github.com/repos/' + self.owner + '/' + self.repo + '/commits/' + commit + '/status'
        # print(stateURL)

        r = requests.get(api_url, headers=header)
        r2 = requests.get(state_url, headers=header)
        content = r.json()
        status = r2.json()
        # print(content['commit']['verification']['verified'])
        try:
            status["state"]
        except Exception:
            logging.error(f"Error getting correctness score with URL '%s'", self.url)

            self.correctness = -1
            return

        if status["state"] == 'success':
            logging.error("Correctness score = 100, master commit build succeeding\nExiting...")

            self.correctness = 1

        elif status['state'] == 'failure':
            logging.error("Correctness score = 0, master commit build failing\nExiting...")

            self.correctness = 0

        elif content['commit']['verification']['verified']:
            logging.error("Correctness score = 50, master commit verified, but no build info\nExiting...")

            self.correctness = 0.5
        else:
            logging.error("Correctness score = 0, no build info and master commit not verified\nExiting...")

            self.correctness = 0

    def get_license(self):
        if int(os.getenv('LOG_LEVEL')) > 0:
            logging.info(f"Getting license for URL %s...", self.url)

        if not os.path.isdir("repo"):
            logging.error(f"Unable to clone repository from '%s'", self.url)

            self.license = -1
            return

        readme_file = ''  # Filename of ReadMe
        for file in os.listdir('repo'):
            if 'readme' in file.lower():
                logging.error('readme found in: ' + file)

                readme_file = file
                break

        if readme_file == '':
            logging.error("License score = 0, no README found")

            shutil.rmtree('repo', ignore_errors=True)
            self.license = 0
            return

        with open('repo/' + readme_file, 'r') as readme:
            content = readme.read()

        license_string = re.search('lgpl.{0,20}2.1', content.lower())
        try:
            _ = license_string.group()
            logging.error("License score = 1, no matching license found")

            self.license = 1
        except Exception:
            logging.error("License score = 0, no matching license found")

            self.license = 0

    def get_net_score(self):
        if int(os.getenv('LOG_LEVEL')) > 0:
            logging.info(f"Getting net score for URL %s...", self.url)

        if self.ramp_up == -1 or self.correctness == -1 or self.bus_factor == -1 \
                or self.response == -1 or self.license == -1:
            self.net_score = -1
            return
        self.net_score = ((self.bus_factor * 0.4) + (self.response * 0.3) + (
                self.correctness + self.ramp_up) * 0.15) * self.license
