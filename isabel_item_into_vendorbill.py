import pandas as pd
from Connection import pro_connect
from SqlAlchemyConnection import connection_production

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', None)

excel = pd.read_excel("G:\PRAXIA/isabel-9.5,22/New Product to be uploaded - not in carepact Master- Vendor Updated.xlsx")
excel = excel[['Item Code', 'Hospital Description', 'Recent Purchase Vendor']]
excel = excel.rename(columns={'Hospital Description': 'Carepact_Item_Name', 'Recent Purchase Vendor': 'VENDOR_NAME'})
carepact_item_master = pd.read_sql_query("SELECT Carepact_Item_Id,Carepact_Item_Name"
                                  "  FROM cscart_Carepact_Item_Masters", con=pro_connect())
carepact_item_master = carepact_item_master.drop_duplicates(subset=['Carepact_Item_Id'])
master = pd.merge(left=excel, right=carepact_item_master, on='Carepact_Item_Name', how='left', indicator=True)
master = master[master['_merge'] == 'both']
carepact_cscart = pd.read_sql_query("SELECT Carepact_Item_Id, Cscart_Id as CSCART_PRODUCT_ID FROM"
                                    " Carepact_Cscart_Mapping", con=pro_connect())
carepact_cscart = pd.merge(left=master, right=carepact_cscart, on='Carepact_Item_Id')
cscart_HOSPITAL_VENDOR_MAP = pd.read_sql_query("SELECT cscart_vendor_id as VENDOR_ID,h_vendor_name as VENDOR_NAME "
                                 "FROM cscart_HOSPITAL_VENDOR_MAP", con=pro_connect())
cscart_HOSPITAL_VENDOR_MAP = pd.merge(left=carepact_cscart, right=cscart_HOSPITAL_VENDOR_MAP, on='VENDOR_NAME')
vendor_bill_item = pd.read_sql_query("SELECT CSCART_PRODUCT_ID, VENDOR_PRODUCT_NAME FROM"
                         " cscart_VENDOR_BILL_ITEM_MAP", con=pro_connect())
vendor_bill_item = vendor_bill_item.drop_duplicates(subset='CSCART_PRODUCT_ID', keep='last')
vendor_bill_items = pd.merge(left=cscart_HOSPITAL_VENDOR_MAP, right=vendor_bill_item, on='CSCART_PRODUCT_ID')
vendor_bill_items = vendor_bill_items.rename(columns={'Item Code': 'VENDOR_ITEM_ID'})
vendor_bill_items = vendor_bill_items[['VENDOR_ID', 'VENDOR_ITEM_ID', 'VENDOR_NAME',
                                       'CSCART_PRODUCT_ID', 'VENDOR_PRODUCT_NAME']]
# with connection_production().connect() as con:
#        vendor_bill_items.to_sql("cscart_VENDOR_BILL_ITEM_MAP", if_exists="append", index=False, con=con)