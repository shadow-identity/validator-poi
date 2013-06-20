validator-poi
=============

For details, see the wiki (russian and english).

That validator search similar named poi's and returns table which contains
highlighted tag values that does not match the pattern

Validator looks into validator.cfg config for parameters. Format of config file:
name_of_file_with_osm_xml_data
tag_that_will_be_searched : needed_value_(case_sensitive)
other_tag : his_value
other_tag : his_value
etc

Script returns html file to stdout and starts web-browser to show result
