#!/usr/bin/python3

import helpers

def parse_product_pic( product ):
    div = product.find_element_by_class_name( 'search-service-pictureWrapper' )
    img = div.find_element_by_tag_name( 'img' )
    return img.get_attribute( "src" )

def parse_product_title( product_details ):
    div = product_details.find_element_by_class_name( 'LinesEllipsis  ' )
    return div.text

def parse_product_grammage( product_details ):
    div = product_details.find_element_by_class_name( 'search-service-productGrammage' )
    return div.text

def parse_product_price( product_details ):
    name = 'search-service-productPrice'
    if helpers.does_class_exist( product_details, name ):
        div = product_details.find_element_by_class_name( name )
        return div.text
    return "-1"

def parse_product_details( product ):
    div = product.find_element_by_class_name( 'search-service-productDetails' )
    a = parse_product_title( div )
    b = parse_product_grammage( div )
    c = parse_product_price( div )
    return a + ";" + b + ";" + c

def parse_product( product ):

    pic = parse_product_pic( product )
    details = parse_product_details( product )

    return details + ";" + pic
