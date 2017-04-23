import csv
import redfin_scraper
from pyzipcode import ZipCodeDatabase
from datetime import datetime as dt
from selenium.webdriver.chrome.options import Options
import multiprocessing

zcdb = ZipCodeDatabase()
# zips = [zc.zip for zc in zcdb.find_zip()]
zips = ['73103']
sttm = dt.now().strftime('%Y%m%d-%H%M%S')
dataDir = './data'
chrome_options = Options()
chrome_options.add_extension("./proxy.zip")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--window-size=1024,768")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-infobars")
sttm = dt.now().strftime('%Y%m%d-%H%M%S')

with open('not_listed.csv', 'rb') as f:
    reader = csv.reader(f)
    not_listed = [zc for zclist in reader for zc in zclist]

for zc in zips:

    if zc in not_listed:
        continue

    outfile = '/historic_sales/events_' + zc + '_' + sttm + '.csv'
    processedUrlsFName = '/processed_urls/processed_urls_' + zc + '.csv'

    rf = redfin_scraper.redfinScraper(
        outfile, processedUrlsFName, virtualDisplay=True,
        subClusterMode='series', timeFilter='sold-all',
        dataDir=dataDir, startTime=sttm)

    rf.run(zc)
