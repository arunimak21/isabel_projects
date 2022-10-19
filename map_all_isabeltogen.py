import pandas as pd
from Connection import pro_connect
from SqlAlchemyConnection import connection_production

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', None)

vendor_map = pd.read_sql_query("SELECT cscart_vendor_id as VENDOR_ID FROM cscart_HOSPITAL_VENDOR_MAP "
                               "where hospital_id=93 ", con=pro_connect())
vendor_bill = pd.read_sql_query("SELECT * from cscart_VENDOR_BILL_ITEM_MAP", con=pro_connect())
vendor_bill_map = pd.merge(left=vendor_map, right=vendor_bill, on='VENDOR_ID')
vendor_bill_map.drop(vendor_bill_map.index[vendor_bill_map['VENDOR_ID'] == 425], inplace=True)
print(vendor_bill_map)
vendor_bill_map = vendor_bill_map[['VENDOR_ITEM_ID', 'CSCART_PRODUCT_ID',
                                   'VENDOR_PRODUCT_NAME', 'LIST_PRICE', 'MRP', 'CAREPACT_PRICE', 'HSNCODE']]
vendor_bill_map['VENDOR_NAME'] = 'Genworks Health Pvt. Ltd.'
vendor_bill_map['VENDOR_ID'] = 425
vendor_bill_map = vendor_bill_map[['VENDOR_ID', 'VENDOR_ITEM_ID', 'VENDOR_NAME', 'CSCART_PRODUCT_ID',
                                   'VENDOR_PRODUCT_NAME', 'LIST_PRICE', 'MRP', 'CAREPACT_PRICE', 'HSNCODE']]
print(vendor_bill_map)

# with connection_production().connect() as con:
#        vendor_bill_map.to_sql("cscart_VENDOR_BILL_ITEM_MAP", if_exists="append", index=False, con=con)
# print('done')