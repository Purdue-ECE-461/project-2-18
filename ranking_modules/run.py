import sys  # Import sys for argv
# from url import URL # Import class data
import shutil
# import pytest #DEPENDENCIES: pip install pytest
import os
import re
import logging
import json
from time import time

if len(sys.argv) != 2:
    print("\ncorrect format: ./python run.py <some-filename>.txt\n")
    sys.exit(1)

FILE_NAME = sys.argv[1]

if FILE_NAME == "install":
    sys.exit(0)


from url import URL  # Import class data after dependencies are installed

url_data = URL()
url_array = []

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

logging.basicConfig(filename=log_file, level=LOGGING_LEVEL)


if FILE_NAME == "tests":
    if os.path.isdir("repo"):
        logging.info('Deleting exising repository folder...')
        shutil.rmtree('repo', ignore_errors=True)
    prevLogLevel = os.getenv('LOG_LEVEL')
    os.environ['LOG_LEVEL'] = '2'  # Set highest log level for best coverage/testing of log capabilities
    logging.info("running tests package...")

    FILE_NAME = 'tests/testFile.txt'
    os.system("coverage run -m pytest test_run.py > tests/log.txt")
    os.system("coverage report >> tests/log.txt")
    with open('tests/log.txt', 'r', encoding='UTF-8') as testLog:
        results = testLog.read()

    num_passed = re.search('\d* passed', results)
    if num_passed is not None:
        if not num_passed[0][0:-7] == '':
            num_passed = int(num_passed[0][0:-7])
        else:
            num_passed = 0
    else:
        num_passed = 0

    num_failed = re.search('\d* failed', results)
    if num_failed is not None:
        if not num_failed[0][0:-7] == '':
            num_failed = int(num_failed[0][0:-7])
        else:
            num_failed = 0
    else:
        num_failed = 0

    coverage = re.findall('\d{1,3}%', results)[-1]
    total = num_passed + num_failed

    print(f'Total: {total}')
    print(f'Passed: {num_passed}')
    print(f'Failed: {num_failed}')
    print(f'Coverage: {coverage}')
    print(f'{num_passed}/{total} tests cases passed. {coverage} line coverage achieved.')

    logging.info("\nTests completed, exiting...")
    os.environ['LOG_LEVEL'] = prevLogLevel  # Return to original log level
    shutil.rmtree('repo', ignore_errors=True)
    sys.exit(0)


start_time = time()

# Check for valid filename
try:
    with open(FILE_NAME, 'r', encoding='UTF-8') as file:
        text = file.read()
except Exception:
    logging.error("ERROR: Specified file '%s' not found!\nExiting...", FILE_NAME)
    sys.exit(1)

URLs = text.split()

print('URL NET_SCORE RAMP_UP_SCORE CORRECTNESS_SCORE BUS_FACTOR_SCORE '
      'RESPONSIVE_MAINTAINER_SCORE DEPENDENCY_SCORE LICENSE_SCORE')

for url_idx in URLs:
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
url_data =[]
for url in sorted_urls:
    print(url.url + ' ' + str(url.net_score) + ' ' + str(url.ramp_up) + ' ' + str(url.correctness) + ' ' + str(
        url.bus_factor) +
          ' ' + str(url.response) + ' ' + str(url.dependency) + ' ' + str(url.license))
    url_data.append(url.make_dict())


full_dict = {'urls': url_data}
with open('modules.json', 'w') as file:
    json.dump(full_dict, file, indent="")

shutil.rmtree('repo', ignore_errors=True)
logging.info("Successfully closing...")
print(f"Runtime: {int(time() - start_time)} sec")

sys.exit(0)
