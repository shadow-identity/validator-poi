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


def name_search(name, osm_data):
    """
    Search name or similar names in osm_data, returns list of ElementTree objects that's match
    1. open
    2. search name
        3. get needed tags
        4. make dict
    5. make list

    """
    poi_id = []
    return poi_id


def parse_id(id):
    """
    Parse id, turn it to dict with only needed keys
    """
    poi_list = []
    return poi_list

if __name__ == '__main__':
    generate_html('bla bla', 'bla bla')

