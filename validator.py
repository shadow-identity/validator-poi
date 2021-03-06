# -*- coding: utf-8 -*-
"""
That validator finds similar named POIs and returns table with highlighted tag values that does not match the pattern.

Validator looks for settings in the validator.cfg file. Format of this file:

name_of_file_with_osm_xml_data
tag_that_will_be_searched : needed_value_(case_sensitive)
other_tag : his_value
other_tag : his_value
etc

Script returns html file to stdout and starts web-browser to show result
"""

#TODO: web form to get all the data

from lxml import etree
import lxml.html
from lxml.html import builder as E


def read_config(file_name='validator.cfg'):
    config = open(file_name, 'r').read().splitlines()
    osm_file = config[0]
    pattern = []
    for line in config:
        item = line.rsplit(':')
        if len(item) == 2:
            item[0], item[1] = item[0].strip(), item[1].strip().decode('utf-8')
            pattern.append(item)
    return pattern, osm_file


def create_josm_url(poi):
    id = poi.get('id')
    tag = poi.tag
    if tag == 'node':
        url_id = 'n' + id
    elif tag == 'way':
        url_id = 'w' + id
    elif tag == 'relation':
        url_id = 'r' + id
    else:
        url_id = 'OBJECT {tag} ERROR'.format(tag=tag)
    return 'http://localhost:8111/load_object?objects=' + url_id


def generate_html(pattern, poi_list):
    """
    Generates html with table, filled by poi
    """
    tbody = etree.Element('tbody')
    tr_header = etree.SubElement(tbody, 'tr')
    for key in pattern:
        # generate header of table which contains all given keys
        th_header = etree.SubElement(tr_header, 'th')
        th_header.text = key[0]
    th_header = etree.SubElement(tr_header, 'th')
    th_header.text = 'Edit in josm'

    for poi in poi_list:
        # generate element tree of poi
        tr = etree.SubElement(tbody, 'tr')
        for key in pattern:
            td = etree.SubElement(tr, 'td')
            if key[1] == poi.get(key[0]):
                td.text = poi.get(key[0], '')
            else:
                # if value not equal to pattern, mark it bold
                b = etree.SubElement(td, 'b')
                b.text = poi.get(key[0])
        td = etree.SubElement(tr, 'td')
        link = etree.SubElement(td, 'a')
        link.set('href', poi['josm_url'])
        link.text = 'Edit'

    html = E.HTML(
        E.HEAD(
            E.META(content="text/html; charset=utf-8"),
            E.TITLE('Table of POI')
        ),
        E.BODY(
            E.H1('Table of POI'),
            E.TABLE(
                tbody,
                cellspacing="0", cellpadding="10",  border="1",

            )
        )
    )

    lxml.html.open_in_browser(html)
    return lxml.html.tostring(html, pretty_print=True)


def name_search(pattern, osm_file_name):
    """
    Search name or similar names in osm_data, returns list of ElementTree objects that's match
    1. open
    2. search name
        3. get needed tags
        4. make dict
    5. make list of needed poi's

    """

    query = u'.//tag[@k="{key}"][@v="{value}"]'.format(key=pattern[0][0],
                                                       value=pattern[0][1])
    osm_file = open(osm_file_name, 'r').read()
    element = etree.fromstring(osm_file)

    poi_list = []
    #TODO: make search with inaccurate match ????
    for poi_tag in element:
        # get every element and search for needed tags
        for key_tag in poi_tag.findall(query):
            # we find 'tag' - this is required poi.
            # get his id and children's tags
            poi = {'id': poi_tag.get('id'), key_tag.get('k'): key_tag.get('v')}
            for tag in poi_tag:
                # look every tag, get needed (that is in pattern)
                for attribute in pattern:
                    if tag.get('k') == attribute[0]:
                        poi[attribute[0]] = tag.get('v')
            poi['josm_url'] = create_josm_url(poi_tag)
            poi_list.append(poi)
    return poi_list


if __name__ == '__main__':
    pattern, osm_file = read_config()
    poi_list = name_search(pattern, osm_file)
    print generate_html(pattern, poi_list)

