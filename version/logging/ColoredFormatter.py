import logging


class ColoredFormatter(logging.Formatter):
    """
    ColoredFormatter for logging
    """
    LEVEL_MAP = {logging.FATAL: 'F', logging.ERROR: 'E', logging.WARN: 'W', logging.INFO: 'I', logging.DEBUG: 'D'}
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
    COLORS = {
        'WARNING': YELLOW,
        'INFO': WHITE,
        'DEBUG': BLUE,
        'CRITICAL': YELLOW,
        'ERROR': RED,
        'OK': GREEN
    }
    RESET_SEQ = "\033[0m"
    COLOR_SEQ = "\033[1;%dm"
    BOLD_SEQ = "\033[1m"

    def __init__(self, fmt: str, datefmt: str, use_color: bool=True) -> None:
        """
        Constructor
        :param fmt: Message format
        :param datefmt: datetime format
        :param use_color: use colors
        """
        logging.Formatter.__init__(self, fmt, datefmt)
        self.use_color = use_color

    def format(self, record: logging.LogRecord) -> str:
        levelname = record.levelname
        if self.use_color and levelname in self.COLORS:
            levelname_color = self.COLOR_SEQ % (30 + self.COLORS[levelname]) + levelname + self.RESET_SEQ
            record.levelname = levelname_color
            record.levelletter = self.LEVEL_MAP[record.levelno]
        return logging.Formatter.format(self, record)
