# -*- coding: utf-8 -*-
"""
That validator search similar named poi's and returns table which contains
highlighted tag values that does not match the pattern
"""

#TODO: web form to get all the data

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
                         ['operator', 'X5 Retail Group'],
                         ['tag3', 'value3']),
                ):
    #TODO: get garbage out, make unit-test
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
    osm_file_name = './map.osm'
    osm_file = open(osm_file_name, 'r').read()
    element = etree.fromstring(osm_file)

    poi_list = []
    #TODO: make search from children of <osm>, not from <osm>???
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
            poi_list.append(poi)
    print poi_list
    return poi_list


def parse_id(id):
    """
    Parse id, turn it to dict with only needed keys
    """
    poi_list = []
    return poi_list


if __name__ == '__main__':
    name_search()

