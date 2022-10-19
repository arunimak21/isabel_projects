import pandas as pd
from Connection import pro_connect
from SqlAlchemyConnection import connection_production

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', None)

cscart_user = pd.read_sql_query("select user_id, company_id, company from cscart_users where user_type='V' "
                                "and user_id >= '477' order by user_id desc", con=pro_connect())
cscart_companies = pd.read_sql_query("select company_id, company from cscart_companies order by company_id desc",
                                     con=pro_connect())
cscart_user['hospital_id'] = 93
cscart_user['cscart_customer_id'] = 424
cscart_user['hospital_vendor_id'] = 0
cscart_user = cscart_user.rename(columns={'user_id': 'cscart_vendor_id', 'company': 'h_vendor_name'})
cscart_hospital_vendor_map = cscart_user[['hospital_id', 'cscart_customer_id', 'hospital_vendor_id',
                                          'cscart_vendor_id', 'h_vendor_name']]
cscart_hospital_vendor_map = cscart_hospital_vendor_map.sort_values(by='cscart_vendor_id', ascending=True)
# with connection_production().connect() as con:
#        cscart_hospital_vendor_map.to_sql("cscart_HOSPITAL_VENDOR_MAP", if_exists="append", index=False, con=con)