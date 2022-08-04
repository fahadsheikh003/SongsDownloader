from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from time import sleep
import pandas as pd
import json
import os
import glob

timeOut = 60
path = 'D:\\AudioSongs'

def create_directory(name: str):
    global path
    path = os.path.join(path, name)
    if not os.path.exists(path):
        os.makedirs(path)

def get_files_count():
    count = 0
    for _path in os.listdir(path):
        if os.path.isfile(os.path.join(path, _path)):
            count += 1
    return count

def check_for_incomplete_downloads():
    for _path in os.listdir(path):
        if ".crdownload" in _path:
            print(f"Downloading {_path[:-(len('.crdownload'))]}....")
            return True
    return False

def get_index(string: str, char: str):
    if string == None or string == "" or char == None or char == "":
        return -1
    
    for i in range(len(string) - 1, -1, -1):
        if char[0] == string[i]:
            return i
    return -1

def get_recently_created_file():
    list_of_files = glob.glob(f"{path}/*")
    if len(list_of_files) == 0:
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    pos = get_index(latest_file, '\\')
    return latest_file[pos+1:]

def get_page_urls(url: str):
    if url == None or url == "":
        return None

    links = []
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service('chromedriver.exe'), options=options)
    driver.get(url)

    while True:
        try:
            songs = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='nw m bk']"))
            )
        except:
            print("Unable to load songs in webpage")
            driver.close()
            break
        else:
            songs = driver.find_elements(By.CSS_SELECTOR, "div[class='nw m bk']")

        for song in songs:
            try:
                link = song.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            except:
                link = ""

            if link != "":
                links.append(link)

        try:
            driver.find_element(By.LINK_TEXT, "NEXT").click()
        except:
            break

    driver.close()
    return links

def download_song_with_gui(url: str):
    if url == None or url == "":
        return None

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    prefs = {'download.default_directory':path}
    options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(service=Service('chromedriver.exe'), options=options)
    try:
        driver.get(url)
    except:
        print("link corrupted!")
        return

    try:
        dbutton = driver.find_element(By.LINK_TEXT, '320Kbps Mp3 Songs')
    except:
        try:
            dbutton = driver.find_element(By.LINK_TEXT, '192Kbps Mp3 Songs')
        except:
            try:
                dbutton = driver.find_element(By.LINK_TEXT, '128Kbps Mp3 Songs')
            except:
                dbutton = ""

    if dbutton == "":
        return

    dbutton.click()

    for window in driver.window_handles:
        if window == driver.window_handles[0]:
            continue
        driver.switch_to.window(window)
        driver.close()
    
    driver.switch_to.window(driver.window_handles[0])

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get('chrome://downloads')

    try:
        host1 = driver.find_element(By.CSS_SELECTOR, "downloads-manager").shadow_root
        host2 = host1.find_element(By.CSS_SELECTOR, "downloads-item").shadow_root
        title = host2.find_element(By.ID, 'title-area').text
    except:
        print("Unable to locate downloading progress")
        driver.quit()
        return

    print(f"Downloading {title}")

    for _ in range(timeOut):
        progress = host2.find_element(By.ID, "progress")
        prog = progress.get_attribute('value')
        print(f"Progress: {prog}")
        if prog == "100":
            print("Download Completed!")
            break
        sleep(1)
    else:
        print('timeOut!')

    driver.quit()
        
def download_song_without_gui(url: str):
    if url == None or url == "":
        return None

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    prefs = {'download.default_directory':path}
    options.add_experimental_option('prefs', prefs)
    options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service('chromedriver.exe'), options=options)

    try:
        driver.get(url)
    except:
        print("link corrupted!")
        return

    try:
        dbutton = driver.find_element(By.LINK_TEXT, '320Kbps Mp3 Songs')
    except:
        try:
            dbutton = driver.find_element(By.LINK_TEXT, '192Kbps Mp3 Songs')
        except:
            try:
                dbutton = driver.find_element(By.LINK_TEXT, '128Kbps Mp3 Songs')
            except:
                dbutton = ""

    if dbutton == "":
        return

    # countBeforeDownloading = get_files_count()

    dbutton.click()

    sleep(2)

    for _ in range(timeOut):
        # countAfterDownloading = get_files_count()
        # if countAfterDownloading > countBeforeDownloading:
        #     break
        if not check_for_incomplete_downloads():
            break
        sleep(1)
    else:
        print('timeOut!')
        driver.quit()
        return

    songName = get_recently_created_file()
    print(f"{songName} Downloaded..")

    driver.quit()

def download_songs(links: list):
    for link in links:
        # download_song_with_gui(link)
        download_song_without_gui(link)

def get_artist_names(artist: str):
    if artist == None or artist == "":
        return None

    encodedArtist = quote(artist)

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--headless")

    url = f"https://www.pagalworld.us/search.php?q={encodedArtist}"
    driver = webdriver.Chrome(service=Service('chromedriver.exe'), options=options)
    driver.get(url)

    main = driver.find_element(By.CSS_SELECTOR, "div[class='block']")

    singersList = []
    
    Lists = main.find_elements(By.TAG_NAME, "ul")
    for ListItems in Lists:
        ListItemsElement = ListItems.find_elements(By.TAG_NAME, "li")
        check = False
        for items in ListItemsElement:
            if check:
                singersList.append(items)
            if "Singer Search Results" in items.text:
                check = True
        
    Names = []
    Links = []
    for singer in singersList:
        element = singer.find_element(By.TAG_NAME, 'a')
        Names.append(element.text)
        Links.append(element.get_attribute('href'))

    df = pd.DataFrame({'name':Names, 'link':Links})
    return json.loads(df.to_json(orient='records'))

def select_artist(artists: list):
    if artists != None:
        for artist in artists:
            choice = input(f"Do u mean {artist['name']}? (yes or no)\nchoice: ")
            if choice.lower() == "yes":
                return artist
    return None

if __name__ == "__main__":
    artist = input("Enter name of the Artist: ")

    print("Please wait while we're fetching list of artists for u..")
    print("And don't worry we'll inform u if there is any issue..")

    artists = get_artist_names(artist)
    artist = select_artist(artists)
    if artist == None:
        print("Thank you for using this app..")
        print("Developed by Devil..")
        exit(0)

    create_directory(artist['name'])

    print("Please wait while we're fetching list of songs..")
    print("And don't worry we'll inform u if there is any issue..")

    links = get_page_urls(artist['link'])

    print("Please hold on while we're downloading songs..")
    print("And don't worry we'll inform u if there is any issue..")

    download_songs(links)

    print(f"Congratulations all the songs that we've found are downloaded at {path}..")
    print("Thank you for using this app..")
    print("Developed by Devil..")

    # download_song_without_gui('https://www.pagalworld.us/23856/dil-meri-na-sune-mp3-songs.html')