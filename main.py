import enum
import subprocess
import psutil
import time
import win32con
import pyautogui
import selenium
import pyperclip
from functools import wraps
from pywinauto.application import Application, AppNotConnected
from pywinauto.findwindows import ElementNotFoundError
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import ctypes 
from cfg import github
from cfg import apps
from cfg import urls
from cfg.vetos import vetos
from browser import Browser
from retrier import retry_until_ready
import gist


def print_full_qualified_path(e):
    print(f"{e.__class__.__module__}.{e.__class__.__name__}")

def open_app(app):
    if is_process_running(app["process"]):
        return

    startup_info = subprocess.STARTUPINFO()
    startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup_info.wShowWindow = win32con.SW_MAXIMIZE

    subprocess.Popen(app["path"], startupinfo=startup_info)   
        
    focus(app)
        

def is_running(app):
    return is_process_running(app["process"])


def is_process_running(process_name):
    for proc in psutil.process_iter(['name']):
        try:
            if process_name.lower() in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def kill(app):
    print(f"Checking if {app["window_title"]} is running, to kill it...")    
    kill_process(app["process"])

def kill_process(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            print(f"Killing process {proc.pid} - {proc.info['name']}")
            proc.kill()
            time.sleep(0.3)


def focus(app):
    focus_window(app["window_title"])
    
def focus_window(window_title):
    main_window = get_window(window_title)
    #  main_window.maximize()

    # Move the window to a visible spot
    screen_width, screen_height = main_window.client_rect().width(), main_window.client_rect().height()
    window_width, window_height = main_window.client_rect().width(), main_window.client_rect().height()
    left = (screen_width - window_width) // 2
    top = (screen_height - window_height) // 2
    main_window.move_window(left, top)

    main_window.set_focus()


def minimize(app):
    minimize_window(app["window_title"])

def minimize_window(window_title):
    get_window(window_title).minimize()

@retry_until_ready()
def get_window(window_title):
    app = Application().connect(title=window_title, found_index=0)
    return app.window(title=window_title)
        

@retry_until_ready(timeout=37)
def find(ref_img):
    box = pyautogui.locateOnScreen(ref_img_path(ref_img), grayscale=False)
    return pyautogui.center(box)  

def click(ref_img):
    x, y = find(ref_img)
    pyautogui.click(x, y)

def ref_img_path(ref_img):
    return "./imgs/" + ref_img + ".png"

def set_volume_to_max():
    print("Getting default audio interface...")
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))

    print("Setting volume to max (100%)...")
    volume.SetMasterVolumeLevelScalar(1.0, None)
    volume.SetMute(0, None)


def launch_cs():
    kill(apps.cs)
    kill(apps.anticheater)

    open_app(apps.anticheater)
    click("anticheater_opencs")

def prepare_voicemeeter():
    print("Preparing VoiceMeter...")
    kill(apps.voicemeeter_macro_buttons)
    kill(apps.voicemeeter)
    open_app(apps.voicemeeter)
    
    
def copy_lobby_link_button():
    return Browser.lookup().css("#lobby-copy-trigger")
    
def is_on_lobby():
    return copy_lobby_link_button().exists()

def veto_maps():
    print("Clearing vetos...")
    Browser.lookupAll().css(".MapPreVetoContent__container--vetoed").click()
    
    print("Vetoing maps:")
    for veto in vetos:
        print(f" - {veto}")
        Browser.lookup().text(veto).click()
        

def create_lobby():
    Browser.lookup().css("#lobby-actions-create-lobby-button").click()
    
      
    print("Seting lobby to Private")
    Browser.lookup().text("Privada").click()

    print("Allowing unverified players to join lobby...")
    css_for_unverified_players_button = ".PlayersType__container__checkButton > div:nth-child(1) > button:nth-child(1)"    
    Browser.lookup().css(css_for_unverified_players_button).click()

    veto_maps()
    
    print("Unchecking the option to save lobby configs...")
    Browser.lookup().text("Salvar configurações para a sua próxima lobby").click()
    
    Browser.lookup().button_or_link_with_text("Criar Sala").click()

def share_with_friends(message):
    gist.update(github.access_token, github.gist_id, github.gist_filename, message)
    

    

def share_lobby():
    set_volume_to_max()
    
    if not is_running(apps.cs):
        prepare_voicemeeter()
        launch_cs()
        time.sleep(5) # to prevent crosshair overlay bug when CS is minimized too fast
    
    minimize(apps.cs)

    kill(apps.browser)
    Browser.visit(urls.lobby)
    
    if not is_on_lobby():
        create_lobby()
        
    copy_lobby_link_button().click()
    share_with_friends(pyperclip.paste())


    

share_lobby()

