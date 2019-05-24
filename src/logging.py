import logging
from time import time
from colorama import Fore, Style
from typing import Callable, Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create console handler and set level to info
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


def with_logging(func: Callable) -> Callable:

    """
    Decorator used for logging functions execution
    :param func: function to decorate
    """

    def wrapper(*args, **kwargs) -> Any:
        logger.info(f'{Fore.YELLOW}Running: {func.__name__}{Style.RESET_ALL}')
        ts = time()
        try:
            result = func(*args, **kwargs)
            te = time()
            logger.info(f'{Fore.GREEN}Completed: {func.__name__}' + f' in {te-ts:.3f} sec{Style.RESET_ALL}')
            return result
        except Exception as e:
            te = time()
            logger.error(f'{Fore.RED}{type(e).__name__} raised during execution of function: {func.__name__}'
                         + f' in {te-ts:.3f} sec,'
                         + f' args: {e.args}{Style.RESET_ALL}')

    return wrapper
