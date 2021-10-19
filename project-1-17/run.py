import sys # Import sys for argv
from sys import exit
# from url import URL # Import class data
import shutil
# import pytest #DEPENDENCIES: pip install pytest
import os
import re
import subprocess


if len(sys.argv) != 2:
    print("\ncorrect format: ./python run.py <some-filename>.txt\n")
    exit(1)

filename = sys.argv[1]

if filename == "install":
    exit(0)

from url import URL # Import class data after dependencies are installed
 
urlData = URL()
urlArray = []

if filename == "test":
    import pytest
    if os.path.isdir("repo"):
        if int(os.getenv('LOG_LEVEL')) > 1:
            logFile = open(os.getenv('LOG_FILE'), 'a')
            print('Deleting exising repository folder...', file=logFile)
            logFile.close()
        shutil.rmtree('repo', ignore_errors=True)
    prevLogLevel = os.getenv('LOG_LEVEL')
    os.environ['LOG_LEVEL'] = '2' # Set highest log level for best coverage/testing of log capabilities
    if int(os.getenv('LOG_LEVEL')) > 0:
        logFile = open(os.getenv('LOG_FILE'), 'w')
        print("running test package...\n", file=logFile)
        logFile.close()
    
    filename = 'test/testFile.txt'
    os.system("coverage run -m pytest test_run.py > test/log.txt")
    os.system("coverage report >> test/log.txt")
    testLog = open('test/log.txt', 'r')
    results = testLog.read()

    numPassed = re.search('\d* passed', results)
    if(not numPassed == None):
        if not numPassed[0][0:-7] == '':
            numPassed = int(numPassed[0][0:-7])
        else:
            numPassed = 0
    else:
            numPassed = 0
    
    numFailed = re.search('\d* failed', results)
    if(not numFailed == None):
        if not numFailed[0][0:-7] == '':
            numFailed = int(numFailed[0][0:-7])
        else:
            numFailed = 0
    else:
            numFailed = 0
    
    coverage = re.findall('\d{1,3}%', results)[-1]
    total = numPassed + numFailed

    print('Total: {}'.format(total))
    print('Passed: {}'.format(numPassed))
    print('Failed: {}'.format(numFailed))
    print('Coverage: ' + coverage)
    print('{}/{} test cases passed. '.format(numPassed, total) + coverage + ' line coverage achieved.')

    if int(os.getenv('LOG_LEVEL')) > 0:
        logFile = open(os.getenv('LOG_FILE'), 'a')
        print("\nTests completed, exiting...", file=logFile)
        logFile.close()
    os.environ['LOG_LEVEL'] = prevLogLevel # Return to original log level
    shutil.rmtree('repo', ignore_errors=True)
    exit(0)

# Check for valid filename
try:
    file = open(filename, 'r')
except:
    print("ERROR: Specified file '{}' not found!\nExiting...".format(filename))
    exit(1)

text = file.read()
URLs = text.split()

print('URL NET_SCORE RAMP_UP_SCORE CORRECTNESS_SCORE BUS_FACTOR_SCORE RESPONSIVE_MAINTAINER_SCORE LICENSE_SCORE')

for urlIdx in URLs:
    # Check if URL needs to be converted
    urlData = URL()
    urlData.url = urlIdx
    if('npmjs.com' in urlIdx):
        urlData.convertNpmToGitHub()
    
    urlData.setOwner()
    # Check for valid repo
    if(urlData.owner == -1):
        urlData.netScore = -1
        continue
    urlData.setRepo()
    # Check for valid repo
    if(urlData.repo == -1):
        urlData.netScore = -1
        continue
    urlData.getBusFactor()
    urlData.getResponsiveness()
    urlData.getRampUp()
    urlData.getCorrectness()
    urlData.getLicense()
    urlData.getNetScore()
    urlArray.append(urlData)

sortedURLS = sorted(urlArray, key=(lambda getNet: getNet.netScore), reverse=True)
for url in sortedURLS:
    print(url.url + ' ' +  str(url.netScore) + ' ' + str(url.rampUp) + ' ' + str(url.correctness) + ' ' + str(url.busFactor) +
        ' ' + str(url.response) + ' ' + str(url.license))

file.close()
shutil.rmtree('repo', ignore_errors=True)
if int(os.getenv('LOG_LEVEL')) > 0:
        logFile = open(os.getenv('LOG_FILE'), 'a')
        print("Successfully closing...", file=logFile)
        logFile.close()
        
exit(0)
