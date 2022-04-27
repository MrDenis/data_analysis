import sys
#sys.path.append('../')

from splitter import Splitter 
from optparse import OptionParser, OptionError
#from options import check_required

import csv
import os


class Options(OptionParser):

   def __init__(self):
      OptionParser.__init__(self)

      self.add_option('-s', '--source-file', dest='src_file', help="mobile operator's csv file to consolidate")
      self.add_option('-o', '--output-file', dest='out_file', help='resulted consolidated file')


   def parse(self, argv):
      (opts, args) = OptionParser.parse_args(self, argv[1:])
     
      check_required(opts, 'src_file')

      self.__dict__.update(opts.__dict__)

     
class FieldConsolidator:
   ''' as input get table, column on that group should be done, column which values should be 
       consolidated with separator
       returns dictionary: key; consolidated value
   ''' 
   def __init__(self, table, 
                column_key=0, column_value=1, separator=';'):

      self._table = table
      self._col_key = column_key
      self._col_value = column_value
      self._sep = separator

   def result(self):
     result = {}
     for row in self._table:
        key = row[self._col_key]
        value = row[self._col_value]
        if key in result: 
            result[key] = self._sep.join([result[key], value])
        else:
            result[key] = value      

     return result
      

PREF_COUNTRY_NAME, PREF_DIALLED, PREF_CODES, PREF_MSN, PREF_OPERATOR_NAME = range (0,5)
   
def process(csv_table):
   ''' function takes csv reader oboject, performs consolidation and returns result list 
       format is:
       country name=0, country dialled code=1, prefix=2, msn=3, operator name=4
   '''

   target_csv = []

   # group by country name
   splitter = Splitter(csv_table, column=PREF_COUNTRY_NAME)

   for country_name, items in splitter:
      # consolidate table that related to one country 
      consolidated_items = FieldConsolidator(items, column_key=PREF_OPERATOR_NAME, column_value=PREF_CODES)
      result = consolidated_items.result()

      # group by operator name
      splitter_pmn = Splitter(items, column=PREF_OPERATOR_NAME)

      for operator_name, pmn_items in splitter_pmn :
         target_line = pmn_items[0]
         target_line[2] = result[operator_name]
         target_csv.append(target_line)

   return target_csv 



def open_csv(filename, skip_header=False, delimiter_value=','):
   '''opens csv file and put all contents to list'''

   csv_table = []

   file_in = csv.reader(open(filename,'r'), delimiter=delimiter_value)

   if skip_header: 
      file_in.next()

   for row in file_in:
      csv_table.append(row)
      
   return csv_table


def write_csv(rows, filename):

   csv_output = open(filename, "w")
   wr = csv.writer(csv_output, quoting=csv.QUOTE_ALL)
   wr.writerows(rows) 
   csv_output.close()


def main(argv):

   opts = Options()
   opts.parse(argv)
          
   filename = opts.src_file
   out_file = opts.out_file

   if not out_file: 
      out_file = 'target_' + filename

   csv_table = open_csv(filename)

   result_data = process(csv_table)

   write_csv(result_data, out_file)
 

if __name__ == '__main__':
   sys.exit(main(sys.argv))












   








