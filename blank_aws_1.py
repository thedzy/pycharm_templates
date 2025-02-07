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
import logging.config
import pprint
from pathlib import Path
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
                        help='region name(s) default: %(default)s')

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

