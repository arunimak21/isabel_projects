import pandas as pd
from Connection import pro_connect
from SqlAlchemyConnection import connection_production

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', None)

def hospital():
    hospital_item = pd.read_sql_query("SELECT * FROM cscart_HOSPITAL_VENDOR_MAP"
                                      " where hospital_id=93", con=pro_connect())
    return hospital_item
def Vendor_map():
    hospital_item = hospital()
    hospital_item = hospital_item[['hospital_vendor_id', 'cscart_vendor_id', 'h_vendor_name']]
    hospital_item['hospital_id'] = 98
    hospital_item['cscart_customer_id'] = 518
    # with connection_production().connect() as con:
    #     hospital_item.to_sql("cscart_HOSPITAL_VENDOR_MAP", if_exists="append", index=False, con=con)
    # print('cscart_HOSPITAL_VENDOR_MAP uploaded')
    return hospital_item

def vendor_score():
    hospital_item = hospital()
    hospital_item = hospital_item.rename(columns={'cscart_vendor_id': 'vendor_id'})
    hospital_item['carepact_score'] = 1
    hospital_item['hospital_id'] = 98
    hospital_item['total_score'] = 25
    hospital_item = hospital_item[['hospital_id', 'vendor_id', 'carepact_score', 'total_score']]

    # with connection_production().connect() as con:
    #     hospital_item.to_sql("cscart_VENDOR_SCORE", if_exists="append", index=False, con=con)
    # print('vendor score uploaded')
    return hospital_item

# vendor_score()

