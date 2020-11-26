#!/usr/bin/python3

def parse_product_pic( product ):
    div = product.find_element_by_class_name( 'search-service-pictureWrapper' )
    img = div.find_element_by_tag_name( 'img' )
    print( "image={}".format( img.get_attribute( "src" ) ) )


def parse_product( product ):

    parse_product_pic( product )
