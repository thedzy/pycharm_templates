## Pycharm Templates

### My pycharm templates using Apache Velcoity

# WARNING: Bugs in pycharm
## Bugs in pycharm:
### This took some figuring out why things break in weird ways when making updates
1. Pycharm is caching in memory the macros, so if you change the macros you need to restart pycharm or rename the macros
2. Leading indents in the macros cause indentation errors in the generated code, but NOT necessarily where the macro runs

### blank:

Setup a basic python script with:
- Logging, with colour output and log rotation

![New Doc](media/blank.png)
```python
#!/usr/bin/env python3

__author__ = 'Shane Young'
__version__ = '1.0'
__email__ = 'thedzy@thedzy.com'
__date__ = '2023-01-01'
__credits__ = ''

__description__ = \
    """
    Filename.py: 
    This is a new file that will do cool stuff
    """

import argparse
import logging
from logging.handlers import RotatingFileHandler
import pprint
from pathlib import Path
import json
import csv
import shutil


class ColourFormat(logging.Formatter):
    ...


def main() -> None:
    logger.note('Start')

    # Messages
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warn message')
    logger.error('Error message')
    logger.critical('Critical message')

    # TODO: Code

    logger.note('Done')


def create_logger(name: str = __file__, levels: dict = {}) -> logging.Logger:
    ...


if __name__ == '__main__':
    ...


```
### blank_aws_1:

Setup a python script to access a aws account with:
- Boto3, command line parameters to choose account and regions
- Logging, with colour output and log rotation

![New Doc](media/blank_aws.png)

### blank_aws_2:

Setup a python script to access multiple aws accounts with:
- Boto3, command line parameters to choose accounts and regions
- Logging, with colour output and log rotation

![New Doc](media/blank_aws.png)
```python
#!/usr/bin/env python3

__author__ = 'Shane Young'
__version__ = '1.0'
__email__ = 'thedzy@thedzy.com'
__date__ = '2023-01-01'
__credits__ = ''

__description__ = \
    """
    Filename.py: 
    This is a new file that will do cool stuff
    """

import argparse
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import pprint
import json
import csv
import shutil

import boto3 as aws
import botocore


class ColourFormat(logging.Formatter):
    ...


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
            ec2 = session.client('ec2', region_name=region)
            s3 = session.client('s3', region_name=region)
            logs = session.client('logs', region_name=region)

            # TODO: code

        except botocore.exceptions.NoCredentialsError:
            logger.error(f'No credentials for {options.profile}')
            return
        except ec2.exceptions.ClientError as err:
            logger.error(f'Error : ec2 {err}')
            return
        except s3.exceptions.ClientError as err:
            logger.error(f'Error : s3 {err}')
            return
        except logs.exceptions.ClientError as err:
            logger.error(f'Error : logs {err}')
            return
        except KeyboardInterrupt:
            logger.critical('Operation cancelled by user')
            logger.debug('Exception information:', exc_info=True)

    logger.info('Done')


def create_logger(name: str = __file__, levels: dict = {}) -> logging.Logger:
    ...


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
                        help='region name(s) default: %(default)s')

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
```

### blank_threaded:

Setup a multithreading python script with:
- Logging, with colour output and log rotation
- Threaded function
- Progress bar

![New Doc](media/blank_multithreaded.png)
```python
#!/usr/bin/env python3

__author__ = 'Shane Young'
__version__ = '1.0'
__email__ = 'thedzy@thedzy.com'
__date__ = '2023-06-15'
__credits__ = ''

__description__ = \
    """
    Filename.py: 
    This is a new file that will do cool stuff
    """

import argparse
import collections
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import pprint
import random
import threading
import time
from typing import Optional
import json
import csv
import shutil


class ThreadManager:
    ...

class ColourFormat(logging.Formatter):
    ...


class ProgressBar:
    ...

def main() -> None:
    logger.note('Start')

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

    logger.note('Done')


def random_sleep(thread_number, low, high):
    # Let's create a function to spend time
    timer_sleep = random.uniform(low, high)
    time.sleep(timer_sleep)

    return thread_number, timer_sleep


def create_logger(name: str = __file__, levels: dict = {}) -> logging.Logger:
    ...

if __name__ == '__main__':
    ...

```

## How to use:

Add the files and the includes into your pycharm templates directory

![Tempaltes](media/templates.png)
![Includes](media/includes.png)


## Versions:

- Version 1.1 \
After regaining my mind on why macros do not always do what you think they should, I either corrected them or restored them \
The biggest update is this readme, see the warning above.  I will try to locate this bug report...and since I am writing this...\
This looks like it: [https://youtrack.jetbrains.com/issue/PY-44984](https://youtrack.jetbrains.com/issue/PY-44984)\
Wish I found this much sooner
Assuming a bug report for the weird indents...