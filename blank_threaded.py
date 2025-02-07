#!/usr/bin/env python3

__author__ = 'thedzy'
__copyright__ = 'Copyright 2024, thedzy'
__license__ = 'GPL'
__version__ = '1.0'
__maintainer__ = 'thedzy'
__email__ = 'thedzy@hotmail.com'
__status__ = 'Development'
__date__ = '${YEAR}-${MONTH}-${DAY}'
__description__ = \
    """
    ${FILE_NAME}: 
    ${Description}
    """

#set($include = "starting value so your not prompted with variable")

#set($requiredParam = "")
#set($optionalParam = "")

#macro(setDefaults $requiredParam $optionalParam)
#if($requiredParam && !$requiredParam.isEmpty())
$requiredParam
#else
$optionalParam
#end
#end

import argparse
import collections
import logging
import logging.config
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import pprint
import random
import threading
import time
from pathlib import Path
from typing import Optional

#foreach($include in $Includes.split(","))
#if(($include) && ($include != ""))
import $include
#end
#end

import google.auth.exceptions
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


#parse("ThreadManager")

#parse("ColourFormat")

#parse("ProgressBar")

def main() -> None:
    logger.info('Start')

    start_time = time.time()
    loop_low, loop_high = 10, 500
    sleep_low, sleep_high = 0, 10
    semaphores = 200

    loops = random.randrange(loop_low, loop_high)
    print(f'Generating {loops} threads that will take {sleep_low} to {sleep_high} seconds each to complete')
    print(f'Processing {semaphores} threads at a time (semaphores)')

    with ProgressBar(loops, 'Starting',
                     foreground_rgb=(1.0, 1.0, 0.2,), background_rgb=(0.0, 0.0, 0.6), invert=True,
                     columns=80) as progress:
        # Create managing class, with up to n concurrent processes
        with ThreadManager(semaphores=semaphores) as thread_manager:
            # Create process threads
            for thread_number in range(loops):
                # Append the function to the queue (function, parameters, keywords).
                thread_manager.append(random_sleep, thread_number, low=sleep_low, high=sleep_high)

            # While the queue is not empty
            total_time = 0
            while thread_manager.active_count() > 0:
                # Get one value at a time
                thread_number, value = thread_manager.get_value()
                progress.increment(title=f'Completed thread #{thread_number:2}')

                # Track total function time
                total_time += value

            # Let us see the bar complete, for demo only
            progress.draw(loops, 'Done')
            time.sleep(1)

    print(f'Total CPU Time      {total_time:9.1f}s')
    print(f'Should have taken   {total_time / 60:9.1f}m')
    print(f'Actual time taken   {time.time() - start_time:9.1f}s')

    logger.info('Done')


def random_sleep(thread_number, low, high):
    # Let's create a function to spend time
    timer_sleep = random.uniform(low, high)
    time.sleep(timer_sleep)

    return thread_number, timer_sleep


def auth_google(scopes: list, credentials_json: str, save_json: bool = False) -> Credentials:
    """
    Authenticate with Google Workspaces API
    :param scopes: List of scopes to authenticate with
    :param credentials_json: Json file with credentials
    :param save_json: Save scope and token to json file
    :return: Credentials object
    """
    credentials_file = Path(__file__).parent.joinpath(credentials_json.name)
    # Check if credentials file already contains credentials and token
    try:
        credentials = Credentials.from_authorized_user_file(credentials_file, scopes)
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        return credentials
    except ValueError:
        try:
            logger.info('Web credentials not found, attempting to generate new ones')
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
            credentials = flow.run_local_server(port=0)

            # Save the credentials for the next run and skip web auth
            if save_json:
                credentials_json.write(credentials.to_json())
            return credentials
        except ValueError as err:
            logger.error(f'Error processing credentials: {err}', exc_info=True)
            return None
        except Exception as err:
            logger.critical(f'Unknown error: {err.args}', exc_info=True)
    except google.auth.exceptions.RefreshError as err:
        logger.error(f'Error refreshing credentials: {err.args[1].get("error_description")}')
        return None
    except Exception as err:
        logger.critical(f'Unknown error: {err.args}', exc_info=True)

    return None

def create_logger(name: str = __file__, levels: dict = {}) -> logging.Logger:
    # Create log level
    def make_log_level(level_name: str, level_int: int) -> None:
        logging.addLevelName(level_int, level_name.upper())
        setattr(new_logger, level_name, lambda *args: new_logger.log(level_int, *args))

    new_logger = logging.getLogger(name)

    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'stderr': {
                '()': ColourFormat,
                'style': '{', 'format': '{message}',
            },
            'file': {
                'style': '{', 'format': '[{asctime}] [{levelname:8}] {message}'
            }
        },
        'handlers': {
            'stderr': {
                'class': 'logging.StreamHandler',
                'formatter': 'stderr',
                'stream': 'ext://sys.stderr',
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'file',
                'filename': options.log_file if options.log_file else '/dev/null',
                'maxBytes': 1024 * #setDefaults($Log_Size_MB 5),
                'backupCount': #setDefaults($Backup_Count 0)
            }
        },
        'loggers': {
            'root': {
                'handlers': [
                    'stderr'
                ]
            },
            name: {
                'level': 10 if options.debug else 20,
                'handlers': [
                    'stderr'
                ]
            }
        }
    }

    if options.log_file is not None:
        logging_config['loggers'][name]['handlers'].append('file')

    logging.config.dictConfig(logging_config)

    # Create custom levels
    for level in levels.items():
        make_log_level(*level)

    return new_logger


if __name__ == '__main__':
    def valid_path(path):
        parent = Path(path).parent
        if not parent.is_dir():
            print(f'{parent} is not a directory, make it?', end=' ')
            if input('y/n: ').lower()[0] == 'y':
                parent.mkdir(parents=True, exist_ok=True)
                return Path(path)
            raise argparse.ArgumentTypeError(f'{path} is an invalid path')
        return Path(path)


    # Create argument parser
    parser = argparse.ArgumentParser(description=__description__)


    # Debug/verbosity option
    parser.add_argument('--debug', default=False,
                        action='store_true', dest='debug',
                        help=argparse.SUPPRESS)

    # Output
    parser.add_argument('--log', type=valid_path,
                        default=None,
                        action='store', dest='log_file',
                        help='output log')

    options = parser.parse_args()

    logger = create_logger()
    logger.debug('Debug ON')
    logger.debug(pprint.pformat(options))

    main()
