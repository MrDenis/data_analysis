

class Splitter:
   '''iterator that groups table by some txt field '''
   def __init__(self, items, column=0):
      self._items = items
      self._col = column  
      self._b = 0             #begin index in items list for current group
      self._e = len(items)    #end index in items list

   def __iter__(self):
      return self

   def __next__(self):
      if self._b >= self._e:
         raise StopIteration

      field = None
      n = 0 

      for i in self._items[self._b:self._e]:
         if not field:
            field = i[self._col]             
         elif field != i[self._col]:
            break 
         n = n + 1  

      #return values
      b = self._b
      #init variables for next iteration
      self._b = b + n  
      return self._items[b][self._col], self._items[b:b+n]
