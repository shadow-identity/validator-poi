# -*- coding: utf-8 -*-
"""
That validator search similar named pois and returns table which contains
highlighted tag values that does not match the pattern
"""
__author__ = 'nedr'

#TODO: rename 'ideal' variable
#TODO: name search euristics
#TODO: web form to get all the data
#TODO: NodeGetByName method to OsmApi.py or do not use API at all

from lxml import etree
import lxml.html
from lxml.html import builder as E


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

    html = E.HTML(
        E.HEAD(
            E.TITLE('Table of POI')
        ),
        E.BODY(
            E.H1('Table of POI'),
            E.TABLE(
                tbody
            )
        )
    )

    lxml.html.open_in_browser(html)
    return lxml.html.tostring(html, pretty_print=True)


def name_search(pattern=(['name', u'Пятёрочка'],
                         ['shop', 'convenience'],
                         ['tag2', 'value2'],
                         ['tag3', 'value3'])
                ):
    """
    Search name or similar names in osm_data, returns list of ElementTree objects that's match
    1. open
    2. search name
        3. get needed tags
        4. make dict
    5. make list

    """
    osm_file_name = './map.osm'
    osm_file = open(osm_file_name, 'r')
    iteration = 0
    for _, element in etree.iterparse(osm_file):
        # element = the osm object (node, line, ...)
        iteration += 1
        print iteration
        if iteration == 8470:
            pass
        print element.get('id'), element.tag
        if len(element.findall('tag')):
            # element has tags - search needed items
            for key_tag in element.findall(u'.//tag[@k="name"][@v="Пятёрочка"]'):
                # we find 'tag' - this is required poi.
                # get his id and children's tags
                poi = {'id': element.get('id'), key_tag.get('k'): key_tag.get('v')}
                for tag in element:
                    # look every tag, get needed (that is in pattern)
                    for attribute in pattern:
                        if tag.get('k') == attribute[0]:
                            poi[attribute[0]] = tag.get('v')
                print poi
        element.clear()

    poi_id = []
    return poi_id


def parse_id(id):
    """
    Parse id, turn it to dict with only needed keys
    """
    poi_list = []
    return poi_list

pattern = ['name', u'Пятёрочка'], ['shop', 'convenience'], ['tag2', 'value2'], ['tag3', 'value3']

if __name__ == '__main__':
    name_search()

