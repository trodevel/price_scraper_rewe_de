#!/usr/bin/python3

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import staleness_of

import config         # DRIVER_PATH
import helpers        # find_element_by_tag_and_class_name
import product_parser # parse_product
import re

from datetime import datetime

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

    links = dict()

    for s in elements:
        link = s.get_attribute( 'href' )
        name = s.text

        link = harmonize_link( link )

        print( "DEBUG: determine_categories: {} - {}".format( link, name ) )
        links[ link ] = name

    return links

##########################################################

def determine_subcategories( driver ):

    d1 = driver.find_element_by_class_name( 'search-service-rsFacetedProductList' )

    d2 = d1.find_element_by_class_name( 'search-service-hideInMobileView' )

    d3 = d2.find_element_by_class_name( 'search-service-rsFacetGroupListContainer' )

    # somehow the following doesn't work, so use the helper
    d4 = d3.find_element_by_class_name( 'search-service-navFacetGroupContainerFacetOptionList' )
    #d4 = helpers.find_element_by_tag_and_class_name( d3, 'div', 'search-service-navFacetGroupContainerFacetOptionList' )

    if d4 == None:
        print( "FATAL: cannot find sub-categories" )
        exit()

    d5 = d4.find_element_by_class_name( 'search-service-navFacetGroupList' )

    #d6 = d5.find_element_by_class_name( 'search-service-rsFacetGroupContainerFacetOptionList search-service-rsFacetGroupContainerIntendedFacetOption' )
    #d6 = helpers.find_element_by_tag_and_class_name( d5, 'li', 'search-service-rsFacetGroupContainerFacetOptionList search-service-rsFacetGroupContainerIntendedFacetOption' )

    #if d6 == None:
    #    print( "FATAL: cannot find sub-categories" )
    #    exit()

    elements = d5.find_elements_by_class_name( 'search-service-rsFacetGroupContainerCategoryFacetOption' )

    print( "INFO: found {} sub categories".format( len( elements ) ) )

    links = dict()

    for s in elements:
        link = s.get_attribute( 'href' )
        name = s.get_attribute( 'title' )

        link = harmonize_link( link )

        print( "DEBUG: determine_subcategories: {} - {}".format( link, name ) )
        links[ link ] = name

    return links

##########################################################

def determine_number_of_pages( driver ):

    try:

        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-service-paginationContainer"))
            )

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

    except:

        return 1

##########################################################

def has_page_loaded( driver ):
    #self.log.info("Checking if {} page is loaded.".format(self.driver.current_url))
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'

##########################################################

def wait_for_page_load_v1( driver, timeout=20 ):

    i = 0

    while i <= timeout:
        if has_page_loaded( driver ):
            print( "DEBUG: loaded page in {} sec".format( i ) )
            return
        i += 1
        helpers.sleep( 1 )

    print( "FATAL: cannot load page in {} sec".format( timeout ) )
    exit()

##########################################################

def wait_for_page_load_v3( driver, timeout=20 ):

    print( "DEBUG: waiting for page to load at {}.".format( driver.driver.current_url ) )
    old_page = driver.find_element_by_tag_name('html')
    yield
    WebDriverWait(driver, timeout).until(staleness_of(old_page))

##########################################################

def wait_for_page_load( driver, timeout=20 ):

    wait_for_page_load_v1( driver, timeout )

##########################################################

def extract_name_from_url( url ):
    p = re.compile( "/([a-z_\-]*)/$" )
    result = p.search( url )
    res = result.group( 1 )
    return res

##########################################################

#def wait_till_product_page_loaded( driver ):
#
#    element = WebDriverWait(driver, 15).until(
#        EC.visibility_of_element_located((By.ID, "search-service-content"))
#        )
#
#    print( "DEBUG: page loaded" )

##########################################################

def parse_page( driver, f, category_handle, category_name, subcategory_handle, subcategory_name ):

    content = driver.find_element_by_id( 'search-service-content' )

    if content == None:
        print( "FATAL: cannot find content" )
        exit()

    elements = content.find_elements_by_class_name( 'search-service-productDetailsWrapper' )

    print( "INFO: found {} elements".format( len( elements ) ) )

    for e in elements:
        p = product_parser.parse_product( e )
        line = category_handle + ';' + category_name + ';' + subcategory_handle + ';' + subcategory_name + ';' + p + "\n"
        f.write( line )
        print( '.', end='', flush=True )

    print()

##########################################################

def parse_subcategory( driver, f, category_handle, category_name, subcategory_link, subcategory_name ):

    subcategory_handle = extract_name_from_url( subcategory_link )

    driver.get( subcategory_link )

    #wait_till_product_page_loaded( driver )
    wait_for_page_load( driver )

    num_pages = determine_number_of_pages( driver )

    print( "INFO: number of pages {} on {}".format( num_pages, subcategory_link ) )

    page = 1

    print( "INFO: parsing page {} / {}".format( page, num_pages ) )

    parse_page( driver, f, category_handle, category_name, subcategory_handle, subcategory_name )

    page += 1

    while page <= num_pages:
        print( "INFO: parsing page {} / {}".format( page, num_pages ) )

        driver.get( subcategory_link + '?page=' + str( page ) )

        #wait_till_product_page_loaded( driver )
        wait_for_page_load( driver )

        parse_page( driver, f, category_handle, category_name, subcategory_handle, subcategory_name )

        page += 1

##########################################################

def parse_category( driver, f, category_link, category_name ):

    category_handle = extract_name_from_url( category_link )

    driver.get( category_link )

    #wait_till_product_page_loaded( driver )
    wait_for_page_load( driver )

    determine_subcategories( driver )

    num_pages = determine_number_of_pages( driver )

    print( "INFO: number of pages {} on {}".format( num_pages, category_link ) )

    page = 1

    print( "INFO: parsing page {} / {}".format( page, num_pages ) )

    parse_page( driver, f, category_handle, category_name )

    page += 1

    while page <= num_pages:
        print( "INFO: parsing page {} / {}".format( page, num_pages ) )

        driver.get( category_link + '?page=' + str( page ) )

        #wait_till_product_page_loaded( driver )
        wait_for_page_load( driver )

        parse_page( driver, f, category_handle, category_name )

        page += 1

##########################################################

def generate_filename():
    now = datetime.now()
    d1 = now.strftime( "%Y%m%d_%H%M" )
    res = "products_" + d1 + ".csv"
    return res

##########################################################
driver = helpers.init_driver( config.DRIVER_PATH )

driver.get( 'https://shop.rewe.de' )

accept_banner( driver )

select_shop_by_post_code( driver )

helpers.sleep(5)

category_links = determine_categories( driver )

num_categ = len( category_links )

f = open( generate_filename(), "w" )

i = 0

for c, category_name in category_links.items():

    i += 1

    print( "INFO: parsing category {} / {} - {}".format( i, num_categ, category_name ) )

    parse_category( driver, f, c, helpers.to_csv_conform_string( category_name ) )
