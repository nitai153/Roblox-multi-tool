import sys, os, subprocess, time, platform, shutil, webbrowser
from datetime import datetime

required_packages = ['selenium', 'requests', 'colorama']
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, init
init(autoreset=True)
PURPLE = Fore.MAGENTA
RESET = Fore.RESET

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_main_ascii():
    ascii_art = f"""
{PURPLE}   _____       _     _           
 |  __ \     | |   | |          
 | |__) |___ | |__ | | _____  __
 |  _  // _ \| '_ \| |/ _ \ \/ /
 | | \ \ (_) | |_) | | (_) >  < 
 |_|  \_\___/|_.__/|_|\___/_/\_\\{RESET}
"""
    print(ascii_art)

def get_desktop_path():
    if platform.system() == "Windows":
        userprofile = os.environ.get("USERPROFILE", "")
        if not userprofile:
            return os.path.join(os.path.expanduser("~"), "Desktop")
        onedrive = os.path.join(userprofile, "OneDrive", "Desktop")
        standard = os.path.join(userprofile, "Desktop")
        return onedrive if os.path.exists(onedrive) else standard
    else:
        return os.path.join(os.path.expanduser("~"), "Desktop")

def repair_folders():
    desktop = get_desktop_path()
    main_folder = os.path.join(desktop, "Roblox multi tool")
    account_gen_folder = os.path.join(main_folder, "Account generator")
    cookies_folder = os.path.join(account_gen_folder, "Cookies")
    for folder in [main_folder, account_gen_folder, cookies_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
    return main_folder, account_gen_folder, cookies_folder

def ensure_installed_location():

    script_path = os.path.abspath(__file__)
    desktop = get_desktop_path()
    main_folder = os.path.join(desktop, "Roblox multi tool")
    account_gen_folder = os.path.join(main_folder, "Account generator")
    cookies_folder = os.path.join(account_gen_folder, "Cookies")
    repair_folders()  

    if os.path.normcase(os.path.dirname(script_path)) != os.path.normcase(main_folder):
        print(f"\n{PURPLE}--- Installing Roblox Multi Tool ---{RESET}")
        print(f"{PURPLE}Installing to: {main_folder}{RESET}\n")
        try:
            shutil.move(script_path, os.path.join(main_folder, os.path.basename(script_path)))
            print(f"{PURPLE}Moved script to: {os.path.join(main_folder, os.path.basename(script_path))}{RESET}")
        except Exception as e:
            print(f"{PURPLE}Failed to move script: {e}{RESET}")
            input(f"{PURPLE}Press Enter to exit...{RESET}")
            sys.exit(1)
        print(f"\n{PURPLE}Re-launching from the new folder...{RESET}\n")
        try:
            subprocess.Popen([sys.executable, os.path.join(main_folder, os.path.basename(script_path))])
        except Exception as e:
            print(f"{PURPLE}Failed to re-launch script: {e}{RESET}")
        sys.exit(0)

def get_default_cookie():
    _, _, cookies_folder = repair_folders()
    default_cookie_path = os.path.join(cookies_folder, "default_cookie.txt")
    if os.path.exists(default_cookie_path):
        with open(default_cookie_path, "r") as f:
            return f.read().strip()
    return None

def set_default_cookie(cookie_value):
    _, _, cookies_folder = repair_folders()
    default_cookie_path = os.path.join(cookies_folder, "default_cookie.txt")
    with open(default_cookie_path, "w") as f:
        f.write(cookie_value.strip())

def remove_default_cookie():
    _, _, cookies_folder = repair_folders()
    default_cookie_path = os.path.join(cookies_folder, "default_cookie.txt")
    if os.path.exists(default_cookie_path):
        os.remove(default_cookie_path)

def change_cookie_from_folder():
    clear_screen()
    _, _, cookies_folder = repair_folders()
    cookie_files = [f for f in os.listdir(cookies_folder) if f.endswith(".txt") and f != "default_cookie.txt"]
    if not cookie_files:
        print(f"{PURPLE}No cookie files found in Cookies folder.{RESET}")
        time.sleep(2)
        return
    print(f"{PURPLE}Select a cookie file to set as default:{RESET}")
    for idx, f in enumerate(cookie_files, 1):
        print(f"{PURPLE}{idx} - {f}{RESET}")
    choice = input(f"{PURPLE}Enter your choice (0 to cancel): {RESET}")
    clear_screen()
    if choice.isdigit():
        idx = int(choice)
        if idx == 0:
            return
        if 1 <= idx <= len(cookie_files):
            selected_file = cookie_files[idx-1]
            path = os.path.join(cookies_folder, selected_file)
            with open(path, "r") as f:
                cookie_value = f.read().strip()
            set_default_cookie(cookie_value)
            print(f"{PURPLE}Default cookie updated from {selected_file}.{RESET}")
            time.sleep(2)

def is_cookie_valid():
    cookie = get_default_cookie()
    if not cookie:
        return False
    headers = get_headers()
    try:
        response = requests.get("https://users.roblox.com/v1/users/authenticated", headers=headers)
        if response.status_code == 200 and "id" in response.json():
            return True
    except Exception:
        pass
    return False

def get_headers():
    cookie = get_default_cookie()
    return {
        "Cookie": f".ROBLOSECURITY={cookie if cookie else ''}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

def manage_cookie_menu():
    while True:
        clear_screen()
        current_cookie = get_default_cookie()
        valid = is_cookie_valid() if current_cookie else False
        print(f"{PURPLE}Manage Cookie Menu:{RESET}")
        if current_cookie:
            if valid:
                print(f"{PURPLE}Current default cookie is valid.{RESET}")
            else:
                print(f"{PURPLE}Current default cookie is invalid.{RESET}")
        else:
            print(f"{PURPLE}No default cookie found.{RESET}")
        print(f"{PURPLE}1) {'Change' if current_cookie else 'Add'} Cookie (Manual Input){RESET}")
        print(f"{PURPLE}2) Add/Change Cookie from Cookies Folder{RESET}")
        if current_cookie:
            print(f"{PURPLE}3) Remove Cookie{RESET}")
        print(f"{PURPLE}0) Back to Main Menu{RESET}")
        choice = input(f"{PURPLE}Enter your choice: {RESET}")
        if choice == "0":
            break
        clear_screen()
        if choice == "1":
            new_cookie = input(f"{PURPLE}Enter cookie value: {RESET}").strip()
            set_default_cookie(new_cookie)
            print(f"{PURPLE}Cookie updated.{RESET}")
            time.sleep(2)
        elif choice == "2":
            change_cookie_from_folder()
        elif choice == "3" and current_cookie:
            remove_default_cookie()
            print(f"{PURPLE}Cookie removed.{RESET}")
            time.sleep(2)
        else:
            print(f"{PURPLE}Invalid choice, try again.{RESET}")
            time.sleep(1)

def generate_username(length=9):
    import random, string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_password(length=12):
    import random, string
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choices(chars, k=length))

def create_account():
    clear_screen()
    print(f"{PURPLE}Creating a new Roblox account...{RESET}\n")
    username = generate_username()
    password = generate_password()
    try:
        driver = webdriver.Chrome()
    except Exception as e:
        print(f"{PURPLE}Error launching Chrome WebDriver: {e}{RESET}")
        input(f"{PURPLE}Press Enter to return to the menu...{RESET}")
        return
    wait = WebDriverWait(driver, 10)
    try:
        driver.get("https://www.roblox.com/CreateAccount")
        wait.until(EC.element_to_be_clickable((By.ID, "signup-username"))).send_keys(username)
        driver.find_element(By.ID, "signup-password").send_keys(password)
        month_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "MonthDropdown")))
        Select(month_dropdown).select_by_value("Mar")
        driver.find_element(By.ID, "DayDropdown").send_keys("15")
        driver.find_element(By.ID, "YearDropdown").send_keys("2002")
        wait.until(EC.element_to_be_clickable((By.ID, "MaleButton"))).click()
        wait.until(EC.element_to_be_clickable((By.ID, "signup-button"))).click()

        while True:
            if "roblox.com/home" in driver.current_url:
                print(f"{PURPLE}Successfully redirected to roblox.com/home!{RESET}")
                break
            time.sleep(2)
        cookie = driver.get_cookie(".ROBLOSECURITY")

        _, account_gen_folder, cookies_folder = repair_folders()
        if cookie:
            os.makedirs(cookies_folder, exist_ok=True)
            cookie_file_path = os.path.join(cookies_folder, f"{username}.txt")
            with open(cookie_file_path, "w") as cf:
                cf.write(cookie["value"])
            print(f"\n{PURPLE}Cookie for {username} saved to: {cookie_file_path}{RESET}")
        else:
            print(f"\n{PURPLE}No .ROBLOSECURITY cookie found.{RESET}")
        print(f"{PURPLE}Generated Username: {username}{RESET}")
        print(f"{PURPLE}Generated Password: {password}{RESET}")
    except Exception as e:
        print(f"{PURPLE}An error occurred: {e}{RESET}")
    finally:
        driver.quit()
        input(f"\n{PURPLE}Press Enter to return to the Account Generator menu...{RESET}")

