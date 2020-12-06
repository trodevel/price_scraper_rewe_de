#!/usr/bin/python3

from selenium import webdriver

import time

##########################################################

def init_driver( driver_path ):
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome( options=options, driver_path )

    return driver

##########################################################

def does_class_exist( parent, class_name ):

    elems = parent.find_elements_by_class_name( class_name )

    if len( elems ) > 0 :
        return True

    return False

def get_optional_element_text_by_class_name( parent, class_name, default_value ):

    if does_class_exist( parent, class_name ):
        div = parent.find_element_by_class_name( class_name )
        return div.text

    return default_value

def find_element_by_tag_name_and_attribute_name( driver, tag_name, attribute_name, attribute_val, is_whole_name = True ):

    print( "INFO: looking for '{}' '{}' = '{}':".format( tag_name, attribute_name, attribute_val ) )

    all_elems = driver.find_elements_by_tag_name( tag_name )

    print( "DEBUG: find_element_by_tag_name_and_attribute_name: all '{}' {}:".format( tag_name, len( all_elems ) ) )

    for i in all_elems:
        i_val = i.get_attribute( attribute_name )
        print ( "DEBUG: find_element_by_tag_name_and_attribute_name: {} '{}' '{}'".format( i.text, attribute_name, i_val ) )
        if is_whole_name:
            if i_val == attribute_val:
                print( "DEBUG: find_element_by_tag_name_and_attribute_name: FOUND - {}".format( i_val ) )
                return i
        else:
            if i_val.startswith( attribute_val ):
                print( "DEBUG: find_element_by_tag_name_and_attribute_name: FOUND - {} ".format( i_val ) )
                return i

    return None;

def find_element_by_tag_and_class_name( driver, tag_name, class_name, is_whole_name = True ):

    return find_element_by_tag_name_and_attribute_name( driver, tag_name, "class", class_name, is_whole_name )

def dump_elements_by_tag_name( driver, tag_name ):

    all_elems = driver.find_elements_by_tag_name( tag_name )

    print( "dump_elements_by_tag_name: tag '{}', found {} element(s):".format( tag_name, len( all_elems ) ) )

    for i in all_elems:
        print( "class '{}', id '{}'".format( i.get_attribute( 'class' ), i.get_attribute( 'id' ) ) )

def sleep( sec ):
    print( "sleeping {} sec".format( sec ) )
    time.sleep( sec )

def quote_quotes( s ):
    res = s.replace( '"', '""' )
    return res

def to_csv_conform_string( s, separator = ';' ):

    if s.find( separator ) != -1:
        return '"' + quote_quotes + '"'

    return s
