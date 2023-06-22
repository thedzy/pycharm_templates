# Pycharm Templates

### My pycharm templates using Apache Velcoity

## blank.py:

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

__description__ =
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
