import time
import pyautogui
import selenium
import pywinauto
from functools import wraps

exceptions_eligible_for_retry = (
    pywinauto.findwindows.ElementNotFoundError, 
    pywinauto.application.AppNotConnected, 
    pyautogui.ImageNotFoundException,
    selenium.common.exceptions.ElementClickInterceptedException,
    selenium.common.exceptions.TimeoutException,
 )

def retry_until_ready(timeout=30, delay=0.12):
    """
        A decorator that retries a function if window or element not found exceptions are raised.

    :param timeout: The maximum time to keep retrying in seconds.
    :param delay: The delay between retries in seconds.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions_eligible_for_retry as e:
                    current_time = time.time()
                    if current_time - start_time > timeout:
                        print(f"Timeout: Failed after {timeout} seconds. Last error: {e}")
                        raise e
                    time.sleep(delay)
                except Exception as e:
                    # This catches any other exceptions and stops retrying
                    _print_full_qualified_path(e)
                    print(f"An unexpected error occurred: {e}")
                    break
                
        return wrapper
    return decorator

def _print_full_qualified_path(e):
    print(f"{e.__class__.__module__}.{e.__class__.__name__}")
