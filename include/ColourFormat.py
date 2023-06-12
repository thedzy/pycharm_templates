class ColourFormat(logging.Formatter):
    """
    Add colour to logging events
    """

    def __init__(self, fmt: str = None, datefmt: str = None, style: str = '%', levels={}) -> None:
        """
        Initialise the formatter
        ft: (str) Format String
        datefmt: (str) Date format
        style: (str) Format style
        levels: tuple, tuple (level number start, colour, attribute
        """
        self.levels = {}
        set_levels = {10: 90, 20: 92, 30: 93, 40: 91, 50: (41, 97)}
        set_levels.update(levels)

        for key in sorted(set_levels.keys()):
            value = set_levels[key]
            colour = str(value) if isinstance(value, (str, int)) else ';'.join(map(str, value))

            self.levels[key] = f'\x1b[5;{colour};m'

        super().__init__(fmt, datefmt, style)

    def formatMessage(self, record: logging.LogRecord, **kwargs: dict) -> str:
        """
        Override the formatMessage method to add colour
        """
        no_colour = u'\x1b[0m'
        for level in self.levels:
            colour = self.levels[level] if record.levelno >= level else colour

        return f'{colour}{super().formatMessage(record, **kwargs)}{no_colour}'
