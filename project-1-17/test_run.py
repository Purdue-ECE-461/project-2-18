import sys # Import sys for argv
from sys import exit
from url import URL # Import class data
import shutil
import pytest #DEPENDENCIES: pip install pytest
import os

urlArray = []
def testLen():
    # Check for the right amount of URLs
    if int(os.getenv('LOG_LEVEL')) > 0:
        logFile = open(os.getenv('LOG_FILE'), 'a')
        print("Running testLen...", file=logFile)
        logFile.close()
    filename = 'test/testFile.txt'
    try:
        file = open(filename, 'r')
    except:
        print("ERROR: Specified file '{}' not found!\nExiting...".format(filename))
        exit(1)

    text = file.read()
    URLs = text.split()
    #urlArray = []

    for urlIdx in URLs:
        # Check if URL needs to be converted
        urlData = URL()
        urlData.url = urlIdx
        if('npmjs' in urlIdx):
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

        urlArray.append(urlData)
    assert len(urlArray) == 10

def testSort():
    # Make sure the URLs are sorted
    if int(os.getenv('LOG_LEVEL')) > 0:
        logFile = open(os.getenv('LOG_FILE'), 'a')
        print("Running testSort...", file=logFile)
        logFile.close()
    url1 = URL()
    url2 = URL()
    url3 = URL()
    url4 = URL()
    url5 = URL()

    url1.netScore = 0.2
    url2.netScore = 0.85
    url3.netScore = 0.7
    url4.netScore = 0.92
    url5.netScore = 0.4
    urlArray = [url1, url2, url3, url4, url5]

    sortedURLS = sorted(urlArray, key=(lambda getNet: getNet.netScore), reverse=True)

    idx = 0
    while idx < 4:
        assert sortedURLS[idx].netScore >= sortedURLS[idx+1].netScore
        idx = idx + 1

def rangeVar(netScore):
    assert netScore == -1 or (netScore <= 1 and netScore >= 0)

def testRange():
    # Check for values either -1 or within [0,1]
    if int(os.getenv('LOG_LEVEL')) > 0:
        logFile = open(os.getenv('LOG_FILE'), 'a')
        print("Running testRange...", file=logFile)
        logFile.close()

    file = open('test/testFile.txt')
    text = file.read()
    URLs = text.split()
    urlArray = []

    for urlIdx in URLs:
        # Check if URL needs to be converted
        urlData = URL()
        urlData.url = urlIdx
        if('npmjs' in urlIdx):
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

    assert True # Completed acquisition of data successfully

def testRangeNet():
    for url in urlArray:
        assert url.netScore == -1 or (url.netScore <= 1 and url.netScore >= 0)

def testRangeRamp():
    for url in urlArray:
        assert url.rampUp == -1 or (url.rampUp <= 1 and url.rampUp >= 0)

def testRangeCorrect():
    for url in urlArray:
        assert url.correctness == -1 or (url.correctness <= 1 and url.correctness >= 0)

def testRangeBus():
    for url in urlArray:
        assert url.busFactor == -1 or (url.busFactor <= 1 and url.busFactor >= 0)

def testRangeResponse():
    for url in urlArray:
        assert url.response == -1 or (url.response <= 1 and url.response >= 0)

def testRangeLicense():
    for url in urlArray:
        assert url.license == -1 or (url.license <= 1 and url.license >= 0)
            
    #print("Successfully closing...")

def testConvert():
    if int(os.getenv('LOG_LEVEL')) > 0:
        logFile = open(os.getenv('LOG_FILE'), 'a')
        print("Running testConvert...", file=logFile)
        logFile.close()
    url = URL()
    url.url = 'https://www.npmjs.com/package/express'
    url.convertNpmToGitHub()
    assert url.url == 'https://github.com/expressjs/express'

def testBadPAT():
    # Check for bad PAT handling
    prevPAT = os.getenv('GITHUB_TOKEN')
    os.environ['GITHUB_TOKEN'] = ''
    if int(os.getenv('LOG_LEVEL')) > 0:
        logFile = open(os.getenv('LOG_FILE'), 'a')
        print("Running testBadPAT...", file=logFile)
        logFile.close()

    file = open('test/testFile.txt')
    text = file.read()
    URLs = text.split()
    urlArray = []

    for urlIdx in URLs:
        # Check if URL needs to be converted
        urlData = URL()
        urlData.url = urlIdx
        if('npmjs' in urlIdx):
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

    assert True # Code didn't break after bad PAT was given
    os.environ['GITHUB_TOKEN'] = prevPAT # Restore original PAT

def testRangeNetBadPAT():
    for url in urlArray:
        assert url.netScore == -1 or (url.rampUp <= 1 and url.rampUp >= 0)

def testRangeRampBadPAT():
    for url in urlArray:
        assert url.rampUp == -1 or (url.rampUp <= 1 and url.rampUp >= 0)

def testRangeCorrectBadPAT():
    for url in urlArray:
        assert url.correctness == -1 or (url.rampUp <= 1 and url.rampUp >= 0)

def testRangeBusBadPAT():
    for url in urlArray:
        assert url.busFactor == -1 or (url.rampUp <= 1 and url.rampUp >= 0)

def testRangeResponseBadPAT():
    for url in urlArray:
        assert url.response == -1 or (url.rampUp <= 1 and url.rampUp >= 0)

def testRangeLicenseBadPAT():
    for url in urlArray:
        assert url.license == -1 or (url.license <= 1 and url.license >= 0)

def testRampUpGuide():
    if int(os.getenv('LOG_LEVEL')) > 0:
        logFile = open(os.getenv('LOG_FILE'), 'a')
        print("Running testRampUpGuide...", file=logFile)
        logFile.close()
    # Test that program can find an installation guide
    url = URL()
    url.url = 'https://github.com/Purdue-ECESS/ecea-website-source-code'
    url.getRampUp()
    assert url.rampUp == 1

def testRampUpNoReadMe():
    if int(os.getenv('LOG_LEVEL')) > 0:
        logFile = open(os.getenv('LOG_FILE'), 'a')
        print("Running testRampUpNoReadMe...", file=logFile)
        logFile.close()
    # Test that program can handle a lacking ReadMe
    url = URL()
    url.url = 'https://github.com/Purdue-ECESS/website'
    url.getRampUp()
    assert url.rampUp < 0.5

def testCorrectnessCI():
    if int(os.getenv('LOG_LEVEL')) > 0:
        logFile = open(os.getenv('LOG_FILE'), 'a')
        print("Running testCorrectnessCI...", file=logFile)
        logFile.close()
    # Test that program can handle locating CI build info
    url = URL()
    url.url = 'https://github.com/expressjs/express'
    url.setOwner()
    url.setRepo()
    url.getCorrectness()
    assert url.correctness == 1
