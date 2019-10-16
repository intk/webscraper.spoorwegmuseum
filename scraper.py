# Import libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

import time
import json
import urllib.parse

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

# Find themes
time.sleep(2)
themes = driver.find_elements_by_css_selector(config['theme'])
for theme in themes:
	themeAttribute = theme.get_attribute(config['themeAttribute'])
	if themeAttribute != 'home':
		themeTitle = driver.find_element_by_css_selector("%s[%s='%s'] %s" % (config['theme'], config['themeAttribute'], theme.get_attribute(config['themeAttribute']),  config['themeTitle'])).get_attribute('innerHTML') 
		themeDict = {'theme': themeTitle, 'subthemes': [], 'items': []}

		# Find subthemes
		subthemes = driver.find_elements_by_css_selector("%s[%s='%s'] %s" % (config['theme'], config['themeAttribute'], theme.get_attribute(config['themeAttribute']),  config['subtheme']))
		for subtheme in subthemes:
			themeDict['subthemes'].append(subtheme.get_attribute(config['subthemeAttribute']))

		# Find collection items
		items = driver.find_elements_by_css_selector("%s[%s='%s'] %s" % (config['theme'], config['themeAttribute'], theme.get_attribute(config['themeAttribute']),  config['item']))
		for item in items:
			themeDict['items'].append(item.get_attribute(config['itemAttribute']))

		sitemap.append(themeDict)

print("Themes found")
print(json.dumps(sitemap))

#Exit program
time.sleep(5)
driver.close()




