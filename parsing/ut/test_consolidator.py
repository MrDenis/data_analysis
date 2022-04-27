import unittest

import sys
sys.path.append('../')

from csv_table_consolidator import FieldConsolidator

def test_consolidator(items, col_unique=0, col_value=1, sep=';'):
   '''returns dict consolidate prefixes splitted by ';' in one field for the same operator
      TODO: sort list of prefixes ?
   '''   
   consolidated_items = FieldConsolidator(items, col_unique, col_value, sep)

   return consolidated_items.result()


class test_consolidate(unittest.TestCase):

   def test_simple (self) :     
      items = [['UKRKS', '67'],
               ['UKRAS', '63'],
               ['UKRUM', '66'],
               ['UKRKS', '97'],
               ['UKRUM', '50'],
              ]

      result = test_consolidator(items)

      self.assertEqual(len(result), 3)  # 3 mobile operators in source list

      self.assertEqual(result['UKRKS'], '67;97')
      self.assertEqual(result['UKRUM'], '66;50')
      self.assertEqual(result['UKRAS'], '63')

   # this test has nothing to conslidate
   def test_when_no_agg (self) :

      items = [['UKRKS', '67'],
               ['UKRUM', '50'],
               ['URKAS', '63']   
              ]

      result = test_consolidator(items)

      self.assertEqual(len(result), 3) 

      self.assertEqual(result['UKRKS'], '67')
      self.assertEqual(result['UKRUM'], '50')


   # consolidate with other separator
   def test_optional_arg (self) :


      items = [['UKRKS', 'data', '67', 'col3'],
               ['UKRUM', 'data', '50', 'col3'],
               ['UKRAS', 'data', '63', 'col3'],
               ['UKRUM', 'data', '66', 'col3']
              ]

      result = test_consolidator(items, 0, 2, '/')

      self.assertEqual(len(result), 3) 

      self.assertEqual(result['UKRKS'], '67')
      self.assertEqual(result['UKRUM'], '50/66')
      self.assertEqual(result['UKRAS'], '63')



if __name__ == '__main__' :
   unittest.main()


    
