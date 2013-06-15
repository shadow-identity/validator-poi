# -*- coding: utf-8 -*-
__author__ = 'nedr'

import unittest
from validator import generate_html


class MyTestCase(unittest.TestCase):
    def test_html_generating(self):
        ideal = 'name', 'tag1', 'tag2', 'tag3'
        poi1 = {'name': 'poi1', 'tag1': 'value1', 'tag2': 'value2'}
        poi2 = {'name': 'poi2', 'tag1': 'value1', 'tag3': 'value3'}
        poi_list = [poi1, poi2]
        result = generate_html(ideal, poi_list)

        needed = '''<html>
<head><title>Table of POI</title></head>
<body>
<h1>Table of POI</h1>
<table><tbody>
<tr>
<th>name</th>
<th>tag1</th>
<th>tag2</th>
<th>tag3</th>
</tr>
<tr>
<td>poi1</td>
<td>value1</td>
<td>value2</td>
<td></td>
</tr>
<tr>
<td>poi2</td>
<td>value1</td>
<td></td>
<td>value3</td>
</tr>
</tbody></table>
</body>
</html>
'''
        self.assertEqual(result, needed)


if __name__ == '__main__':
    unittest.main()
