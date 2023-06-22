# Pycharm Templates

### My pycharm templates using Apache Velcoity

## blank_threaded.py:

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

__description__ =
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
