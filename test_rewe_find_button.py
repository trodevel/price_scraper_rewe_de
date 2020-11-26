#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import config         # DRIVER_PATH

import time

options = webdriver.ChromeOptions() 
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

DRIVER_PATH = config.DRIVER_PATH
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get('https://shop.rewe.de/c/obst-gemuese/?page=2')

element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "uc-btn-accept-banner"))
    )

print "found banner, sleeping"

time.sleep(10)

print "clicking"
terms_button = driver.find_element_by_id( 'uc-btn-accept-banner' )
terms_button.click()

all_buttons = driver.find_elements_by_tag_name('button')

print "Buttons ", len( all_buttons ), ":"
for i in all_buttons:
    i_class = i.get_attribute('class')
    print ( i.text, 'class ', i_class )
    if i_class == 'gbmc-trigger gbmc-qa-trigger':
        print "FOUND !!!!"
        i.click()
        break

try:
    link_select_loc = driver.find_element_by_id("gbmc-trigger gbmc-qa-trigger")

    print( "found 'select loc' link" )
except:
    print( "ERROR: found 'select loc' link" )
    #print("Unexpected error:", sys.exc_info()[0])
    exit()

link_select_loc.click()

elements = driver.find_elements_by_class_name("gbmc-market-chooser-container")

print( "found", len( elements ), " elements" )

if elements is not None:
    for element in elements:
        print(element.text)
        #match = pattern.match(element.text)
        #if match:
            #print(element.text)

#terms_button = driver.find_element_by_id( 'uc-btn-accept-banner' )

#if terms_button is not None:
#    terms_button.click()
