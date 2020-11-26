#!/usr/bin/python3

def does_class_exist( parent, class_name ):

    elems = parent.find_elements_by_class_name( class_name )

    if len( elems ) > 0 :
        return True

    return False

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

def find_element_by_tag_and_class_name( driver, tag_name, class_name, is_whole_name = True ):

    return find_element_by_tag_name_and_attribute_name( driver, tag_name, "class", class_name, is_whole_name )
