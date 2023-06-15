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
#foreach($include in $Includes.split(","))
#if(($include) && ($include != ""))
import $include
#end
#end


#parse("ThreadManager")

#parse("ColourFormat")

#parse("ProgressBar")

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
