# -*- coding: utf-8 -*-
__author__ = 'nedr'

import unittest
from validator import generate_html, name_search


class MyTestCase(unittest.TestCase):
    pattern = (['name', u'Пятёрочка'],
               ['shop', 'convenience'],
               ['operator', 'X5 Retail Group'])

    def test_html_generating(self):
        poi1 = {'name': u'Пятёрочка', 'operator': 'X3 Retail Group', 'shop': 'convenience'}
        poi2 = {'name': u'Пятерочка', 'shop': 'supermarket'}
        poi_list = [poi1, poi2]
        result = generate_html(self.pattern, poi_list)
        needed = open('test/needed_html.html', 'r').read()

        self.assertEqual(result, needed)

    def test_name_search(self):
        result = name_search(self.pattern, 'test/map.osm')
        needed = [{'shop': 'convenience',
                   'id': '1891418809',
                   'name': u'\u041f\u044f\u0442\u0451\u0440\u043e\u0447\u043a\u0430'},
                  {'shop': 'convenience',
                   'id': '2327568854',
                   'name': u'\u041f\u044f\u0442\u0451\u0440\u043e\u0447\u043a\u0430'}]
        self.assertEqual(result, needed)

if __name__ == '__main__':
    unittest.main()
