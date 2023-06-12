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

#set($param = "starting value so your not prompted with variable")
#set($value = "starting value so your not prompted with variable")
#macro(defaultValue $param $value)
#if ($param != "")
$value
#else
$param
#end
#end

import argparse
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import pprint
#foreach($include in $Includes.split(","))
#if(($include) && ($include != ""))
import $include
#end
#end

import boto3 as aws
import botocore



#parse("ColourFormat")


def main() -> None:
    logger.info('Start')

    # Create session
    session = aws.Session(
        profile_name=options.profile
    )

    for region in options.regions:
        # Verify that we have credentials
        if not session.get_credentials():
            logger.error(f'No credentials for {options.profile}')
            exit()

        try:
            logger.info(f'Processing {region} for profile {options.profile}:')

            # Create clients
#set($asset = "starting value so your not prompted with include")
#foreach($asset in $Assets.split(","))
#set($asset = $asset.trim())
#if(($asset) && ($asset != ""))
            $asset = session.client('${asset}', region_name=region)
#end
#end

            # TODO: code

        except botocore.exceptions.NoCredentialsError:
            logger.error(f'No credentials for {options.profile}')
            return
#foreach($asset in $Assets.split(","))
#set($asset = $asset.trim())
#if(($asset) && ($asset != ""))
        except ${asset}.exceptions.ClientError as err:
            logger.error(f'Error : $asset {err}')
            return
#end
#end
        except KeyboardInterrupt:
            logger.critical('Operation cancelled by user')
            logger.debug('Exception information:', exc_info=True)

    logger.info('Done')


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
        log_size_mb = #defaultValue($Log_Size_MB 5)
        log_size = log_size_mb * 1024 * 1024
        log_file_handle = RotatingFileHandler(options.output,
                                              maxBytes=log_size,
                                              backupCount=#defaultValue($Backup_Count 0)
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

    # Instances
    parser.add_argument('-p', '--profile', default='default',
                        action='store', dest='profile', choices=aws.session.Session().available_profiles,
                        metavar='NAME',
                        help='profile name, '
                             'Choices: %(choices)s')

    # Region
    parser.add_argument('-r', '--regions', default=['us-west-2'], nargs=argparse.ONE_OR_MORE,
                        action='store', dest='regions', choices=aws.session.Session().get_available_regions('ec2'),
                        metavar='NAME',
                        help='region name(s)')

    # Debug option
    parser.add_argument('--debug', default=20,
                        action='store_const', dest='debug', const=10,
                        help=argparse.SUPPRESS)

    # Output
    parser.add_argument('-o', '--output', type=valid_path, default=None,
                        action='store', dest='output',
                        help='output log')

    options = parser.parse_args()

    logger = create_logger(levels={'note': 21})
    logger.debug('Debug ON')
    logger.debug(pprint.pformat(options))

    main()

