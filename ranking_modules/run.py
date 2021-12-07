import json
import logging
import os
import re
import shutil
import sys
from time import time

from url import URL


def main():

    if len(sys.argv) != 2:
        print("\ncorrect format: ./python run.py <some-filename>.txt\n")
        sys.exit(1)

    file_name = sys.argv[1]

    if file_name == "install":
        sys.exit(0)

    url_array = []

    # Configure logging
    try:
        log_file = os.environ['LOG_FILE']
    except KeyError:
        logging.error("Couldn't find environment variable for 'LOG_FILE'")
        sys.exit()

    try:
        log_level = os.environ['LOG_LEVEL']
    except KeyError:
        logging.error("Couldn't find environment variable for 'LOG_LEVEL'")
        sys.exit()

    # Initialize

    if log_level == '0':
        logging_level = logging.NOTSET
    elif log_level == '1':
        logging_level = logging.INFO
    elif log_level == '2':
        logging_level = logging.DEBUG
    else:
        logging.error("Log level %s is not defined", log_level)
        sys.exit()

    logging.basicConfig(filename=log_file, level=logging_level)

    if file_name == "tests":
        if os.path.isdir("repo"):
            logging.info('Deleting exising repository folder...')
            shutil.rmtree('repo', ignore_errors=True)
        os.environ['LOG_LEVEL'] = '2'  # Set highest log level for best coverage/testing of log capabilities
        logging.info("running tests package...")

        # file_name = 'tests/testFile.txt'
        os.system("coverage run -m pytest test_run.py > tests/log.txt")
        os.system("coverage report >> tests/log.txt")
        with open('tests/log.txt', 'r', encoding='UTF-8') as testLog:
            results = testLog.read()

        search = re.search('\\d* passed', results)
        if search is not None:
            if not search[0][0:-7] == '':
                num_passed = int(search[0][0:-7])
            else:
                num_passed = 0
        else:
            num_passed = 0

        search = re.search('\\d* failed', results)
        if search is not None:
            if not search[0][0:-7] == '':
                num_failed = int(search[0][0:-7])
            else:
                num_failed = 0
        else:
            num_failed = 0

        coverage = re.findall('\\d{1,3}%', results)[-1]
        total = num_passed + num_failed

        print(f'Total: {total}')
        print(f'Passed: {num_passed}')
        print(f'Failed: {num_failed}')
        print(f'Coverage: {coverage}')
        print(f'{num_passed}/{total} tests cases passed. {coverage} line coverage achieved.')

        logging.info("\nTests completed, exiting...")
        shutil.rmtree('repo', ignore_errors=True)
        sys.exit(0)

    start_time = time()

    if file_name.endswith('.txt'):
        # Check for valid filename
        try:
            with open(file_name, 'r', encoding='UTF-8') as file:
                text = file.read()
                urls = text.split()
        except FileNotFoundError:
            logging.error("ERROR: Specified file '%s' not found!\nExiting...", file_name)
            sys.exit(1)

    elif file_name.endswith('.json'):
        with open(file_name, 'r') as json_file:
            data: dict = json.load(json_file)

        try:
            url = data['data']['URL']
            urls = [url]
        except KeyError:
            logging.error("Package doesn't have a url key")
            sys.exit(1)

    else:
        logging.error("Filetype not recognised!")
        sys.exit(1)

    print('URL NET_SCORE RAMP_UP_SCORE CORRECTNESS_SCORE BUS_FACTOR_SCORE '
          'RESPONSIVE_MAINTAINER_SCORE DEPENDENCY_SCORE LICENSE_SCORE')

    for url_idx in urls:
        # Check if URL needs to be converted
        url_data = URL()
        url_data.url = url_idx
        if 'npmjs.com' in url_idx:
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
        url_data.get_dependecy_score()
        url_data.get_net_score()
        url_array.append(url_data)

    sorted_urls = sorted(url_array, key=(lambda get_net: get_net.net_score), reverse=True)
    url_scores = []
    for url in sorted_urls:
        print(url.url + ' ' + str(url.net_score) + ' ' + str(url.ramp_up) + ' ' + str(url.correctness) + ' ' + str(
            url.bus_factor) +
              ' ' + str(url.response) + ' ' + str(url.dependency) + ' ' + str(url.license))
        url_scores.append(url.make_dict())

    with open('modules.json', 'w') as file:
        json.dump(url_scores, file, indent="")

    shutil.rmtree('repo', ignore_errors=True)
    logging.info("Successfully closing...")
    print(f"Runtime: {int(time() - start_time)} sec")

    sys.exit(0)


if __name__ == '__main__':
    main()
