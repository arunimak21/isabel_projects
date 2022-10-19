import pandas as pd
from Connection import pro_connect

production = pro_connect()
if production.open:
    cur = production.cursor()

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns' , None)

master_itemid = pd.read_excel("G:/PRAXIA/ISABEL/Master for Update - items Uploaded already.xlsx")
master_itemid = master_itemid.rename(columns={'Description': 'VENDOR_PRODUCT_NAME'})
isabel = pd.read_excel("G:/PRAXIA\praxia_carepact.xlsx")
isabel_master = pd.merge(left=master_itemid, right=isabel, on='Description')
# master_itemid['Description'] = master_itemid["Description"].str.replace('[(,)]', '')
carepact_item = pd.read_sql_query("SELECT Carepact_Item_Id,Carepact_Item_Name"
                                  "  FROM cscart_Carepact_Item_Masters", con=pro_connect())
master = pd.merge(left=isabel_master, right=carepact_item, on='Carepact_Item_Name')
carepact_cscart = pd.read_sql_query("SELECT Carepact_Item_Id, Cscart_Id as CSCART_PRODUCT_ID FROM"
                                    " Carepact_Cscart_Mapping", con=pro_connect())
carepact_cscart = pd.merge(left=master, right=carepact_cscart, on='Carepact_Item_Id')
item = pd.read_sql_query("SELECT VENDOR_ID, VENDOR_ITEM_ID, CSCART_PRODUCT_ID, VENDOR_PRODUCT_NAME FROM"
                         " cscart_VENDOR_BILL_ITEM_MAP where VENDOR_ID = 425 ", con=pro_connect())
cscart_item = pd.merge(left=master_itemid, right=item, on='VENDOR_PRODUCT_NAME')
cscart_item = cscart_item[['Item Code', 'VENDOR_PRODUCT_NAME', 'CSCART_PRODUCT_ID', 'VENDOR_ID']]
cscart_item1 = cscart_item.rename(columns={'Item Code': 'VENDOR_ITEM_ID'})
# item['VENDOR_ITEM_ID'] = item['VENDOR_ITEM_ID'].apply(lambda x: "{}{}".format('GEN', x))
# for index, row in cscart_item1.iterrows():
#     sql = 'update cscart_VENDOR_BILL_ITEM_MAP set VENDOR_ITEM_ID = %s where VENDOR_ID =425 and CSCART_PRODUCT_ID = %s'
#     cur.execute(sql, (row['VENDOR_ITEM_ID'], row['CSCART_PRODUCT_ID']))
# production.commit()