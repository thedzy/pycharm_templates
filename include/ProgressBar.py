class ProgressBar:
    """
    Create progress bar
    v1.1 Fixed colours
    """

    def __init__(self, max_size: int = 100, title: str = '',
                 foreground_rgb: tuple = (0.9, 0.9, 0.9), background_rgb: tuple = (0.1, 0.1, 0.1),
                 light_rgb: tuple = (1.0, 1.0, 1.0), dark_rgb: tuple = (0.0, 0.0, 0.0),
                 invert: bool = False, columns: Optional[int] = None,
                 wait_pattern=' ◢◤ ', wait_speed=0.2) -> None:
        """
        Initialise the progress bar
        :param max_size: (int) Maximum size
        :param title: (str) Title
        :param foreground_rgb: (tuple) Foreground RGB
        :param background_rgb: (tuple) Background RGB
        :param light_rgb: (tuple) Light text RGB
        :param dark_rgb: (tuple) Dark text RGB
        :param invert: (bool) Use the background colour for the foreground text, vis a versa
        :param columns: (int) Width of the progress bar
        """
        self.__position = 0
        self.max_size = max_size
        self.title = title

        self.__wait_position = 0
        self.__wait_pattern = wait_pattern
        self.__wait_position_len = len(wait_pattern)
        self.__wait_speed = wait_speed

        # Initialise the colours
        self.__background = None
        self.__foreground = None
        self.__foreground_text = None
        self.__background_text = None

        # Store the colours
        self.__foreground_rgb = foreground_rgb
        self.__background_rgb = background_rgb
        self.__light_rgb = light_rgb
        self.__dark_rgb = dark_rgb

        # Invert
        self.__invert = invert

        # Set the colours
        self.foreground = foreground_rgb
        self.background = background_rgb
        self.light = light_rgb
        self.dark = dark_rgb

        # Set the size of the bar
        if columns is None:
            try:
                self.columns, _ = os.get_terminal_size()
            except (OSError, NameError):
                # Catch error if not in terminal or os is not supported/imported
                self.columns = 100
        else:
            self.columns = columns

        # Get width and fill size
        self.item_of_len = len(str(max_size))
        percent_padding, side_padding, len_of_padding = 4, 2, (self.item_of_len * 2) + 1
        self.progress_width = self.columns - percent_padding - side_padding - len_of_padding

        self.draw(self.__position, title)

    def __del__(self):
        """
        Clear the progress bar
        """
        # Clear the bar
        print(' ' * self.columns, end='\r')
        return

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()

    def __calculate_text_colour(self):
        light, dark = (
            self.get_colour(*self.__dark_rgb), self.get_colour(*self.__light_rgb))

        self.__foreground_text = light if self.colour_contrast(*self.__foreground_rgb) > 0.5 else dark
        self.__background_text = light if self.colour_contrast(*self.__background_rgb) > 0.5 else dark

    @property
    def foreground(self) -> tuple:
        """
        Get the foreground colour
        :return: (tuple)
        """
        return self.__foreground_rgb

    @foreground.setter
    def foreground(self, rgb: tuple) -> None:
        """
        Set the foreground colour
        :param rgb: (tuple)
        :return: (tuple)
        """
        self.__foreground_rgb = rgb
        self.__foreground = self.get_colour(*self.__foreground_rgb)
        self.__calculate_text_colour()

    @property
    def background(self) -> tuple:
        """
        Get the background colour
        :return: (tuple)
        """
        return self.__background_rgb

    @background.setter
    def background(self, rgb: tuple) -> None:
        """
        Set the background colour
        :param rgb: (tuple)
        :return: (tuple)
        """
        self.__background_rgb = rgb
        self.__background = self.get_colour(*self.__background_rgb)
        self.__calculate_text_colour()

    @property
    def width(self) -> int:
        """
        Get the progress width
        :return: (int)
        """
        return self.columns

    @property
    def invert(self) -> bool:
        """
        Get the invert
        :return: (bool)
        """
        return self.__invert

    @invert.setter
    def invert(self, enabled: bool = True) -> None:
        """
        Set the invert
        :return: (bool)
        """
        self.__invert = enabled
        self.__calculate_text_colour()

    @property
    def light_rgb(self) -> tuple:
        """
        Get the light colour
        :return: (tuple)
        """
        return self.__light_rgb

    @light_rgb.setter
    def light_rgb(self, rgb: tuple) -> None:
        """
        Set the light colour
        :param rgb: (tuple)
        :return: (tuple)
        """
        self.__light_rgb = rgb
        self.__light = self.get_colour(*self.__light_rgb)
        self.__calculate_text_colour()

    @property
    def dark_rgb(self) -> tuple:
        """
        Get the dark colour
        :return: (tuple)
        """
        return self.__dark_rgb

    @dark_rgb.setter
    def dark_rgb(self, rgb: tuple) -> None:
        """
        Set the dark colour
        :param rgb: (tuple)
        :return: (tuple)
        """
        self.__dark_rgb = rgb
        self.__dark = self.get_colour(*self.__dark_rgb)

        self.__calculate_text_colour()

    def draw(self, position: int = 0, title: str = ''):
        """
        Draw the bar
        :param position: (int) Position of the bar
        :param title: (str) Title of the bar
        :return:
        """
        self.__position = position
        self.title = title

        # Get the text for "item of items"
        item_of = f'{position:{self.item_of_len}}/{self.max_size:{self.item_of_len}}'

        # Get fill position
        progress_filled = int(position * self.columns / self.max_size)

        # Trim title if too long and format
        if len(title) > self.progress_width:
            title = f'...{title[-self.progress_width + 5:]}'

        # Get fill
        progress_text = f'▏{item_of} {title.ljust(self.progress_width - 2)} {position / self.max_size * 100:3.0f}%▕'
        fill = progress_text[0:progress_filled]
        empty = progress_text[progress_filled:self.columns]

        if self.__invert:
            foreground_text = self.__background
            background_text = self.__foreground
        else:
            foreground_text = self.__foreground_text
            background_text = self.__background_text

        # Print
        print(
            f'\033[48;5;{foreground_text}m\033[38;7m\033[38;5;{self.__foreground:0.0f}m{fill}\033[48;5;{background_text}m\033[38;5;{self.__background:0.0f}m{empty}\033[0m',
            end='\r',
            flush=True)

    def wait(self, title: Optional[str] = None, wait_pattern: Optional[str] = None, left2right: bool = True) -> None:
        """
        Draw a progress bar to the width of the screen
        :param title: (str) Title at the beginning of the progress
        :param wait_pattern: (str) Pattern to repeat
        :param left2right: (bool) Movement for left r=to right
        :return: (void)
        """
        self.__wait_position += 1
        title = self.title if title is None else title

        wait_pattern = self.__wait_pattern if wait_pattern is None else wait_pattern
        wait_pattern_len = self.__wait_position_len if wait_pattern is None else len(wait_pattern)

        columns = self.columns - len(title) - 2

        # Calculate for direction
        if left2right:
            start = wait_pattern_len - (self.__wait_position % wait_pattern_len)
        else:
            start = self.__wait_position % wait_pattern_len

        # Repeat pattern
        text = f'{wait_pattern[start:]}{wait_pattern[:start]}' * columns

        # Print
        time.sleep(self.__wait_speed)
        print(f'\033[0m{title}\033[0m\033[38;5;{self.__foreground}m▕\033[48;5;{self.__background:0.0f}m{text[:columns]}\033[0m\033[38;5;{self.__foreground}m▏\033[0m', end='\r', flush=True)

    def increment(self, increment: int = 1, title: Optional[str] = None):
        """
        Increment the progress bar
        :param increment: (int) Increment
        :param title: (str) Title
        """
        self.__position += increment
        self.draw(self.__position, title if title else self.title)

    @staticmethod
    def get_colour(red: float, green: float, blue: float) -> int:
        """
        Calculate ansi code for rgb
        :param red: (float) 0-1 Red
        :param green: (float) 0-1 Green
        :param blue: (float) 0-1 Blue
        :return: (int) 0-255 Ansi code
        """
        grey_shades = 23
        if int(red * grey_shades) == int(green * grey_shades) == int(blue * grey_shades):
            # If colour is shade of grey
            ansi_code = 232 + (int(red * grey_shades))
        else:
            # If colour
            ansi_code = 16 + (36 * int(red * 5)) + (6 * int(green * 5)) + int(blue * 5)

        return ansi_code

    @staticmethod
    def colour_contrast(red: float, green: float, blue: float) -> float:
        """
        Get the perceived brightness of a colour
        :param red: (float) 0-1 Red
        :param green: (float) 0-1 Green
        :param blue: (float) 0-1 Blue
        :return: (float) 0-1 Perceived brightness
        """

        colour_value = ((red * 299) + (green * 587) + (blue * 114)) / 1000

        return colour_value
