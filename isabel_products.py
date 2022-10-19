import pandas as pd
from Connection import pro_connect
from SqlAlchemyConnection import connection_production

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', None)

excel = pd.read_excel("G:\PRAXIA\isabel-9.5,22/New Product to be uploaded - not in carepact Master- Vendor Updated.xlsx")
excel = excel.rename(columns={'Hospital Description': 'ITNAME', 'Recent Purchase Vendor': 'VENDOR_NAME',
                              'Item Code': 'ID'})
excel1 = pd.read_excel("G:\PRAXIA\isabel-9.5,22\To be uploaded- matching with carepact master.xlsx")
excel1 = excel1.rename(columns={'Carepact_Master': 'ITNAME', 'Recent Purchase Vendor': 'VENDOR_NAME',
                              'Item Code': 'ID'})
inserted = pd.read_excel("G:\isabel_inserted_items_vendor.xlsx")
inserted1 = pd.merge(left=inserted, right=excel, on='ITNAME', how='right', indicator=True)
inserted1 = inserted1[inserted1['_merge'] == 'both']
inserted1 = inserted1[['ID_y', 'ITNAME', 'VENDOR_NAME', 'Carepact_Item_Id']]
inserted2 = pd.merge(left=inserted, right=excel1, on='Carepact_Item_Id', how='right', indicator=True)
inserted2 = inserted2[inserted2['_merge'] == 'both']
inserted2 = inserted2[['ID_y', 'product', 'VENDOR_NAME', 'Carepact_Item_Id']]
inserted2 = inserted2.rename(columns={'product': 'ITNAME'})
result = inserted1.append(inserted2)

hospital_item = pd.read_sql_query("SELECT ID as ID_y, CSCART_PRODUCT_ID, REORDER_LEVEL FROM cscart_HOSPITAL_ITEMS"
                                  " where HOSPITAL_ID=93", con=pro_connect())
pro_sub = pd.read_sql_query("SELECT product_id as CSCART_PRODUCT_ID, quantity_ordered FROM cscart_products_subscription"
                            " where user_id=424", con=pro_connect())
hospital_sub = pd.merge(left=hospital_item, right=pro_sub, on='CSCART_PRODUCT_ID')
mapping = pd.read_sql_query("SELECT Cscart_Id as CSCART_PRODUCT_ID, Carepact_Item_Id FROM Carepact_Cscart_Mapping",
                            con=pro_connect())
item_mapping = pd.merge(left=hospital_sub, right=mapping, on='CSCART_PRODUCT_ID').drop_duplicates(subset='CSCART_PRODUCT_ID')
result_sub = pd.merge(left=item_mapping, right=result, on='Carepact_Item_Id', how='left', indicator=True)
result_sub = result_sub[['ID_y_y', 'ITNAME', 'Carepact_Item_Id', 'VENDOR_NAME', 'REORDER_LEVEL', 'quantity_ordered']]
result_sub.to_excel("G:/isabel_item_vendor1.xlsx")