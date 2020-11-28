#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import config         # DRIVER_PATH
import helpers        # find_element_by_tag_and_class_name
import product_parser # parse_product

from datetime import datetime

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
    element = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.ID, "uc-btn-accept-banner"))
        )
    print( "DEBUG: found banner" )

    helpers.sleep( 5 )

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

    helpers.sleep(5)

    market_chooser_div = driver.find_element_by_class_name( 'gbmc-market-chooser-container' )

    print( "DEBUG: select_shop_by_post_code: found {}".format( market_chooser_div.get_attribute( 'class' ) ) )

    i = helpers.find_element_by_tag_and_class_name( market_chooser_div, "input", "gbmc-zipcode-input gbmc-undecided", False )

    if i == None:
        print( "FATAL: cannot find input field to enter postcode (PLZ)" )
        exit()

    print( "INFO: sending postcode {}".format( config.PLZ ) )

    i.send_keys( config.PLZ )

    helpers.sleep(3)

    #find_element_by_tag_and_class_name( market_chooser_div, "section", "gbmc-content", False )
    i = helpers.find_element_by_tag_and_class_name( market_chooser_div, "button", "gbmc-qa-pickup-trigger", False )

    if i == None:
        print( "FATAL: cannot find input field to enter postcode (PLZ)" )
        exit()

    i.click()

    helpers.sleep(3)

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

def harmonize_link( link ):

    if link.endswith('/'):
        return link

    return link + '/'

##########################################################

def determine_categories( driver ):

    # somehow the following doesn't work, so use the helper
    #div = driver.find_element_by_class_name( 'home-page-categories home-page-categories-collapsed' )
    div = helpers.find_element_by_tag_and_class_name( driver, 'div', 'home-page-categories home-page-categories-collapsed' )

    if div == None:
        print( "FATAL: cannot find categories" )
        exit()

    i2 = div.find_element_by_class_name( 'home-page-category-tiles' )

    elements = i2.find_elements_by_class_name( 'home-page-category-tile' )

    print( "INFO: found {} categories".format( len( elements ) ) )

    links = []

    for s in elements:
        link = s.get_attribute( 'href' )

        link = harmonize_link( link )

        print( "DEBUG: determine_categories: {}".format( link ) )
        links.append( link )

    return links

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

    return int( button.text )

##########################################################

def wait_till_product_page_loaded( driver ):

    element = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.ID, "search-service-content"))
        )

    print( "DEBUG: page loaded" )

    element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "search-service-paginationContainer"))
        )

##########################################################

def parse_page( driver, f, category_link ):

    content = driver.find_element_by_id( 'search-service-content' )

    if content == None:
        print( "FATAL: cannot find content" )
        exit()

    elements = content.find_elements_by_class_name( 'search-service-productDetailsWrapper' )

    print( "INFO: found {} elements".format( len( elements ) ) )

    for e in elements:
        p = product_parser.parse_product( e )
        line = category_link + ";" + p + "\n"
        f.write( line )
        print( '.', end='', flush=True )

    print()

##########################################################

def parse_category( driver, f, category_link ):

    driver.get( category_link )

    wait_till_product_page_loaded( driver )

    num_pages = determine_number_of_pages( driver )

    print( "INFO: number of pages {} on {}".format( num_pages, category_link ) )

    page = 1

    parse_page( driver, f, category_link )

    page += 1

    while page <= num_pages:

        driver.get( category_link + '?page=' + str( page ) )

        wait_till_product_page_loaded( driver )

        parse_page( driver, f, category_link )

        page += 1

##########################################################

def generate_filename():
    now = datetime.now()
    d1 = now.strftime( "%Y%m%d_%H%M" )
    res = "products_" + d1 + ".csv"
    return res

##########################################################
driver = init_driver()

driver.get( 'https://shop.rewe.de' )

accept_banner( driver )

select_shop_by_post_code( driver )

helpers.sleep(5)

category_links = determine_categories( driver )

f = open( generate_filename(), "w" )

for c in category_links:

    parse_category( driver, f, c )

    print( '*', end='', flush=True )

print()