def view_cookies():
    clear_screen()
    _, account_gen_folder, cookies_folder = repair_folders()
    if not os.path.exists(cookies_folder):
        print(f"{PURPLE}No Cookies folder found. No accounts generated yet.{RESET}")
        input(f"\n{PURPLE}Press Enter to return...{RESET}")
        return
    files = [f for f in os.listdir(cookies_folder) if f.endswith(".txt")]
    if not files:
        print(f"{PURPLE}No cookie files found. No accounts generated yet.{RESET}")
        input(f"\n{PURPLE}Press Enter to return...{RESET}")
        return
    print(f"{PURPLE}Cookie files (each corresponds to an account):{RESET}")
    for f in files:
        print(f"{PURPLE} - {f}{RESET}")
    print(f"\n{PURPLE}Total accounts generated: {len(files)}{RESET}")
    input(f"\n{PURPLE}Press Enter to return...{RESET}")

def account_generator_menu():
    while True:
        clear_screen()
        print(f"{PURPLE}Account Generator Menu:{RESET}")
        print(f"{PURPLE}1) Generate a new account{RESET}")
        print(f"{PURPLE}2) View cookies / total accounts{RESET}")
        print(f"{PURPLE}0) Back to main menu{RESET}")
        choice = input(f"\n{PURPLE}Enter your choice: {RESET}").strip()
        if choice == "1":
            create_account()
        elif choice == "2":
            view_cookies()
        elif choice == "0":
            break
        else:
            print(f"{PURPLE}Invalid choice, please try again.{RESET}")
            time.sleep(1)

