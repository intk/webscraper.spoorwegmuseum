# Import libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

import time
import json
import urllib.parse


# Function for getting collection item data
def getItem(url, itemTitle, itemSubtitle):

	# Load collection item
	driver.get(url)
	print("Item loaded: %s"%url)
	time.sleep(0.5)

	# Get title and subtitle of collection item
	itemTitle = driver.find_element_by_css_selector("%s" % config['itemTitle']).get_attribute('innerHTML').replace('\n', '').replace('\t', '')
	itemSubtitle = driver.find_element_by_css_selector("%s" % config['itemSubtitle']).get_attribute('innerHTML').replace('\n', '').replace('\t', '')
	headingDict = {'title': itemTitle, 'subtitle': itemSubtitle}

	return headingDict

# Get configuration
with open("config.json", 'r') as f:
	config = json.load(f)

# Set sitemap object
sitemap = []

# Set the url
url = config['url']

# Run Headless Chrome
options = Options()  
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("--disable-gpu")
options.headless = False

# Enable usage of cache and cookies
options.add_argument('user-data-dir=data')

driver = webdriver.Chrome('./chromedriver', chrome_options=options)  

# Open web page
driver.implicitly_wait(10)
driver.get(url)

# Return page source
print("Page loaded: {}".format(driver.current_url))

# Scrape webpage
time.sleep(2)
themes = driver.find_elements_by_css_selector(config['theme'])
print("Themes found")
for theme in themes:
	themeAttribute = theme.get_attribute(config['themeAttribute'])
	if themeAttribute != 'home':

		# Find themes
		themeTitle = driver.find_element_by_css_selector("%s[%s='%s'] %s" % (config['theme'], config['themeAttribute'], theme.get_attribute(config['themeAttribute']),  config['themeTitle'])).get_attribute('innerHTML') 
		themeDict = {'title': themeTitle, 'subtitle': '', 'link':'%s/#/%s'%(config['url'], themeAttribute), 'category': 'theme'}
		sitemap.append(themeDict)

		print("Theme %s appended"%themeTitle)

		# Find subthemes
		subthemes = driver.find_elements_by_css_selector("%s[%s='%s'] %s" % (config['theme'], config['themeAttribute'], theme.get_attribute(config['themeAttribute']),  config['subtheme']))
		for subtheme in subthemes:
			subthemeTitle = driver.find_element_by_css_selector("%s[%s='%s'] %s" % (config['subtheme'], config['subthemeAttribute'], subtheme.get_attribute(config['subthemeAttribute']),  config['subthemeTitle'])).get_attribute('innerHTML') 
			subthemeDict = {'title': subthemeTitle, 'subtitle': '', 'link':'%s/#/%s'%(config['url'], subtheme.get_attribute(config['subthemeAttribute'])), 'category': 'subtheme'}
			sitemap.append(subthemeDict)

			print("Subtheme %s appended"%subthemeTitle)

		# Find collection items
		items = driver.find_elements_by_css_selector("%s[%s='%s'] %s" % (config['theme'], config['themeAttribute'], theme.get_attribute(config['themeAttribute']),  config['item']))
		for item in items:
			itemAttribute = item.get_attribute(config['itemAttribute'])
			itemLink = '%s/#/%s'%(config['url'], itemAttribute)

			# Get item headings
			itemHeadings = getItem(itemLink, config['itemTitle'], config['itemSubtitle'])
			itemDict = {'title': itemHeadings['title'], 'subtitle': itemHeadings['subtitle'], 'link': itemLink, 'category': 'item'}
			sitemap.append(itemDict)

			print("Item %s appended"%itemDict['title'])

print(json.dumps(sitemap))

#Exit program
time.sleep(5)
driver.close()




