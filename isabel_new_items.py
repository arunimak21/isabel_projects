"""created 10/5/22 by arunima"""
"""isabel items already in item master but no cscart_id, so for creating product_id,insert datas into vendor_items
 with vendor name and run template creation """

import pandas as pd
from Connection import pro_connect
import numpy as np
from SqlAlchemyConnection import connection_production

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', None)

excel = pd.read_excel("G:\isabel_to_be_uploaded_unknown_vendor.xlsx")
excel1 = excel.drop_duplicates(subset=['Carepact_Item_Id'])
carepact_cscart_map = pd.read_sql_query("SELECT Carepact_Item_Id, Cscart_Id FROM "
                                        "Carepact_Cscart_Mapping", con=pro_connect())
carepact_cscart_map = carepact_cscart_map.drop_duplicates(subset=['Carepact_Item_Id'])
excel_map = pd.merge(left=excel1, right=carepact_cscart_map, on='Carepact_Item_Id', how='left', indicator='exists')
excel_map1 = excel_map[excel_map['exists'] == 'left_only']
excel_map1 = excel_map1[['Carepact_Item_Id', 'Carepact_Item_Name', 'VENDOR_NAME', 'Rate', 'TAX', 'HSN']]
excel_map1 = excel_map1.rename(columns={'Carepact_Item_Name': 'Vendor_Item_Name', 'Rate': 'Price', 'HSN': 'Hsncode',
                                        'VENDOR_NAME': 'Vendor', 'TAX': 'Tax'})
vendor_map = pd.read_sql_query("select cscart_vendor_id as Vendor_Id, h_vendor_name as Vendor from"
                               " cscart_HOSPITAL_VENDOR_MAP where hospital_id=93", con=pro_connect())
vendor_maps = pd.merge(left=excel_map1, right=vendor_map, on='Vendor', how='left', indicator=True)
vendor_mapss = vendor_maps[vendor_maps['_merge'] == 'both']
vendor_mapss['Vendor_Id'] = vendor_mapss['Vendor_Id'].astype('int')
vendor_mapss = vendor_mapss[['Carepact_Item_Id', 'Vendor_Item_Name', 'Vendor', 'Price', 'Tax', 'Hsncode', 'Vendor_Id']]

# with connection_production().connect() as con:
#     vendor_mapss.to_sql("cscart_Carepact_Vendor_Items", if_exists="append", index=False, con=con)

# vendor_mapss.to_excel("G:/isabel_unknown_vendor_products.xlsx")