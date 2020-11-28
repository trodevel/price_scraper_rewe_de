#!/usr/bin/python3

import helpers

def parse_product_pic( product ):
    div = product.find_element_by_class_name( 'search-service-pictureWrapper' )
    img = div.find_element_by_tag_name( 'img' )
    return img.get_attribute( "src" )

def parse_product_title( p ):
    div = p.find_element_by_class_name( 'LinesEllipsis  ' )
    return div.text

def parse_product_grammage( p ):
    div = p.find_element_by_class_name( 'search-service-productGrammage' )
    return div.text

def parse_product_price( p ):
    return helpers.get_optional_element_text_by_class_name( p, 'search-service-productPrice', '-1' )

def parse_product_offer_1st_duration( p ):
    return helpers.get_optional_element_text_by_class_name( p, 'search-service-productOfferDuration', '' )

def parse_product_offer_1st_original_price( p ):
    return helpers.get_optional_element_text_by_class_name( p, 'search-service-productOfferOriginalPrice', '' )

def parse_product_offer_1st( p ):
    name = 'search-service-productOfferFirstLine'
    if helpers.does_class_exist( p, name ):
        div = p.find_element_by_class_name( name )
        a = parse_product_offer_1st_duration( div )
        b = parse_product_offer_1st_original_price( div )
        return a + ";" + b
    return ";"

def parse_product_offer_2nd_product_offer_price( p ):
    return helpers.get_optional_element_text_by_class_name( p, 'search-service-productOfferPrice', '' )

def parse_product_offer_2nd( p ):
    name = 'search-service-productOfferSecondLine'
    if helpers.does_class_exist( p, name ):
        div = p.find_element_by_class_name( name )
        return parse_product_offer_2nd_product_offer_price( div )
    return ""

def parse_product_offer( p ):
    name = 'search-service-productOffer'
    if helpers.does_class_exist( p, name ):
        div = p.find_element_by_class_name( name )
        a = parse_product_offer_1st( div )
        b = parse_product_offer_2nd( div )
        return a + ";" + b
    return ";;"

def parse_product_details( product ):
    div = product.find_element_by_class_name( 'search-service-productDetails' )
    a = parse_product_title( div )
    b = parse_product_grammage( div )
    c = parse_product_price( div )
    d = parse_product_offer( div )
    return a + ";" + b + ";" + c + ";" + d

def parse_product( product ):

    pic = parse_product_pic( product )
    details = parse_product_details( product )

    res = details + ";" + pic

    return res.replace( "\n", "<br>" )
