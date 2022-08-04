Welcome to Song Downloader 

Please install all the requirements that are specified in "requirements.txt"
NOTE: It is recommended to install these requirements in a virtual environment and run this script in that environment

The project uses selenium to scrape songs from the site: https://www.pagalworld.us/
NOTE: selenium uses a browser as a driver in order to interact with the website

The version of the Chrome driver that is used for this project is "ChromeDriver 103.0.5060.134"

You can replace the chrome driver in the working directory if it isn't compatible with your device.
Use link: https://chromedriver.chromium.org/downloads to download chrome driver.

Before running the script please set the value of path by to the directory where you want to download your songs and set the timeOut according to your internet speed as the script will maximum wait for time specified in timeOut after that it will close the driver automatically and move onto the next one.
NOTE: the path you enter must exists beforehand and the timeOut is in seconds.

Flow of Script:
    1. Run the script
    2. Enter name of the artist
    3. Wait while script fetches list of artists found on the website
    4. Select the artist whose songs you want to download
    5. The Script will automatically create a directory with name of the artist on the path specified
    6. Wait while script fetches list of songs available on the site for that specific artist
    7. After fetching list of songs the script will start downloading the songs one by one

NOTES:
    1. If you want to download multiple songs simultaneously you can use ThreadPoolExecutor of concurrent.futures and specify the max_workers (number of threads allowed to execute at a time)
    2. Two different techniques has been used for waiting until a file has been downloaded (one for headless -- CLI version and one for GUI version) as there is no method available in selenium to detect and wait until a file has been downloaded
        
        GUI method: the script opens download page of chrome in new tab and looks for the progress of the latest file that is currently downloading or downloaded after every 1 second. (you can reduce time if you want to)

        CLI method: the script checks that if there is any file that is currently downloading after every 1 second. If no then it closes the drivers. (you can reduce time if you want to)

Credits:
developed by Devil
