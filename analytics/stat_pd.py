# -*- coding: utf-8 -*-
import pandas as pd
import importlib


def output_formatted (frame):
   grouped = frame.groupby('CAT4')
   for key, group in grouped:
      print(f"{key}\n=====\n")
      for app_no, app_no_group in group.groupby('CAT3'):
         print ("     " + app_no + "\n     =====\n")
         for _, row in app_no_group.iterrows():
            row = row.drop(['CAT3', 'CAT4'])
            print (row.values.flatten().tolist())


def process_csv(filename):
   df = pd.read_csv("source_table.csv", keep_default_na=False, 
               names=['CAT1', 'CAT2', 'CAT3', 
                      'CAT4', 'KEYWORD', 'TEXT', 
                      'PRICE', 'PRICE_PER_1M2', 
                      'CURRENCY', 'FLOOR', 'FLOOR_TOTAL', 
                      'SQUARE_TOTAL', 'SQUARE_LIVE', 
                      'SQUARE_KITCHEN', 'NEW_BUILD', 
                      'LIVING_CONDITION', 'CONTACT'],
               )

   df = df.loc[ (df['CAT1'].isin (['Нерухомість', 'Недвижимость'])) & 
               ( df['CAT2'].isin(['Квартири і кімнати. Продам.', 'Квартиры и комнаты. Продам']) ) &  
                  df['CAT3'].isin(['101: Квартири 1-кімнатні', '101: Квартиры 1-комнатные',
                              '102: Квартири 2-кімнатні', '102: Квартиры 2-комнатные',                                    
                              '103: Квартири 3-кімнатні', '103: Квартиры 3-комнатные',
                              '104: Квартири 4-кімнатні', '104: Квартиры 4-комнатные',
                              '105: Квартири багатокімнатні', '105: Квартиры многокомнатные'])
   ]

   df = df.apply(lambda x : pd.to_numeric(x) if x.name in [
      'SQUARE_TOTAL',
      'PRICE_PER_1M2',
      'PRICE_PER_1M2',
      'PRICE'] else x)

   fvm = importlib.import_module("filters.90k_newb")

   df = df.loc[df['CAT3'].isin(fvm.filters['cat3']) &
               df['NEW_BUILD'].isin(fvm.filters['new_build']) &
               df['CAT4'].isin(fvm.filters['cat4'])
   ]

   df = df.loc[(df['SQUARE_TOTAL'] != None) & (df['SQUARE_TOTAL'] < fvm.filters['sq_total_max'])
               & (
                  (df['PRICE_PER_1M2'] != None)
                  & (
                     ( (df['CURRENCY'] == 'USD') & (df['PRICE_PER_1M2'] < fvm.filters['price_per_1m2_usd']) ) | 
                     ( (df['CURRENCY'] == 'UAH') & (df['PRICE_PER_1M2'] < fvm.filters['price_per_1m2_uah']) )
                  )
                  & (
                  ( (df['CURRENCY']=='USD') & (df['PRICE'] < fvm.filters['price_usd'])) | 
                  ( (df['CURRENCY']=='UAH') & (df['PRICE'] < fvm.filters['price_uah']))
                  )
               )
               ]
   df = df.drop(['CAT1', 'CAT2'], axis=1)
   return df 


if __name__ == '__main__':
   frame = process_csv("source_table.csv")
   output_formatted(frame)



