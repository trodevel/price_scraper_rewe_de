#!/usr/bin/python3

def parse_product_pic( product ):
    div = product.find_element_by_class_name( 'search-service-pictureWrapper' )
    img = div.find_element_by_tag_name( 'img' )
    print( "image={}".format( img.get_attribute( "src" ) ) )

def parse_product_title( product_details ):
    div = product_details.find_element_by_class_name( 'LinesEllipsis  ' )
    print( "title {}".format( div.text ) )

def parse_product_grammage( product_details ):
    div = product_details.find_element_by_class_name( 'search-service-productGrammage' )
    print( "grammage {}".format( div.text ) )

def parse_product_price( product_details ):
    div = product_details.find_element_by_class_name( 'search-service-productPrice' )
    print( "grammage {}".format( div.text ) )

def parse_product_details( product ):
    div = product.find_element_by_class_name( 'search-service-productDetails' )
    parse_product_title( div )
    parse_product_grammage( div )
    parse_product_price( div )

def parse_product( product ):

    parse_product_pic( product )
    parse_product_details( product )
