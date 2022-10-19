import pandas as pd
from Connection import pro_connect
from SqlAlchemyConnection import connection_production

"""Out Put Display Setting """
desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', None)

# production server connection
# production = pro_connect()
# cur = production.cursor()

isabel_item = pd.read_excel("G:/PRAXIA/Book2- fuzzy work 1.xlsx")
isabel_items = isabel_item[isabel_item.Similarity == "Matching"]
carepact_items = pd.read_sql_query("SELECT * FROM cscart_Carepact_Item_Masters", con=pro_connect())
isabel_carepact = pd.merge(left=isabel_items, right=carepact_items, on='Carepact_Item_Name')
isabel_carepacts = isabel_carepact.drop_duplicates(subset=['Carepact_Item_Id'], keep='last')
isabel_carepacts = isabel_carepact[['Carepact_Item_Id', 'Carepact_Item_Name', 'Purcahse Vendor']]
carepact_cscart = pd.read_sql_query("SELECT Id, Carepact_Item_Id,Cscart_Id as CSCART_PRODUCT_ID FROM"
                                    " Carepact_Cscart_Mapping", con=pro_connect())
carepact_cscart_id = pd.merge(left=isabel_carepacts, right=carepact_cscart, on='Carepact_Item_Id',
                              how='left', indicator=True)
carepact_cscart_merge = carepact_cscart_id[carepact_cscart_id['_merge'] == 'left_only']
cscart_new = carepact_cscart_merge[['Carepact_Item_Id', 'Carepact_Item_Name']]
cscart_news = pd.merge(left=cscart_new, right=isabel_item, on='Carepact_Item_Name', how='left')
cscart_news = cscart_news[['Carepact_Item_Id', 'Carepact_Item_Name', 'Customer Price']]
vendor_item = pd.read_sql_query("SELECT * FROM cscart_VENDOR_BILL_ITEM_MAP", con=pro_connect())
vendor_carepact = pd.merge(left=carepact_cscart_id, right=vendor_item, on='CSCART_PRODUCT_ID')
vendor_carepacts = vendor_carepact.drop_duplicates(subset=['CSCART_PRODUCT_ID'], keep='last')
vendor_carepact_merge = vendor_carepacts[['VENDOR_ITEM_ID', 'CSCART_PRODUCT_ID','VENDOR_PRODUCT_NAME','Purcahse Vendor',
                                          'LIST_PRICE', 'MRP','CAREPACT_PRICE', 'HSNCODE', 'out_of_stock']]
vendor_carepact_merge.rename(columns={'Purcahse Vendor': 'VENDOR_NAME'}, inplace=True)
vendor_carepact_merge['VENDOR_ID'] = 425
vendor_merge = vendor_carepact_merge[['VENDOR_ID', 'VENDOR_ITEM_ID','VENDOR_NAME', 'CSCART_PRODUCT_ID','VENDOR_PRODUCT_NAME',
                                      'LIST_PRICE', 'MRP','CAREPACT_PRICE', 'HSNCODE', 'out_of_stock']]
# with connection_production().connect() as con:
#      vendor_merge.to_sql("cscart_VENDOR_BILL_ITEM_MAP", if_exists="append", index=False, con=con)
hospital_item = pd.read_sql_query("SELECT * FROM cscart_HOSPITAL_ITEMS", con=pro_connect())
hospital_vendorbill = pd.merge(left=vendor_merge, right=hospital_item, on='CSCART_PRODUCT_ID')
hospital_vendorbills = hospital_vendorbill.drop_duplicates(subset=['CSCART_PRODUCT_ID'], keep='last')
hospital_id = hospital_vendorbills[['ID', 'CSCART_PRODUCT_ID', 'ITNAME', 'REORDER_LEVEL']]
hospital_id['HOSPITAL_ID'] = 93
hospital_id = hospital_id[['ID', 'CSCART_PRODUCT_ID', 'HOSPITAL_ID', 'ITNAME', 'REORDER_LEVEL']]

# hospital_id.dropna(subset=['ID'])
# with connection_production().connect() as con:
#       hospital_id.to_sql("cscart_HOSPITAL_ITEMS", if_exists="append", index=False, con=con)
