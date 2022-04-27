
import unittest
import sys

sys.path.append('../')

from splitter import Splitter

def test_txt_splitter(items, column):
   '''returns subtotals per each month group''' 
   splitter = Splitter(items, column)
   subtotals = []

   for name, grouped_items in splitter :
      subtotals.append ({name:len(grouped_items)})

   return subtotals


# missing month report is validated by grouped month subtotals
class TestSplitter(unittest.TestCase):

   def test_3_groups (self):
      items = [ ['Zimbabwe',   '263', '99x', 'Fake', ],
                ['Zimbabwe',   '263', '98x', 'Fake2', ],
                ['Uzbekistan', '998', '90', 'Beeline'],
                ['Uzbekistan', '998', '97', 'MTS'],
                ['Uzbekistan', '998', '93', 'UCell'],
                ['Uzbekistan', '998', '94', 'UCell'],
                ['Uzbekistan', '998', '94', 'UCell'],
                ['Uruguay',    '598', '99', 'Ancel'],
              ]

      # group by column 'country name', index=0
      result = test_txt_splitter(items, 0)
      # list groups returned by splitter: Zimbabwe 2 records, Uzbekistan 5, Uruguay 1
      self.assertEqual([{'Zimbabwe':2},{'Uzbekistan':5},{'Uruguay':1}], result)


   def test_1_group (self):
      items = [ ['Zimbabwe',   '263', '99x', 'Fake', ],
                ['Zimbabwe',   '263', '98x', 'Fake2', ],
                ['Zimbabwe',   '263', '97x', 'Fake2', ],
              ]


      result = test_txt_splitter(items, 0)

      # result is one group with 3 items
      self.assertEqual([{'Zimbabwe':3}], result)

   def test_4_groups_one_line (self):
      items = [ ['Zimbabwe',   '263', '99x', 'Fake', ],
                ['Uzbekistan', '998', '90', 'Beeline'],
                ['Uruguay',    '598', '99', 'Ancel'],
                ['Ukraine',    '380', '67', 'Kyivstar'],
              ]

      result = test_txt_splitter(items, 0)
      self.assertEqual([{'Zimbabwe':1},
                        {'Uzbekistan':1},
                        {'Uruguay':1},
                        {'Ukraine':1}], result)


   # list should be sorted by column to group by
   # otherwise wrong result are expected
   def test_unsorted (self):
      items = [ ['Zimbabwe',   '263', '99x', 'Fake', ],
                ['Uzbekistan', '998', '90', 'Beeline'],
                ['Zimbabwe',   '263', '98x', 'Fake2', ],
                ['Uzbekistan', '998', '97', 'MTS'],
                ['Uruguay',    '598', '99', 'Ancel'],
                ['Uzbekistan', '998', '93', 'UCell'],
              ]

      # group by column 'country name', index=0
      result = test_txt_splitter(items, 0)
      # list groups returned by splitter: Zimbabwe 2 records, Uzbekistan 5, Uruguay 1
      self.assertEqual([{'Zimbabwe':1},
                        {'Uzbekistan':1},
                        {'Zimbabwe':1},
                        {'Uzbekistan':1},
                        {'Uruguay':1},
                        {'Uzbekistan':1}
                       ], result)


if __name__ == '__main__' :
   unittest.main()
