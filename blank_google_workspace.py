#!/usr/bin/env python3

__author__ = 'Shane Young'
__version__ = '1.0'
__email__ = 'thedzy@thedzy.com'
__date__ = '${YEAR}-${MONTH}-${DAY}'
__credits__ = ''

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
import logging
from logging.handlers import RotatingFileHandler
import pprint
from pathlib import Path
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


#parse("ColourFormat")


def main() -> None:
    logger.note('Start')

    scopes = [
#set($scope = "starting value so your not prompted")
#foreach($scope in $Scopes.split(","))
        'https://www.googleapis.com/auth/$scope.trim()',
#end
    ]
    credentials = auth_google(scopes, options.google_credentials, False)
    if not credentials:
        logger.critical('Unable to authenticate')
        exit(1)

    # Create the Google Sheets APIs
#set($service = "starting value so your not prompted")
#set($service_data[0] = "starting value so your not prompted")
#set($service_data[1] = "starting value so your not prompted")
#foreach($service in $Services.split(","))
#set($service_data = $service.split("/"))
#if($service_data.size() > 1)
    $service_data[1] = build('$service_data[1].trim()', '$service_data[0].trim()', credentials=credentials)
#end
#end

    logger.note('Done')


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
    """
    Create a logger
    :param name: (str) Name of logger
    :param levels: (dict) Custom log levels
    :return: (logging.Logger) Logger
    """

    # Create log level
    def make_log_level(level_name: str, level_int: int) -> None:
        logging.addLevelName(level_int, level_name.upper())
        setattr(new_logger, level_name, lambda *args: new_logger.log(level_int, *args))

    # Setup logging
    new_logger = logging.getLogger(name)
    new_logger.setLevel(options.debug)

    # Create stream handler
    log_stream_handle = logging.StreamHandler()
    log_format = '[{asctime}] [{levelname:8}] {message}'
    log_stream_handle.setFormatter(ColourFormat('{message}', style='{', levels={20: 16, 21: 92}))
    new_logger.addHandler(log_stream_handle)

    # Set file handler
    if options.output:
        log_size_mb = #setDefaults($Log_Size_MB 5)
        log_size = log_size_mb * 1024 * 1024
        log_file_handle = RotatingFileHandler(options.output,
                                              maxBytes=log_size,
                                              backupCount=#setDefaults($Backup_Count 0)
                                              )
        log_file_handle.setFormatter(logging.Formatter(log_format, style='{'))
        new_logger.addHandler(log_file_handle)

    # Create custom levels
    for level in levels.items():
        make_log_level(*level)

    return new_logger

if __name__ == '__main__':
    def valid_path(path):
        parent = Path(path).parent
        if not parent.is_dir():
            print(f'{parent} is not a directory, make it?')
            if input('y/n: ').lower() == 'y':
                parent.mkdir(parents=True, exist_ok=True)
                Path(path)
            raise argparse.ArgumentTypeError(f'{path} is not a directory')
        return Path(path)


    # Create argument parser
    parser = argparse.ArgumentParser(description=__description__)

    # Google Workspaces auth
    parser.add_argument('-g', '--google-credentials', type=argparse.FileType('r+'),
                        action='store', dest='google_credentials',
                        required=True,
                        help='path to Google Workspaces credentials file (json)')

    parser.add_argument('--save-creds', default=False,
                        action='store_true', dest='save_credentials',
                        required=True,
                        help='save credentials with token and scope')

    # Debug option
    parser.add_argument('--debug', default=20,
                        action='store_const', dest='debug', const=10,
                        help=argparse.SUPPRESS)

    # Output
    parser.add_argument('-o', '--output', type=valid_path,
                        default=Path('/tmp').joinpath(Path(__file__).stem).with_suffix('.log'),
                        action='store', dest='output',
                        help='output log')

    options = parser.parse_args()

    logger = create_logger(levels={'note': 21})
    logger.debug('Debug ON')
    logger.debug(pprint.pformat(options))

    main()
