import pandas as pd
from Connection import pro_connect
from SqlAlchemyConnection import connection_production

production = pro_connect()
if production.open:
    cur = production.cursor()

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', None)

excel = pd.read_excel("G:\PRAXIA\isabel-9.5,22\MAIN_ROL.xlsx")
excel['Drug Name'] = excel['Drug Name'].str.strip()
excel['Drug Code'] = excel['Drug Code'].str.strip()
ot_excel = excel.rename(columns={'Drug Name': 'ITNAME', 'Drug Code': 'ID'})

op_item = pd.read_sql_query("SELECT ID, ITNAME, CSCART_PRODUCT_ID FROM cscart_HOSPITAL_ITEMS where"
                            " HOSPITAL_ID=97", con=pro_connect())
excel_item = pd.merge(left=ot_excel, right=op_item, on='ID', how='left', indicator=True)
excel_item = excel_item.drop_duplicates(subset='ID')
excel_item1 = excel_item[excel_item['_merge'] == 'both']
excel_item2 = excel_item[excel_item['_merge'] == 'left_only']
# excel_item2.to_excel("G:/isabel_left_MAIN_items.xlsx")
excel_item1 = excel_item1.rename(columns={'ITNAME_x': 'ITNAME', 'ROL': 'REORDER_LEVEL', 'ROQ': 'quantity_ordered'})
hospital_item = excel_item1[['ID', 'ITNAME', 'CSCART_PRODUCT_ID', 'REORDER_LEVEL']]
hospital_item['HOSPITAL_ID'] = 97
hospital_item['CSCART_PRODUCT_ID'] = hospital_item['CSCART_PRODUCT_ID'].astype('Int64')
# with connection_production().connect() as con:
#     hospital_item.to_sql("cscart_HOSPITAL_ITEMS", if_exists="append", index=False, con=con)
# print('hospital items uploaded')

product_sub = excel_item1[['CSCART_PRODUCT_ID', 'quantity_ordered']]
product_sub = product_sub.rename(columns={'CSCART_PRODUCT_ID': 'product_id'})
product_sub['user_id'] = 517
product_sub['is_active'] = 1
product_sub['product_id'] = product_sub['product_id'].astype('Int64')
# with connection_production().connect() as con:
#     product_sub.to_sql("cscart_products_subscription", if_exists="append", index=False, con=con)
# print('pro_sub uploaded')

left_main_ot = pd.read_excel("G:\isabel_left_MAIN_items.xlsx")
item_master = pd.read_sql_query("SELECT Carepact_Item_Id, Carepact_Item_Name as ITNAME FROM "
                                "cscart_Carepact_Item_Masters", con=pro_connect())
left_item = pd.merge(left=left_main_ot, right=item_master, on='ITNAME', how='left', indicator=True)
left_item1 = left_item[left_item['_merge'] == 'both']
left_item2 = left_item[left_item['_merge'] == 'left_only']
mapping = pd.read_sql_query("SELECT Cscart_Id as CSCART_PRODUCT_ID,Carepact_Item_Id"
                            " FROM Carepact_Cscart_Mapping", con=pro_connect())
item_map = pd.merge(left=left_item1, right=mapping, on='Carepact_Item_Id').drop_duplicates()
hospital_item = item_map[['ID', 'ITNAME', 'CSCART_PRODUCT_ID', 'REORDER_LEVEL']]
hospital_item['HOSPITAL_ID'] = 97
hospital_item['CSCART_PRODUCT_ID'] = hospital_item['CSCART_PRODUCT_ID'].astype('Int64')
# with connection_production().connect() as con:
#     hospital_item.to_sql("cscart_HOSPITAL_ITEMS", if_exists="append", index=False, con=con)
# print('hospital items uploaded')
product_sub = item_map[['CSCART_PRODUCT_ID', 'quantity_ordered']]
product_sub = product_sub.rename(columns={'CSCART_PRODUCT_ID': 'product_id'})
product_sub['user_id'] = 517
product_sub['is_active'] = 1
product_sub['product_id'] = product_sub['product_id'].astype('Int64')
# with connection_production().connect() as con:
#     product_sub.to_sql("cscart_products_subscription", if_exists="append", index=False, con=con)
# print('pro_sub uploaded')