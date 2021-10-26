from sys import exit
from url import URL # Import class data
import os

url_array = []


def test_len():
    # Check for the right amount of URLs
    if int(os.getenv('LOG_LEVEL')) > 0:
        logFile = open(os.getenv('LOG_FILE'), 'a')
        print("Running testLen...", file=logFile)
        logFile.close()
    filename = 'test/testFile.txt'
    try:
        with open(filename, 'r') as file:
            text = file.read()
    except Exception:
        print("ERROR: Specified file '{}' not found!\nExiting...".format(filename))
        exit(1)

    URLs = text.split()

    for urlIdx in URLs:
        # Check if URL needs to be converted
        urlData = URL()
        urlData.url = urlIdx
        if 'npmjs' in urlIdx:
            urlData.convert_npm_to_github()

        urlData.set_owner()
        # Check for valid repo
        if urlData.owner == -1:
            urlData.net_score = -1
            continue
        urlData.set_repo()
        # Check for valid repo
        if urlData.repo == -1:
            urlData.net_score = -1
            continue

        url_array.append(urlData)
    assert len(url_array) == 10


def test_sort():
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

    url1.net_score = 0.2
    url2.net_score = 0.85
    url3.net_score = 0.7
    url4.net_score = 0.92
    url5.net_score = 0.4
    url_array = [url1, url2, url3, url4, url5]

    sortedURLS = sorted(url_array, key=(lambda getNet: getNet.net_score), reverse=True)

    idx = 0
    while idx < 4:
        assert sortedURLS[idx].net_score >= sortedURLS[idx + 1].net_score
        idx = idx + 1


def range_var(netScore):
    assert netScore == -1 or (1 >= netScore >= 0)


def test_range():
    # Check for values either -1 or within [0,1]
    if int(os.getenv('LOG_LEVEL')) > 0:
        logFile = open(os.getenv('LOG_FILE'), 'a')
        print("Running testRange...", file=logFile)
        logFile.close()
    with open('test/testFile.txt') as file:
        text = file.read()
    URLs = text.split()
    url_array = []

    for urlIdx in URLs:
        # Check if URL needs to be converted
        urlData = URL()
        urlData.url = urlIdx
        if 'npmjs' in urlIdx:
            urlData.convert_npm_to_github()

        urlData.set_owner()
        # Check for valid repo
        if urlData.owner == -1:
            urlData.net_score = -1
            continue
        urlData.set_repo()
        # Check for valid repo
        if urlData.repo == -1:
            urlData.net_score = -1
            continue
        urlData.get_bus_factor()
        urlData.get_responsiveness()
        urlData.get_ramp_up()
        urlData.get_correctness()
        urlData.get_license()
        urlData.get_net_score()
        url_array.append(urlData)

    assert True  # Completed acquisition of data successfully


def test_range_net():
    for url in url_array:
        assert url.net_score == -1 or (1 >= url.net_score >= 0)


def test_range_ramp():
    for url in url_array:
        assert url.ramp_up == -1 or (1 >= url.ramp_up >= 0)


def test_range_correct():
    for url in url_array:
        assert url.correctness == -1 or (1 >= url.correctness >= 0)


def test_convert():
    if int(os.getenv('LOG_LEVEL')) > 0:
        logFile = open(os.getenv('LOG_FILE'), 'a')
        print("Running testConvert...", file=logFile)
        logFile.close()
    url = URL()
    url.url = 'https://www.npmjs.com/package/express'
    url.convert_npm_to_github()
    assert url.url == 'https://github.com/expressjs/express'


def test_bad_PAT():
    # Check for bad PAT handling
    prevPAT = os.getenv('GITHUB_TOKEN')
    os.environ['GITHUB_TOKEN'] = ''
    if int(os.getenv('LOG_LEVEL')) > 0:
        logFile = open(os.getenv('LOG_FILE'), 'a')
        print("Running testBadPAT...", file=logFile)
        logFile.close()

    with open('test/testFile.txt') as file:
        text = file.read()
    URLs = text.split()
    url_array = []

    for urlIdx in URLs:
        # Check if URL needs to be converted
        urlData = URL()
        urlData.url = urlIdx
        if 'npmjs' in urlIdx:
            urlData.convert_npm_to_github()

        urlData.set_owner()
        # Check for valid repo
        if urlData.owner == -1:
            urlData.net_score = -1
            continue
        urlData.set_repo()
        # Check for valid repo
        if urlData.repo == -1:
            urlData.net_score = -1
            continue
        urlData.get_bus_factor()
        urlData.get_responsiveness()
        urlData.get_ramp_up()
        urlData.get_correctness()
        urlData.get_license()
        urlData.get_net_score()
        url_array.append(urlData)

    assert True  # Code didn't break after bad PAT was given
    os.environ['GITHUB_TOKEN'] = prevPAT  # Restore original PAT


def testRangeNetBadPAT():
    for url in url_array:
        assert url.net_score == -1 or (1 >= url.ramp_up >= 0)


def testRangeRampBadPAT():
    for url in url_array:
        assert url.ramp_up == -1 or (1 >= url.ramp_up >= 0)


def testRangeCorrectBadPAT():
    for url in url_array:
        assert url.correctness == -1 or (1 >= url.ramp_up >= 0)


def testRangeBusBadPAT():
    for url in url_array:
        assert url.bus_factor == -1 or (1 >= url.ramp_up >= 0)


def testRangeResponseBadPAT():
    for url in url_array:
        assert url.response == -1 or (1 >= url.ramp_up >= 0)


def testRangeLicenseBadPAT():
    for url in url_array:
        assert url.license == -1 or (1 >= url.license >= 0)


def test_ramp_up_guide():
    if int(os.getenv('LOG_LEVEL')) > 0:
        logFile = open(os.getenv('LOG_FILE'), 'a')
        print("Running testRampUpGuide...", file=logFile)
        logFile.close()
    # Test that program can find an installation guide
    url = URL()
    url.url = 'https://github.com/Purdue-ECESS/ecea-website-source-code'
    url.get_ramp_up()
    assert url.ramp_up == 1


def test_ramp_up_no_read_me():
    if int(os.getenv('LOG_LEVEL')) > 0:
        logFile = open(os.getenv('LOG_FILE'), 'a')
        print("Running testRampUpNoReadMe...", file=logFile)
        logFile.close()
    # Test that program can handle a lacking ReadMe
    url = URL()
    url.url = 'https://github.com/Purdue-ECESS/website'
    url.get_ramp_up()
    assert url.ramp_up < 0.5


def test_correctness():
    if int(os.getenv('LOG_LEVEL')) > 0:
        logFile = open(os.getenv('LOG_FILE'), 'a')
        print("Running testCorrectnessCI...", file=logFile)
        logFile.close()
    # Test that program can handle locating CI build info
    url = URL()
    url.url = 'https://github.com/expressjs/express'
    url.set_owner()
    url.set_repo()
    url.get_correctness()
    assert url.correctness == 1