def get_user_id_info(username):
    url = "https://users.roblox.com/v1/usernames/users"
    data = {"usernames": [username], "excludeBannedUsers": False}
    response = requests.post(url, json=data)
    if response.status_code == 200 and response.json()["data"]:
        return response.json()["data"][0]["id"]
    return None

def get_user_info(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def get_friends(user_id):
    friends = []
    cursor = None
    while True:
        url = f"https://friends.roblox.com/v1/users/{user_id}/friends?limit=100&cursor={cursor or ''}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            friends.extend([(f.get("displayName", "Unknown"), f.get("name", "Unknown"), f["id"]) for f in data["data"]])
            cursor = data.get("nextPageCursor")
            if not cursor:
                break
        else:
            break
    return friends, len(friends)

def get_groups(user_id):
    url = f"https://groups.roblox.com/v1/users/{user_id}/groups/roles"
    response = requests.get(url)
    if response.status_code == 200:
        groups = response.json()["data"]
        return [(g["group"]["name"], g["role"]["name"]) for g in groups], len(groups)
    return [], 0

def get_owned_items(user_id):
    items = []
    cursor = None
    while True:
        url = f"https://inventory.roblox.com/v2/users/{user_id}/inventory/1?limit=100&cursor={cursor or ''}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            items.extend([(item.get("name", "Unknown"), item.get("assetId", "N/A")) for item in data["data"]])
            cursor = data.get("nextPageCursor")
            if not cursor:
                break
        else:
            break
    return items, len(items)

def roblox_player_info_menu():
    while True:
        clear_screen()
        username = input(f"{PURPLE}Enter Roblox Username or ID (or type 0 to return): {RESET}").strip()
        if username == "0":
            break
        clear_screen()
        print(f"{PURPLE}Getting user data...{RESET}")
        time.sleep(1)
        user_id = username if username.isdigit() else get_user_id_info(username)
        if not user_id:
            print(f"{PURPLE}Invalid username! Please try again.{RESET}")
            time.sleep(2)
            continue
        user_info = get_user_info(user_id)
        if not user_info:
            print(f"{PURPLE}Failed to get user info!{RESET}")
            time.sleep(2)
            continue
        friends, total_friends = get_friends(user_id)
        groups, total_groups = get_groups(user_id)
        owned_items, total_items = get_owned_items(user_id)
        while True:
            clear_screen()
            print(f"{PURPLE}========== ROBLOX PLAYER INFO =========={RESET}")
            print(f"{PURPLE}Username     : {user_info['name']}{RESET}")
            print(f"{PURPLE}User ID      : {user_id}{RESET}")
            print(f"{PURPLE}Created On   : {user_info.get('created', 'N/A')[:10]}{RESET}")
            print(f"{PURPLE}Description  : {user_info.get('description', 'No description')}{RESET}")
            print(f"{PURPLE}Total Friends: {total_friends}{RESET}")
            print(f"{PURPLE}Total Groups : {total_groups}{RESET}")
            print(f"{PURPLE}Total Owned Items: {total_items}{RESET}")
            print(f"\n{PURPLE}Select an option:{RESET}")
            print(f"{PURPLE}1 = View all friends{RESET}")
            print(f"{PURPLE}2 = View all groups{RESET}")
            print(f"{PURPLE}3 = View all owned items{RESET}")
            print(f"{PURPLE}0 = Go back{RESET}")
            choice = input(f"{PURPLE}Enter choice: {RESET}").strip()
            if choice == "0":
                break
            elif choice == "1":
                clear_screen()
                print(f"{PURPLE}========== FRIEND LIST =========={RESET}")
                if total_friends > 0:
                    for display_name, uname, uid in friends:
                        print(f"{PURPLE}{display_name} ({uname}) - ID: {uid}{RESET}")
                else:
                    print(f"{PURPLE}No friends found.{RESET}")
            elif choice == "2":
                clear_screen()
                print(f"{PURPLE}========== GROUP LIST =========={RESET}")
                if total_groups > 0:
                    for group_name, role in groups:
                        print(f"{PURPLE}{group_name} - Rank: {role}{RESET}")
                else:
                    print(f"{PURPLE}No groups found.{RESET}")
            elif choice == "3":
                clear_screen()
                print(f"{PURPLE}========== OWNED ITEMS =========={RESET}")
                if total_items > 0:
                    for item_name, item_id in owned_items:
                        print(f"{PURPLE}{item_name} - ID: {item_id}{RESET}")
                else:
                    print(f"{PURPLE}No items found.{RESET}")
            else:
                continue
            input(f"\n{PURPLE}Press Enter to go back to the menu.{RESET}")

def get_my_user_id_joiner():
    response = requests.get("https://users.roblox.com/v1/users/authenticated", headers=get_headers())
    if response.status_code == 200:
        return response.json().get("id")
    return None

def get_user_id_multi(username):
    response = requests.post("https://users.roblox.com/v1/usernames/users", json={"usernames": [username]}, headers=get_headers())
    if response.status_code == 200 and response.json().get("data"):
        return response.json()["data"][0]["id"]
    return None

def get_user_presence(user_id):
    response = requests.post("https://presence.roblox.com/v1/presence/users", json={"userIds": [user_id]}, headers=get_headers())
    if response.status_code == 200:
        presences = response.json().get("userPresences", [])
        if not presences:
            return "error", None, None
        data = presences[0]
        if data["userPresenceType"] == 0:
            return "offline", None, None
        elif data["userPresenceType"] == 1:
            return "online", None, None
        elif data["userPresenceType"] == 2:
            if "placeId" in data and "gameId" in data:
                return "in_game", data["placeId"], data["gameId"]
            return "privacy_enabled", None, None
    return "error", None, None

def get_game_name(place_id):
    url = f"https://games.roblox.com/v1/games/multiget-place-details?placeIds={place_id}"
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        games = response.json()
        if games and isinstance(games, list) and len(games) > 0 and "name" in games[0]:
            return games[0]["name"]
    return "Unknown Game"

def get_online_friends():
    my_id = get_my_user_id_joiner()
    if my_id is None:
        return []
    response = requests.get(f"https://friends.roblox.com/v1/users/{my_id}/friends", headers=get_headers())
    if response.status_code != 200:
        return []
    friends_data = response.json().get("data", [])
    friend_ids = [friend["id"] for friend in friends_data]
    presence_response = requests.post("https://presence.roblox.com/v1/presence/users", json={"userIds": friend_ids}, headers=get_headers())
    if presence_response.status_code != 200:
        return []
    presences = presence_response.json().get("userPresences", [])
    presence_dict = {p["userId"]: p for p in presences}
    online_friends = []
    for friend in friends_data:
        friend_id = friend["id"]
        presence = presence_dict.get(friend_id)
        if presence and presence["userPresenceType"] == 2 and "placeId" in presence and "gameId" in presence:
            friend_copy = friend.copy()
            friend_copy["placeId"] = presence["placeId"]
            friend_copy["gameId"] = presence["gameId"]
            online_friends.append(friend_copy)
    return online_friends

def multi_tool_menu():
    while True:
        clear_screen()
        print(f"{PURPLE}========== ROBLOX USER JOINER =========={RESET}")
        print(f"{PURPLE}1 - Join by Username/User ID{RESET}")
        print(f"{PURPLE}2 - Join a Friend{RESET}")
        print(f"{PURPLE}0 - Back to main menu{RESET}")
        choice = input(f"{PURPLE}Choose an option: {RESET}")
        if choice == "1":
            username = input(f"{PURPLE}Enter Username or User ID: {RESET}")
            if username.isdigit():
                user_id = int(username)
            else:
                user_id = get_user_id_multi(username)
            if not user_id:
                print(f"{PURPLE}User Not Found!{RESET}")
                time.sleep(1)
                continue
            check_user_status(user_id)
        elif choice == "2":
            friends = get_online_friends()
            if not friends:
                print(f"{PURPLE}No friends are in-game!{RESET}")
                time.sleep(1)
                continue
            print(f"{PURPLE}In-Game Friends:{RESET}")
            for idx, friend in enumerate(friends, 1):
                name = friend.get("displayName", friend.get("username", "N/A"))
                print(f"{PURPLE}{idx} - {name}{RESET}")
            friend_choice = input(f"{PURPLE}Choose a friend (0 to back): {RESET}")
            if friend_choice.isdigit() and 0 < int(friend_choice) <= len(friends):
                selected_friend = friends[int(friend_choice) - 1]
                check_friend_status(selected_friend)
        elif choice == "0":
            break

def check_user_status(user_id):
    clear_screen()
    print(f"{PURPLE}Checking user status...{RESET}")
    status, place_id, game_id = get_user_presence(user_id)
    if status == "offline":
        print(f"{PURPLE}User is offline.{RESET}")
    elif status == "online":
        print(f"{PURPLE}User is online.{RESET}")
    elif status == "privacy_enabled":
        print(f"{PURPLE}User's game privacy settings prevent tracking.{RESET}")
    elif status == "in_game":
        game_name = get_game_name(place_id)
        print(f"{PURPLE}User is in a game!{RESET}")
        print(f"{PURPLE}Game: {game_name}{RESET}")
        print(f"{PURPLE}Place ID: {place_id}{RESET}")
        choice = input(f"{PURPLE}1 = Join, 2 = Back: {RESET}")
        if choice == "1":
            join_url = f"roblox://placeId={place_id}&gameInstanceId={game_id}"
            print(f"{PURPLE}Joining game using URL: {join_url}{RESET}")
            webbrowser.open(join_url)
    time.sleep(1)

def check_friend_status(friend_data):
    clear_screen()
    print(f"{PURPLE}Checking friend's status...{RESET}")
    friend_id = friend_data.get("id")
    place_id = friend_data.get("placeId")
    game_id = friend_data.get("gameId")
    game_name = get_game_name(place_id)
    friend_name = friend_data.get("displayName", friend_data.get("username", "Unknown"))
    print(f"{PURPLE}{friend_name} is in a game!{RESET}")
    print(f"{PURPLE}Game: {game_name}{RESET}")
    print(f"{PURPLE}Place ID: {place_id}{RESET}")
    choice = input(f"{PURPLE}1 = Join, 2 = Back: {RESET}")
    if choice == "1":
        join_url = f"roblox://placeId={place_id}&gameInstanceId={game_id}"
        print(f"{PURPLE}Joining game using URL: {join_url}{RESET}")
        webbrowser.open(join_url)
    time.sleep(1)

def display_cookie_status():
    cookie = get_default_cookie()
    if cookie:
        print(f"{PURPLE}Cookie Status: Default cookie is set.{RESET}")
    else:
        print(f"{PURPLE}Cookie Status: You have no default cookie.{RESET}")

def main_menu():
    while True:
        clear_screen()
        print_main_ascii()
        display_cookie_status()
        print(f"{PURPLE}==================================={RESET}")
        print(f"{PURPLE}1) Roblox Account Generator{RESET}")
        print(f"{PURPLE}2) Roblox Player Info{RESET}")
        print(f"{PURPLE}3) Roblox User Joiner{RESET}")
        print(f"{PURPLE}4) Manage Cookie{RESET}")
        print(f"{PURPLE}0) Exit{RESET}")
        choice = input(f"\n{PURPLE}Enter your choice: {RESET}")
        if choice == "1":
            account_generator_menu()
        elif choice == "2":
            roblox_player_info_menu()
        elif choice == "3":
            multi_tool_menu()
        elif choice == "4":
            manage_cookie_menu()
        elif choice == "0":
            clear_screen()
            sys.exit(0)
        else:
            print(f"{PURPLE}Invalid choice, please try again.{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    ensure_installed_location()  
    repair_folders()             
    main_menu()