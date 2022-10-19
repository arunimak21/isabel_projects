import pandas as pd
from Connection import pro_connect
from SqlAlchemyConnection import connection_production

production = pro_connect()
if production.open:
    cur = production.cursor()

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', None)

excel = pd.read_excel("G:\PRAXIA\isabel-9.5,22/active_vendor.xlsx")
excel['ID'] = excel['ID'].str.strip()
excel = excel.drop_duplicates(subset=['ID', 'Vendor'])
vendor_id = pd.read_sql_query("SELECT cscart_vendor_id as VENDOR_ID, h_vendor_name as Vendor"
                              " FROM cscart_HOSPITAL_VENDOR_MAP where hospital_id=93", con=pro_connect())
excel_vendor = pd.merge(left=excel, right=vendor_id, on='Vendor', how='left', indicator=True)
excel_vendor1 = excel_vendor[excel_vendor['_merge'] == 'both']
excel_vendor2 = excel_vendor[excel_vendor['_merge'] == 'left_only']
# excel_vendor2.to_excel("G:/isabel_unknown_vendor.xlsx")
excel_vendor1 = excel_vendor1.drop(['_merge'], axis=1)
isabel_item = pd.read_sql_query("SELECT ID, ITNAME, CSCART_PRODUCT_ID FROM cscart_HOSPITAL_ITEMS where"
                            " HOSPITAL_ID=93", con=pro_connect())
isabel_vendor = pd.merge(left=excel_vendor1, right=isabel_item, on='ID')
isabel_vendor['VENDOR_ID'] = isabel_vendor['VENDOR_ID'].astype('Int64')
vendor_bill = pd.read_sql_query("SELECT * FROM cscart_VENDOR_BILL_ITEM_MAP where VENDOR_ID!=426 and"
                                " VENDOR_ID between 425 and 510",
                                con=pro_connect()).drop_duplicates(subset='CSCART_PRODUCT_ID', keep='first')
print(vendor_bill.loc[vendor_bill['VENDOR_ITEM_ID'] == 'DEC003 '])
vendor_update = pd.merge(left=isabel_vendor, right=vendor_bill, on='CSCART_PRODUCT_ID')
print(vendor_update)
# vendor_update = vendor_update[['id', 'ITNAME', 'CSCART_PRODUCT_ID', 'Vendor', 'VENDOR_ID_x']]
# print(vendor_update)
#
#
# for index, row in vendor_update.iterrows():
#     print(index, row)
#     cur.execute("update cscart_VENDOR_BILL_ITEM_MAP set VENDOR_NAME = %s where CSCART_PRODUCT_ID = %s"
#                 " and id = %s",
#                 (row['Vendor'], row['CSCART_PRODUCT_ID'], row['id']))
#     production.commit()
# print('done')


# hospital_items = pd.read_sql_query("SELECT * FROM cscart_HOSPITAL_ITEMS where HOSPITAL_ID=93", con=pro_connect())
# pro_sub = pd.read_sql_query("SELECT product_id as CSCART_PRODUCT_ID,quantity_ordered FROM cscart_products_subscription"
#                             " where user_id=424", con=pro_connect())
# hospital_sub = pd.merge(left=hospital_items, right=pro_sub, on='CSCART_PRODUCT_ID')
# hospital_sub.to_excel("G:/isabel_OP_RLRQ.xlsx")