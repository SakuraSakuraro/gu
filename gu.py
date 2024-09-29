from PIL import Image, ImageTk
import tkinter as tk
import tkinter.constants as tkconstants
import os
import sys
import winreg
import requests
from tzlocal import get_localzone

# Check the registry settings
def check_registry():
    try:
        # Get Nation values
        geo_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\International\Geo")
        nation, _ = winreg.QueryValueEx(geo_key, "Nation")
        winreg.CloseKey(geo_key)

        # Get iCountry, Locale, LocaleName, sLanguage values
        intl_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\International")
        iCountry, _ = winreg.QueryValueEx(intl_key, "iCountry")
        locale, _ = winreg.QueryValueEx(intl_key, "Locale")
        locale_name, _ = winreg.QueryValueEx(intl_key, "LocaleName")
        sLanguage, _ = winreg.QueryValueEx(intl_key, "sLanguage")
        winreg.CloseKey(intl_key)

        # Chaeck values
        if nation == "203" or iCountry == "7" or locale == "00000419" or locale_name == "ru-RU" or sLanguage == "RUS":
            return True
    except:
        pass
    return False

# Check time zone
def check_timezone():
    try:
        timezones = [
            'Asia/Anadyr', 'Asia/Barnaul', 'Asia/Chita', 'Asia/Irkutsk', 'Asia/Kamchatka',
            'Asia/Khandyga', 'Asia/Krasnoyarsk', 'Asia/Magadan', 'Asia/Novokuznetsk', 'Asia/Novosibirsk',
            'Asia/Omsk', 'Asia/Sakhalin', 'Asia/Srednekolymsk', 'Asia/Tomsk', 'Asia/Ust-Nera',
            'Asia/Vladivostok', 'Asia/Yakutsk', 'Asia/Yekaterinburg', 'Europe/Astrakhan', 'Europe/Kaliningrad',
            'Europe/Kirov', 'Europe/Moscow', 'Europe/Saratov', 'Europe/Simferopol', 'Europe/Ulyanovsk', 
            'Europe/Volgograd'
        ]

        local_tz = str(get_localzone())  # Get current time zone
        if local_tz in timezones:
            return True
    except:
        pass
    return False

# Send requests to ipapi.co
def check_location():
    try:
        response = requests.get("https://ipapi.co/json/", timeout=10)
        data = response.json()

        if (data['country_name'] == 'Russia' and 
            data['country_code'] == 'RU' and 
            data['timezone'] in [
                'Asia/Anadyr', 'Asia/Barnaul', 'Asia/Chita', 'Asia/Irkutsk', 'Asia/Kamchatka',
                'Asia/Khandyga', 'Asia/Krasnoyarsk', 'Asia/Magadan', 'Asia/Novokuznetsk', 'Asia/Novosibirsk',
                'Asia/Omsk', 'Asia/Sakhalin', 'Asia/Srednekolymsk', 'Asia/Tomsk', 'Asia/Ust-Nera',
                'Asia/Vladivostok', 'Asia/Yakutsk', 'Asia/Yekaterinburg', 'Europe/Astrakhan', 
                'Europe/Kaliningrad', 'Europe/Kirov', 'Europe/Moscow', 'Europe/Saratov', 'Europe/Simferopol', 
                'Europe/Ulyanovsk', 'Europe/Volgograd']):
            return True
    except:
        pass
    return False

# Get path to image
def get_image_path(filename):
    # Get the path to the directory where the executable file is located
    if getattr(sys, 'frozen', False):
        # If is run as a .exe
        return os.path.join(sys._MEIPASS, filename)
    else:
        # If is run as a source code
        return os.path.join(os.path.dirname(__file__), filename)

# Show image in full screen mode
def show_image_fullscreen():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.protocol("WM_DELETE_WINDOW", lambda: None)  # Block window closing
    root.title("Glory to Ukraine!")
    
    icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'icon.ico'))
    root.iconbitmap(icon_path)

    image_path = get_image_path("image.jpeg")
    image = Image.open(image_path)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    image_resized = image.resize((screen_width, screen_height), Image.LANCZOS)
    tk_image = ImageTk.PhotoImage(image_resized)

    label = tk.Label(root, image=tk_image)
    label.pack()

    root.mainloop()

# Show image in windowed mode
def show_image_windowed():
    root = tk.Tk()
    root.attributes('-fullscreen', False)
    root.resizable(tkconstants.FALSE, tkconstants.FALSE)
    root.title("Glory to Ukraine!")
    
    icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'icon.ico'))
    root.iconbitmap(icon_path)

    image_path = get_image_path("image.jpeg")
    image = Image.open(image_path)
    
    # Resized image to 500x314
    image_resized = image.resize((500, 314), Image.LANCZOS)
    tk_image = ImageTk.PhotoImage(image_resized)

    label = tk.Label(root, image=tk_image)
    label.pack()

    root.mainloop()

# Basic logic: check all conditions and decide how to display the image
if check_registry() or check_timezone() or check_location():
    show_image_fullscreen()
else:
    show_image_windowed()  # If none of the conditions are met, show thumbnail image