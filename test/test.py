# -*- coding: utf-8 -*-
__author__ = 'nedr'

import unittest
from validator import generate_html, name_search, create_josm_url
from lxml import etree


class MyTestCase(unittest.TestCase):
    pattern = (['name', u'Пятёрочка'],
               ['shop', 'convenience'],
               ['operator', 'X5 Retail Group'],
               )  # ideal set of items
    osm_file_name = 'test/map.osm'  # example osm xml

    def test_html_generating(self):
        poi1 = {'name': u'Пятёрочка', 'operator': 'X3 Retail Group', 'shop': 'convenience', 'josm_url': 'http://localhost:8111/load_object?objects=n2327568854'}
        poi2 = {'name': u'Пятерочка', 'shop': 'supermarket', 'josm_url': 'http://localhost:8111/load_object?objects=n2327568854'}
        poi_list = [poi1, poi2]
        result = generate_html(self.pattern, poi_list)
        needed = open('test/needed_html.html', 'r').read()
        self.assertEqual(result, needed)

    def test_name_search(self):
        result = name_search(self.pattern, self.osm_file_name)
        needed = [{'shop': 'convenience',
                   'id': '1891418809',
                   'name': u'\u041f\u044f\u0442\u0451\u0440\u043e\u0447\u043a\u0430',
                   'josm_url': 'http://localhost:8111/load_object?objects=n1891418809'},
                  {'shop': 'convenience',
                   'id': '2327568854',
                   'name': u'\u041f\u044f\u0442\u0451\u0440\u043e\u0447\u043a\u0430',
                   'josm_url': 'http://localhost:8111/load_object?objects=n2327568854'}]
        self.assertEqual(result, needed)

    def test_create_josm_url(self):
        osm_file = open('test/create_urls_test.osm', 'r').read()
        element = etree.fromstring(osm_file)
        result = [create_josm_url(poi) for poi in element]
        needed = ['http://localhost:8111/load_object?objects=n1891418809',
                  'http://localhost:8111/load_object?objects=w62128239',
                  'http://localhost:8111/load_object?objects=r1861067']
        self.assertEqual(result, needed)


if __name__ == '__main__':
    unittest.main()
