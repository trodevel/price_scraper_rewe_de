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

DEBUG_CATEGORY = False
DEBUG_SUBCATEGORY = False

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

    div = driver.find_element_by_css_selector( "div[class='home-page-categories home-page-categories-collapsed']" )

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

        if link.find( "frische" ) == -1 and DEBUG_CATEGORY == True:
            print( "DEBUG: temporary ignoring" )
            continue

        links[ link ] = name

    return links

##########################################################

def determine_subcategories( driver ):

    d1 = driver.find_element_by_class_name( 'search-service-rsFacetedProductList' )

    d2 = d1.find_element_by_class_name( 'search-service-hideInMobileView' )

    d3 = d2.find_element_by_class_name( 'search-service-rsFacetGroupListContainer' )

    d4 = d3.find_element_by_class_name( 'search-service-navFacetGroupContainerFacetOptionList' )

    if d4 == None:
        print( "FATAL: cannot find sub-categories" )
        exit()

    d5 = d4.find_element_by_class_name( 'search-service-navFacetGroupList' )

    d6 = d5.find_element_by_css_selector( "ul[class='search-service-rsFacetGroupContainerFacetOptionList search-service-rsFacetGroupContainerIntendedFacetOption']" )

    if d6 == None:
        print( "FATAL: cannot find sub-categories" )
        exit()

    elements = d6.find_elements_by_class_name( 'search-service-rsFacetGroupContainerCategoryFacetOption' )

    print( "INFO: found {} sub categories".format( len( elements ) ) )

    links = dict()

    for s in elements:

        if helpers.does_tag_exist( s, "a" ) == False:
            print( "WARNING: element without tag 'a', ignoring" )
            continue

        s2 = s.find_element_by_tag_name( "a" )

        link = s2.get_attribute( 'href' )
        name = s2.get_attribute( 'title' )

        if link == None:
            print( "WARNING: empty link {}, ignoring".format( s2 ) )
            continue

        link = harmonize_link( link )

        if link.find( "?" ) != -1:
            print( "WARNING: broken link {}, ignoring".format( link ) )
            continue

        print( "DEBUG: determine_subcategories: {} - {}".format( link, name ) )

        if link.find( "cerealien" ) == -1 and DEBUG_SUBCATEGORY == True:
            print( "DEBUG: temporary ignoring" )
            continue

        links[ link ] = name

    return links

##########################################################

def determine_number_of_pages( driver ):

    i = None

    try:

        i = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-service-paginationContainer"))
            )

    except:

        print( "WARNING: no pagination container found" )

        return 1

    #helpers.dump_elements_by_tag_name( i, 'div' )

    div = None

    if helpers.does_css_selector_exist( i, "div[class='search-service-paginationPagesContainer search-service-paginationPagesContainer']" ):
        div = i.find_element_by_css_selector( "div[class='search-service-paginationPagesContainer search-service-paginationPagesContainer']" )
    elif helpers.does_css_selector_exist( i, "div[class='search-service-paginationPagesContainer search-service-paginationPagesContainer search-service-paginationPagesContainerSmall']" ):
        div = i.find_element_by_css_selector( "div[class='search-service-paginationPagesContainer search-service-paginationPagesContainer search-service-paginationPagesContainerSmall']" )
    else:
        print( "FATAL: broken pagination container" )
        exit()

    #helpers.dump_elements_by_tag_name( div, 'form' )

    elems = div.find_elements_by_tag_name( 'form' )

    if len( elems ) == 0:
        print( "FATAL: cannot find pages" )
        exit()
    last = elems[-1]

    #print( last )

    #helpers.dump_elements_by_tag_name( last, 'button' )

    button = last.find_element_by_tag_name( 'button' )

    return int( button.text )

##########################################################

def extract_handle_from_url( url ):
    #print( "DEBUG: extract_handle_from_url: url = {}".format( url ) )
    p = re.compile( "/([a-z_\-]*)/$" )
    result = p.search( url )
    res = result.group( 1 )
    return res

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
        line = category_handle + ';' + subcategory_handle + ';' + category_name + ';' + subcategory_name + ';' + p + "\n"
        f.write( line )
        print( '.', end='', flush=True )

    print()

##########################################################

def parse_subcategory( driver, f, category_handle, category_name, subcategory_link, subcategory_name ):

    subcategory_handle = extract_handle_from_url( subcategory_link )

    driver.get( subcategory_link )

    helpers.wait_for_page_load( driver )

    num_pages = determine_number_of_pages( driver )

    print( "INFO: number of pages {} on {}".format( num_pages, subcategory_link ) )

    page = 1

    print( "INFO: parsing page {} / {}".format( page, num_pages ) )

    parse_page( driver, f, category_handle, category_name, subcategory_handle, subcategory_name )

    page += 1

    while page <= num_pages:
        print( "INFO: parsing page {} / {}".format( page, num_pages ) )

        driver.get( subcategory_link + '?page=' + str( page ) )

        helpers.wait_for_page_load( driver )

        parse_page( driver, f, category_handle, category_name, subcategory_handle, subcategory_name )

        page += 1

##########################################################

def parse_category( driver, f, category_link, category_name ):

    category_handle = extract_handle_from_url( category_link )

    driver.get( category_link )

    helpers.wait_for_page_load( driver )

    # "angebot" page has another structure, so we'll not bother us with parsing sub-categories
    if category_link.find( "/angebot" ) != -1:
        parse_page( driver, f, category_handle, category_name, category_handle, category_name )
        return

    links = determine_subcategories( driver )

    num_links = len( links )

    i = 0

    for c, name in links.items():

        i += 1

        print( "INFO: parsing subcategory {} / {} - {}".format( i, num_links, name ) )

        parse_subcategory( driver, f, category_handle, category_name, c, helpers.to_csv_conform_string( name ) )


##########################################################

def generate_filename():
    now = datetime.now()
    d1 = now.strftime( "%Y%m%d_%H%M" )
    res = "products_" + d1 + ".csv"
    return res

##########################################################
driver = helpers.init_driver( config.DRIVER_PATH, config.BROWSER_BINARY )

driver.get( 'https://shop.rewe.de' )

accept_banner( driver )

select_shop_by_post_code( driver )

helpers.sleep(5)

links = determine_categories( driver )

num_links = len( links )

f = open( generate_filename(), "w" )

i = 0

for c, name in links.items():

    i += 1

    print( "INFO: parsing category {} / {} - {}".format( i, num_links, name ) )

    parse_category( driver, f, c, helpers.to_csv_conform_string( name ) )

print( "INFO: done" )
