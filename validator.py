# -*- coding: utf-8 -*-
"""
That validator search similar named pois and returns table which contains
highlighted tag values that not similar to most others
"""
__author__ = 'nedr'

#TODO: rename 'ideal' variable
#TODO: name search euristics
#TODO: highlight wrong values (to do this, we need to take ideal values)

from lxml import etree
import lxml.html
from lxml.html import builder as E


def generate_html(ideal, poi_list):
    """
    Generates html with table, filled by poi
    """
    tbody = etree.Element('tbody')
    tr_header = etree.SubElement(tbody, 'tr')
    for key in ideal:
        # generate header of table which contains all given keys
        th_header = etree.SubElement(tr_header, 'th')
        th_header.text = key

    for poi in poi_list:
        # generate element tree of poi
        tr = etree.SubElement(tbody, 'tr')
        for key in ideal:
            td = etree.SubElement(tr, 'td')
            td.text = poi.get(key, '')

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
