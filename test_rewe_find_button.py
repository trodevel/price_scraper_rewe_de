#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import config         # DRIVER_PATH

import time

def find_element_by_tag_and_class_name( driver, tag, class_name, is_whole_name = True ):

    print( "INFO: looking for '{}' '{}':".format( tag, class_name ) )

    all_elems = driver.find_elements_by_tag_name( tag )

    print( "DEBUG: all '{}' {}:".format( tag, len( all_elems ) ) )

    for i in all_elems:
        i_class = i.get_attribute( 'class' )
        print ( "DEBUG: {} class '{}'".format( i.text, i_class ) )
        if is_whole_name:
            if i_class == class_name:
                print( "DEBUG: FOUND - {}".format( i_class ) )
                return i
        else:
            if i_class.startswith( class_name ):
                print( "DEBUG: FOUND - {} ".format( i_class ) )
                return i

    return None;

def find_element_by_tag_name_and_attribute_name( driver, tag_name, attribute_name, attribute_val, is_whole_name = True ):

    print( "INFO: looking for '{}' '{}' = '{}':".format( tag_name, attribute_name, attribute_val ) )

    all_elems = driver.find_elements_by_tag_name( tag_name )

    print( "DEBUG: all '{}' {}:".format( tag_name, len( all_elems ) ) )

    for i in all_elems:
        i_val = i.get_attribute( attribute_name )
        print ( "DEBUG: {} '{}' '{}'".format( i.text, attribute_name, i_val ) )
        if is_whole_name:
            if i_val == attribute_val:
                print( "DEBUG: FOUND - {}".format( i_val ) )
                return i
        else:
            if i_val.startswith( attribute_val ):
                print( "DEBUG: FOUND - {} ".format( i_val ) )
                return i

    return None;

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

print( "found banner, sleeping" )

time.sleep(10)

print( "clicking" )
terms_button = driver.find_element_by_id( 'uc-btn-accept-banner' )
terms_button.click()


i = find_element_by_tag_and_class_name( driver, 'button', 'gbmc-trigger gbmc-qa-trigger' )

if i == None:
    print( "FATAL: cannot find button to enter postcode (PLZ)" )
    exit()

i.click()

print( "sleeping" )
time.sleep(5)


market_chooser_div = driver.find_element_by_class_name( 'gbmc-market-chooser-container' )

print( "found {}".format( market_chooser_div.get_attribute( 'class' ) ) )

#all_elems = market_chooser_div.find_elements_by_xpath(".//*")
#all_elems = market_chooser_div.find_elements_by_tag_name( "div" )
all_elems_d = market_chooser_div.find_elements_by_tag_name( "div" )
all_elems_s = market_chooser_div.find_elements_by_tag_name( "section" )

print( "DEBUG: size {}, {}:".format( len( all_elems_d ), len( all_elems_s ) ) )

all_elems = all_elems_d

#document.querySelector("body > div.gbmc-market-chooser-container > section > div > div > label > input")
#/html/body/div[49]/section/div/div/label/input
#all_elems = driver.find_elements_by_xpath("/html/body/div")
print( "DEBUG: all '{}' {}:".format( 'div', len( all_elems ) ) )

for i in all_elems:
    i_class = i.get_attribute( 'class' )
    print ( "DEBUG: class '{}'".format( i_class ) )

#find_element_by_tag_and_class_name( market_chooser_div, "section", "gbmc-content", False )
i = find_element_by_tag_and_class_name( market_chooser_div, "input", "gbmc-zipcode-input gbmc-undecided", False )

if i == None:
    print( "FATAL: cannot find input field to enter postcode (PLZ)" )
    exit()

print( "sending postcode {}".format( config.PLZ ) )

i.send_keys( config.PLZ )

print( "sleeping" )
time.sleep(3)

#find_element_by_tag_and_class_name( market_chooser_div, "section", "gbmc-content", False )
i = find_element_by_tag_and_class_name( market_chooser_div, "button", "gbmc-qa-pickup-trigger", False )

if i == None:
    print( "FATAL: cannot find input field to enter postcode (PLZ)" )
    exit()

i.click()

print( "sleeping" )
time.sleep(3)

article = find_element_by_tag_name_and_attribute_name( market_chooser_div, "article", "data-testid", "gbmc-pickup-market-1763192" )

if article == None:
    print( "FATAL: cannot find input desired shop" )
    exit()

i = find_element_by_tag_name_and_attribute_name( article, "button", "data-testid", "gbmc-market-picker" )

if i == None:
    print( "FATAL: cannot click on desired shop" )
    exit()

i.click()

exit()

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
