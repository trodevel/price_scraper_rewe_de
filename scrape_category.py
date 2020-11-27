#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import config         # DRIVER_PATH
import helpers        # find_element_by_tag_and_class_name
import product_parser # parse_product

import time

##########################################################

def init_driver():
    options = webdriver.ChromeOptions() 
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    DRIVER_PATH = config.DRIVER_PATH
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

    return driver

##########################################################

def accept_banner( driver ):
    element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "uc-btn-accept-banner"))
        )
    print( "found banner, sleeping" )

    time.sleep(10)

    print( "clicking" )

    terms_button = driver.find_element_by_id( 'uc-btn-accept-banner' )
    terms_button.click()

##########################################################

def select_shop_by_post_code( driver ):
    i = helpers.find_element_by_tag_and_class_name( driver, 'button', 'gbmc-trigger gbmc-qa-trigger' )

    if i == None:
        print( "FATAL: cannot find button to enter postcode (PLZ)" )
        exit()

    i.click()

    print( "sleeping" )
    time.sleep(5)

    market_chooser_div = driver.find_element_by_class_name( 'gbmc-market-chooser-container' )

    print( "found {}".format( market_chooser_div.get_attribute( 'class' ) ) )

    i = helpers.find_element_by_tag_and_class_name( market_chooser_div, "input", "gbmc-zipcode-input gbmc-undecided", False )

    if i == None:
        print( "FATAL: cannot find input field to enter postcode (PLZ)" )
        exit()

    print( "sending postcode {}".format( config.PLZ ) )

    i.send_keys( config.PLZ )

    print( "sleeping" )
    time.sleep(3)

    #find_element_by_tag_and_class_name( market_chooser_div, "section", "gbmc-content", False )
    i = helpers.find_element_by_tag_and_class_name( market_chooser_div, "button", "gbmc-qa-pickup-trigger", False )

    if i == None:
        print( "FATAL: cannot find input field to enter postcode (PLZ)" )
        exit()

    i.click()

    print( "sleeping" )
    time.sleep(3)

    article = helpers.find_element_by_tag_name_and_attribute_name( market_chooser_div, "article", "data-testid", "gbmc-pickup-market-1763192" )

    if article == None:
        print( "FATAL: cannot find input desired shop" )
        exit()

    i = helpers.find_element_by_tag_name_and_attribute_name( article, "button", "data-testid", "gbmc-market-picker" )

    if i == None:
        print( "FATAL: cannot click on desired shop" )
        exit()

    i.click()

##########################################################

def determine_number_of_pages( driver ):

    i = driver.find_element_by_class_name( 'search-service-paginationContainer' )

    #helpers.dump_elements_by_tag_name( i, 'div' )

    # somehow the following doesn't work, so use the helper
    #div = i.find_element_by_class_name( 'search-service-paginationPagesContainer search-service-paginationPagesContainer' )

    div = helpers.find_element_by_tag_and_class_name( i, 'div', 'search-service-paginationPagesContainer search-service-paginationPagesContainer' )

    if div == None:
        print( "FATAL: cannot find pagination container" )
        exit()

    #helpers.dump_elements_by_tag_name( div, 'form' )

    elems = div.find_elements_by_tag_name( 'form' )

    if len( elems ) == 0:
        print( "FATAL: cannot find pages" )
        exit();
    last = elems[-1]

    #print( last )

    #helpers.dump_elements_by_tag_name( last, 'button' )

    button = last.find_element_by_tag_name( 'button' )

    return button.text

##########################################################

driver = init_driver()

driver.get('https://shop.rewe.de/c/obst-gemuese/?page=2')

accept_banner( driver )

select_shop_by_post_code( driver )

print( "sleeping" )
time.sleep(5)

num_pages = determine_number_of_pages( driver )

print( "INFO: number of pages {}".format( num_pages ) )

content = driver.find_element_by_id( 'search-service-content' )

if content == None:
    print( "FATAL: cannot find content" )
    exit()

elements = content.find_elements_by_class_name( 'search-service-productDetailsWrapper' )

print( "INFO: found {} elements".format( len( elements ) ) )

for e in elements:
    p = product_parser.parse_product( e )
    print( p )

exit()
