import requests  # pip install PyGithub requests
from datetime import datetime as dt  # pip install datetime
from git import Repo, exc # pip install GitPython
from sys import exit
import shutil
import os
import re

class URL:
    def __init__(self, url='', netScore=0, rampUp=0, correctness=0, busFactor=0, response=0, license=0):
        self.url = url
        self.owner = ''
        self.repo = ''
        self.netScore = netScore
        self.rampUp = rampUp
        self.correctness = correctness
        self.busFactor = busFactor
        self.response = response
        self.license = license

    def convertNpmToGitHub(self):
        if int(os.getenv('LOG_LEVEL')) > 0:
            logFile = open(os.getenv('LOG_FILE'), 'a')
            print("Converting URL {}...".format(self.url), file=logFile)
            logFile.close()

        html = requests.get(self.url).text
        # Searches for GitHub URL in the raw html
        gitHubUrl = re.search(r'("repository":".{0,100}","keywords")', html)
        
        # Check if repo was found
        if(gitHubUrl == None):
            if int(os.getenv('LOG_LEVEL')) == 2:
                logFile = open(os.getenv('LOG_FILE'), 'a')
                print("ERROR: GitHub URL not found from NPM site", file=logFile)
                logFile.close()
            return(None)
        
        repo = gitHubUrl.group()[14:-12]
        self.url = repo
    
    def setOwner(self):
        if int(os.getenv('LOG_LEVEL')) > 0:
            logFile = open(os.getenv('LOG_FILE'), 'a')
            print("Getting owner for URL {}...".format(self.url), file=logFile)
            logFile.close()

        ownerString = re.search('.com/.*/', self.url)
        try:
            self.owner = ownerString.group()[5:-1]
        except:
            if int(os.getenv('LOG_LEVEL')) == 2:
                logFile = open(os.getenv('LOG_FILE'), 'a')
                print("Invalid URL '{}', skipping tests".format(self.url), file=logFile)
                logFile.close()
            self.owner = -1
    
    def setRepo(self):
        if int(os.getenv('LOG_LEVEL')) > 0:
            logFile = open(os.getenv('LOG_FILE'), 'a')
            print("Getting repo for URL {}...".format(self.url), file=logFile)
            logFile.close()

        repoString = re.search(self.owner + '/.*', self.url)
        try:
            self.repo = repoString.group()[len(self.owner) + 1:]
        except:
            if int(os.getenv('LOG_LEVEL')) == 2:
                logFile = open(os.getenv('LOG_FILE'), 'a')
                print("Invalid URL '{}', skipping tests".format(self.url), file=logFile)
                logFile.close()
            self.repo = -1

    def getBusFactor(self):
        if int(os.getenv('LOG_LEVEL')) > 0:
            logFile = open(os.getenv('LOG_FILE'), 'a')
            print("Setting bus factor URL {}...".format(self.url), file=logFile)
            logFile.close()

        pat = os.getenv('GITHUB_TOKEN')
        if(pat == None or pat == ''):
            if int(os.getenv('LOG_LEVEL')) > 0:
                logFile = open(os.getenv('LOG_FILE'), 'a')
                print("ERROR: Bad credentials, setting net score to -1 for {}...".format(self.url), file=logFile)
                logFile.close()
            self.busFactor = -1
            return
        
        header = {'Authorization': f'token {pat}'}

        # Formats URL to be in form 'https://api.github.com/repos/{owner}/{repo}/contributors'
        formattedURL = 'https://api.github.com/repos/' + self.owner + '/' + self.repo + '/contributors'

        # Obtains list of up to 100 contributors for specified repository, if possible
        # Otherwise, prints error message and exits 1
        response = requests.get(formattedURL, headers=header, params={'per_page': 100})
        try:
            numContributors = len(response.json())+1
        except:
            if int(os.getenv('LOG_LEVEL')) == 2:
                logFile = open(os.getenv('LOG_FILE'), 'a')
                print("Error getting bus factor score with URL '{}'".format(self.url), file=logFile)
                logFile.close()
            self.busFactor = -1
            return

        # Sets URL's bus factor score to 100 if repository has 100 or more contributors
        # Otherwise, sets bus factor score to number of contributors
        if numContributors >= 100:
            self.busFactor = 1
        else:
            self.busFactor = numContributors / 100

        return

    def getResponsiveness(self):
        if int(os.getenv('LOG_LEVEL')) > 0:
            logFile = open(os.getenv('LOG_FILE'), 'a')
            print("Getting responsiveness for URL {}...".format(self.url), file=logFile)
            logFile.close()

        pat = os.getenv('GITHUB_TOKEN')
        if(pat == None or pat == ''):
            if int(os.getenv('LOG_LEVEL')) > 0:
                logFile = open(os.getenv('LOG_FILE'), 'a')
                print("ERROR: Bad credentials, setting net score to -1 for {}...".format(self.url), file=logFile)
                logFile.close()
            self.response = -1
            return
        
        header = {'Authorization': f'token {pat}'}

        # Formats URL to be in form 'https://api.github.com/repos/{owner}/{repo}/releases/latest'
        formattedURL = formattedURL = 'https://api.github.com/repos/' + self.owner + '/' + self.repo + '/releases/latest'

        # Obtains value showing when repository was most recently updated as a datetime value, if possible
        # Otherwise, prints error message and exits 1
        response = requests.get(formattedURL, headers=header)
        try:
            lastUpdatedStr = response.json()['published_at']
        except:
            if int(os.getenv('LOG_LEVEL')) == 2:
                logFile = open(os.getenv('LOG_FILE'), 'a')
                print("Error getting responsiveness score, no release data with URL '{}'".format(self.url), file=logFile)
                logFile.close()
            self.response = 0
            return
        lastUpdatedDT = dt.strptime(lastUpdatedStr, '%Y-%m-%dT%H:%M:%SZ')

        # Calculates difference between current datetime and when repository was most recently updated
        currentDT = dt.now()
        timeDelta = currentDT - lastUpdatedDT

        # Calculates responsiveness score
        # Score starts at 100 and decreases by 5 points for every 30 days it has not been updated, starting from day 30
        responsiveness = 100-(5*(timeDelta.days//30))
        if responsiveness >= 0:
            self.response = responsiveness / 100
        else:
            self.response = 0

        return

    def getRampUp(self):
        if int(os.getenv('LOG_LEVEL')) > 0:
            logFile = open(os.getenv('LOG_FILE'), 'a')
            print("Getting ramp-up for URL {}...".format(self.url), file=logFile)
            logFile.close()

        if os.path.isdir("repo"):
            if int(os.getenv('LOG_LEVEL')) > 1:
                logFile = open(os.getenv('LOG_FILE'), 'a')
                print('Deleting exising repository folder...', file=logFile)
                logFile.close()
            shutil.rmtree('repo', ignore_errors=True)

        Repo.clone_from(self.url, "repo")

        if not os.path.isdir("repo"):
            if int(os.getenv('LOG_LEVEL')) == 2:
                logFile = open(os.getenv('LOG_FILE'), 'a')
                print("Unable to clone repository from '{}'".format(self.url), file=logFile)
                logFile.close()
            self.rampUp = -1
            return

        readmeFile = '' # Filename of ReadMe
        for file in os.listdir('repo'):
            if 'readme' in file.lower():
                if int(os.getenv('LOG_LEVEL')) == 2:
                    logFile = open(os.getenv('LOG_FILE'), 'a')
                    print('readme found in: ' + file, file=logFile)
                    logFile.close()
                readmeFile = file
                break
        
        if (readmeFile == ''):
            if int(os.getenv('LOG_LEVEL')) == 2:
                logFile = open(os.getenv('LOG_FILE'), 'a')
                print("Ramp Up score = 0, no README found", file=logFile)
                logFile.close()
            self.rampUp = 0
            return
        
        readme = open('repo/' + readmeFile, 'r')
        content =readme.read()

        if ("installation guide" in content.lower()) or ("quickstart guide" in content.lower()):
            if int(os.getenv('LOG_LEVEL')) == 2:
                logFile = open(os.getenv('LOG_FILE'), 'a')
                print("Ramp Up score = 100, Quickstart guide found", file=logFile)
                logFile.close()
            readme.close()
            self.rampUp = 1
        else:
            if(len(content) < 1000):
                if int(os.getenv('LOG_LEVEL')) == 2:
                    logFile = open(os.getenv('LOG_FILE'), 'a')
                    print("Ramp Up score = " + str(len(content)/1000) + " based on size of README", file=logFile)
                    logFile.close()
                self.rampUp = len(content) / 1000
            elif(len(content) >= 1000):
                if int(os.getenv('LOG_LEVEL')) == 2:
                    logFile = open(os.getenv('LOG_FILE'), 'a')
                    print("Ramp Up score = 1 based on size of README", file=logFile)
                    logFile.close()
                self.rampUp = 1
            else:
                if int(os.getenv('LOG_LEVEL')) == 2:
                    logFile = open(os.getenv('LOG_FILE'), 'a')
                    print("Ramp Up score = 0.25, README found but not Quickstart guide found", file=logFile)
                    logFile.close()
                self.rampUp = 0.25


    def getCorrectness(self):
        #REFERENCE: https://towardsdatascience.com/all-the-things-you-can-do-with-github-api-and-python-f01790fca131

        if int(os.getenv('LOG_LEVEL')) > 0:
            logFile = open(os.getenv('LOG_FILE'), 'a')
            print("Getting correctness for URL {}...".format(self.url), file=logFile)
            logFile.close()

        pat = os.getenv('GITHUB_TOKEN')
        if(pat == None or pat == ''):
            if int(os.getenv('LOG_LEVEL')) > 0:
                logFile = open(os.getenv('LOG_FILE'), 'a')
                print("ERROR: Bad credentials, setting net score to -1 for {}...".format(self.url), file=logFile)
                logFile.close()
            self.correctness = -1
        
        header = {'Authorization': f'token {pat}'}

        # Formats URL to be in form 'https://api.github.com/repos/{owner}/{repo}/releases/latest'
        commitUrl = 'https://api.github.com/repos/' + self.owner + '/' + self.repo + '/releases/latest'
        commitData = requests.get(commitUrl, headers=header)
        commitData = commitData.json()

        # If there is an error acquiring the data, return a score of -1 and continue through program
        try:
            commit = commitData["target_commitish"]
        except:
            commit = 'master'

        apiURL = 'https://api.github.com/repos/' + self.owner + '/' + self.repo + '/commits/' + commit
        stateURL = 'https://api.github.com/repos/' + self.owner + '/' + self.repo + '/commits/' + commit + '/status'
        #print(stateURL)

        r = requests.get(apiURL, headers=header)
        r2 = requests.get(stateURL, headers=header)
        content = r.json()
        status = r2.json()
        #print(content['commit']['verification']['verified'])
        try:
            status["state"]
        except:
            if int(os.getenv('LOG_LEVEL')) == 2:
                logFile = open(os.getenv('LOG_FILE'), 'a')
                print("Error getting correctness score with URL '{}'".format(self.url), file=logFile)
                logFile.close()
            self.correctness = -1
            return
            
        if(status["state"] == 'success'):
            if int(os.getenv('LOG_LEVEL')) == 2:
                logFile = open(os.getenv('LOG_FILE'), 'a')
                print("Correctness score = 100, master commit build succeeding\nExiting...", file=logFile)
                logFile.close()
            self.correctness = 1

        elif(status['state'] == 'failure'):
            if int(os.getenv('LOG_LEVEL')) == 2:
                logFile = open(os.getenv('LOG_FILE'), 'a')
                print("Correctness score = 0, master commit build failing\nExiting...", file=logFile)
                logFile.close()
            self.correctness = 0

        elif(content['commit']['verification']['verified'] == True):
            if int(os.getenv('LOG_LEVEL')) == 2:
                logFile = open(os.getenv('LOG_FILE'), 'a')
                print("Correctness score = 50, master commit verified, but no build info\nExiting...", file=logFile)
                logFile.close()
            self.correctness = 0.5
        else:
            if int(os.getenv('LOG_LEVEL')) == 2:
                logFile = open(os.getenv('LOG_FILE'), 'a')
                print("Correctness score = 0, no build info and master commit not verified\nExiting...", file=logFile)
                logFile.close()
            self.correctness = 0
    
    def getLicense(self):
        if int(os.getenv('LOG_LEVEL')) > 0:
            logFile = open(os.getenv('LOG_FILE'), 'a')
            print("Getting license for URL {}...".format(self.url), file=logFile)
            logFile.close()

        if not os.path.isdir("repo"):
            if int(os.getenv('LOG_LEVEL')) == 2:
                logFile = open(os.getenv('LOG_FILE'), 'a')
                print("Unable to clone repository from '{}'".format(self.url), file=logFile)
                logFile.close()
            self.license = -1
            return

        readmeFile = '' # Filename of ReadMe
        for file in os.listdir('repo'):
            if 'readme' in file.lower():
                if int(os.getenv('LOG_LEVEL')) == 2:
                    logFile = open(os.getenv('LOG_FILE'), 'a')
                    print('readme found in: ' + file, file=logFile)
                    logFile.close()
                readmeFile = file
                break
        
        if (readmeFile == ''):
            if int(os.getenv('LOG_LEVEL')) == 2:
                logFile = open(os.getenv('LOG_FILE'), 'a')
                print("License score = 0, no README found", file=logFile)
                logFile.close()
            shutil.rmtree('repo', ignore_errors=True)
            self.license = 0
            return
        
        readme = open('repo/' + readmeFile, 'r')
        content =readme.read()

        licenseString = re.search('lgpl.{0,20}2.1', content.lower())
        try:
            licenseExist = licenseString.group()
            if int(os.getenv('LOG_LEVEL')) == 2:
                logFile = open(os.getenv('LOG_FILE'), 'a')
                print("License score = 1, no matching license found", file=logFile)
                logFile.close()
            self.license = 1
        except:
            if int(os.getenv('LOG_LEVEL')) == 2:
                logFile = open(os.getenv('LOG_FILE'), 'a')
                print("License score = 0, no matching license found", file=logFile)
                logFile.close()
            self.license = 0
    
    def getNetScore(self):
        if int(os.getenv('LOG_LEVEL')) > 0:
            logFile = open(os.getenv('LOG_FILE'), 'a')
            print("Getting net score for URL {}...".format(self.url), file=logFile)
            logFile.close()

        if self.rampUp == -1 or self.correctness == -1 or self.busFactor == -1 or self.response == -1 or self.license == -1:
            self.netScore = -1
            return
        self.netScore = ((self.busFactor*0.4) + (self.response*0.3) + (self.correctness + self.rampUp)*0.15) * self.license
