import logging
import os
import sys

from ranking_modules.url import URL  # Import class data

# Configure logging
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
    LOGGING_LEVEL = logging.NOTSET
elif LOG_LEVEL == '1':
    LOGGING_LEVEL = logging.INFO
elif LOG_LEVEL == '2':
    LOGGING_LEVEL = logging.DEBUG
else:
    logging.error("Log level %s is not defined", LOG_LEVEL)
    sys.exit()

logging.basicConfig(filename=log_file, level=LOG_LEVEL)

url_array = []


def get_urls():
    file_name = './ranking_modules/tests/test.txt'
    try:
        with open(file_name, 'r', encoding='UTF-8') as file:
            text = file.read()
        return text.split()
    except FileNotFoundError:
        logging.error("ERROR: Specified file '%s' not found!\nExiting...", file_name)
        sys.exit(1)


def test_len():
    # Check for the right amount of URLs
    logging.info("Running test_len...")
    urls = get_urls()

    for url_idx in urls:
        # Check if URL needs to be converted
        url_data = URL()
        url_data.url = url_idx
        if 'npmjs' in url_idx:
            url_data.convert_npm_to_github()

        url_data.set_owner()
        # Check for valid repo
        if url_data.owner == -1:
            url_data.net_score = -1
            continue
        url_data.set_repo()
        # Check for valid repo
        if url_data.repo == -1:
            url_data.net_score = -1
            continue

        url_array.append(url_data)
    assert len(url_array) == 2


def test_sort():
    # Make sure the URLs are sorted
    logging.info("Running testSort...")
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
    urls = [url1, url2, url3, url4, url5]

    sorted_urls = sorted(urls, key=(lambda get_net: get_net.net_score), reverse=True)

    idx = 0
    while idx < 4:
        assert sorted_urls[idx].net_score >= sorted_urls[idx + 1].net_score
        idx += 1


def range_var(net_score):
    assert net_score == -1 or (1 >= net_score >= 0)


def test_range():
    # Check for values either -1 or within [0,1]
    logging.info("Running test_range...",)
    urls = get_urls()
    url_arr = []

    for url_idx in urls:
        # Check if URL needs to be converted
        url_data = URL()
        url_data.url = url_idx
        if 'npmjs' in url_idx:
            url_data.convert_npm_to_github()

        url_data.set_owner()
        # Check for valid repo
        if url_data.owner == -1:
            url_data.net_score = -1
            continue
        url_data.set_repo()
        # Check for valid repo
        if url_data.repo == -1:
            url_data.net_score = -1
            continue
        url_data.get_bus_factor()
        url_data.get_responsiveness()
        url_data.get_ramp_up()
        url_data.get_correctness()
        url_data.get_license()
        url_data.get_net_score()
        url_arr.append(url_data)

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
    logging.info("Running testConvert...")
    url = URL()
    url.url = 'https://www.npmjs.com/package/express'
    url.convert_npm_to_github()
    assert url.url == 'https://github.com/expressjs/express'


def test_bad_pat():
    # Check for bad PAT handling
    prev_pat = os.getenv('GITHUB_TOKEN')
    logging.info("Running testBadPAT...")

    urls = get_urls()
    url_arr = []

    for url_idx in urls:
        # Check if URL needs to be converted
        url_data = URL()
        url_data.url = url_idx
        if 'npmjs' in url_idx:
            url_data.convert_npm_to_github()

        url_data.set_owner()
        # Check for valid repo
        if url_data.owner == -1:
            url_data.net_score = -1
            continue
        url_data.set_repo()
        # Check for valid repo
        if url_data.repo == -1:
            url_data.net_score = -1
            continue
        url_data.get_bus_factor()
        url_data.get_responsiveness()
        url_data.get_ramp_up()
        url_data.get_correctness()
        url_data.get_license()
        url_data.get_net_score()
        url_arr.append(url_data)

    assert True  # Code didn't break after bad PAT was given
    os.environ['GITHUB_TOKEN'] = prev_pat  # Restore original PAT


def test_range_net_bad_pat():
    for url in url_array:
        assert url.net_score == -1 or (1 >= url.ramp_up >= 0)


def test_range_ramp_bad_pat():
    for url in url_array:
        assert url.ramp_up == -1 or (1 >= url.ramp_up >= 0)


def test_range_correct_bad_pat():
    for url in url_array:
        assert url.correctness == -1 or (1 >= url.ramp_up >= 0)


def test_range_bus_bad_pat():
    for url in url_array:
        assert url.bus_factor == -1 or (1 >= url.ramp_up >= 0)


def test_range_response_bad_pat():
    for url in url_array:
        assert url.response == -1 or (1 >= url.ramp_up >= 0)


def test_range_license_bad_pat():
    for url in url_array:
        assert url.license == -1 or (1 >= url.license >= 0)


def test_ramp_up_guide():
    logging.info("Running testRampUpGuide...")
    # Test that program can find an installation guide
    url = URL()
    url.url = 'https://github.com/Purdue-ECESS/ecea-website-source-code'
    url.get_ramp_up()
    assert url.ramp_up == 1


def test_ramp_up_no_read_me():
    logging.info("Running testRampUpNoReadMe...")
    # Test that program can handle a lacking ReadMe
    url = URL()
    url.url = 'https://github.com/Purdue-ECESS/website'
    url.get_ramp_up()
    assert url.ramp_up < 0.5


def test_correctness():
    logging.info("Running testCorrectnessCI...")
    # Test that program can handle locating CI build info
    url = URL()
    url.url = 'https://github.com/expressjs/express'
    url.set_owner()
    url.set_repo()
    url.get_correctness()
    assert url.correctness == 1
