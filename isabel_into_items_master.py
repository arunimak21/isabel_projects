"""isabel items not in carepact item master"""

import pandas as pd
from Connection import pro_connect
import numpy as np
from SqlAlchemyConnection import connection_production

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', None)

excel = pd.read_excel("G:\PRAXIA\isabel-9.5,22\To be uploaded- matching with carepact master.xlsx")
excel1 = excel.drop_duplicates(subset=['Carepact_Master'])
excel1 = excel1.rename(columns={'Carepact_Master': 'Carepact_Item_Name', 'Recent Purchase Vendor': 'VENDOR_NAME'})
carepact_item_master = pd.read_sql_query("SELECT Carepact_Item_Id,Carepact_Item_Name"
                                  "  FROM cscart_Carepact_Item_Masters", con=pro_connect())
carepact_item_master = carepact_item_master.drop_duplicates(subset=['Carepact_Item_Name'])
excel_carepact = pd.merge(left=excel1, right=carepact_item_master, on=['Carepact_Item_Name', 'Carepact_Item_Id'],
                          how='left', indicator=True)
excel_carepact1 = excel_carepact[excel_carepact['_merge'] == 'left_only']
# excel2 = pd.read_excel("G:/isabel_new_pro_with_carepactid.xlsx")
carepact_cscart_map = pd.read_sql_query("SELECT Carepact_Item_Id, Cscart_Id FROM "
                                        "Carepact_Cscart_Mapping", con=pro_connect())
carepact_cscart_map = carepact_cscart_map.drop_duplicates(subset=['Carepact_Item_Id'])
carepact_cscart = excel_carepact.merge(carepact_cscart_map, on='Carepact_Item_Id', how='left', indicator='exists')
carepact_cscart1 = carepact_cscart[carepact_cscart['exists'] == 'left_only']
# vendor_map2.to_excel("G:/isabel_to_be_uploaded_unknown_vendor_2.xlsx")
carepact_cscart2 = carepact_cscart[carepact_cscart['exists'] == 'both']
carepact_cscart2['Cscart_Id'] = carepact_cscart2['Cscart_Id'].astype('int')
""""""""""""""""""""""""""""""""""""""""""
carepact_cscart3 = carepact_cscart2[['Carepact_Item_Name', 'VENDOR_NAME', 'Rate', 'HSN', 'Cscart_Id']]
# vendor_bill = carepact_cscart2[['Carepact_Item_Name']]
vendor_map = pd.read_sql_query("SELECT cscart_vendor_id as VENDOR_ID, h_vendor_name as VENDOR_NAME"
                               " FROM cscart_HOSPITAL_VENDOR_MAP where hospital_id=93", con=pro_connect())
vendor_map = carepact_cscart3.merge(vendor_map, on='VENDOR_NAME', how='left', indicator='exists')
vendor_map1 = vendor_map[vendor_map['exists'] == 'both']
vendor_map2 = vendor_map[vendor_map['exists'] == 'left_only']
vendor_map1['VENDOR_ID'] = vendor_map1['VENDOR_ID'].astype('int')
vendor_map1 = vendor_map1.rename(columns={'Cscart_Id': 'CSCART_PRODUCT_ID'})
vendor_map1 = vendor_map1.drop(['exists'], axis=1)
vendor_bill = pd.read_sql_query("SELECT VENDOR_NAME, CSCART_PRODUCT_ID FROM "
                                "cscart_VENDOR_BILL_ITEM_MAP", con=pro_connect())
vendor_bill = vendor_bill.drop_duplicates(subset=['CSCART_PRODUCT_ID', 'VENDOR_NAME'])
vendor_bill_item = pd.merge(left=vendor_map1, right=vendor_bill, on=['CSCART_PRODUCT_ID', 'VENDOR_NAME'], how='left',
                            indicator=True)
vendor_bill_item = vendor_bill_item[vendor_bill_item['_merge'] == 'both']
print(vendor_bill_item)
"""into hospital_items"""
carepact_cscart4 = carepact_cscart2.rename(columns={'Cscart_Id': 'CSCART_PRODUCT_ID', 'Carepact_Item_Name': 'ITNAME',
                                             'Item Code': 'ID'})
carepact_cscart4 = carepact_cscart4.drop(['exists', '_merge'], axis=1)
hospital_item = pd.read_sql_query("SELECT * FROM cscart_HOSPITAL_ITEMS where HOSPITAL_ID=93", con=pro_connect())
hospital_item_check = pd.merge(left=carepact_cscart4, right=hospital_item, on=['ID'],
                               how='left', indicator=True)
hospital_item_check1 = hospital_item_check[hospital_item_check['_merge'] == 'left_only']
hospital_item_check = hospital_item_check[['ID', 'ITNAME_x', 'CSCART_PRODUCT_ID_x']]
hospital_item_check['HOSPITAL_ID'] = 93
hospital_item_check = hospital_item_check.rename(columns={'CSCART_PRODUCT_ID_x': 'CSCART_PRODUCT_ID',
                                                          'ITNAME_x': 'ITNAME'})
excel_map1 = hospital_item_check[['ID', 'CSCART_PRODUCT_ID', 'HOSPITAL_ID', 'ITNAME']]
print(excel_map1)
# with connection_production().connect() as con:
#     excel_map1.to_sql("cscart_HOSPITAL_ITEMS", if_exists="append", index=False, con=con)
# print('hospital items uploaded')