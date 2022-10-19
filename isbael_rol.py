import pandas as pd
from Connection import pro_connect
from SqlAlchemyConnection import connection_production

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', None)

vendor_map = pd.read_sql_query("SELECT ID,ITNAME, CSCART_PRODUCT_ID as product_id,REORDER_LEVEL FROM cscart_HOSPITAL_ITEMS "
                               "where hospital_id=5 ", con=pro_connect())
pro_dub = pd.read_sql_query("select product_id,quantity_ordered FROM cscart_products_subscription where "
                            "user_id=123 and is_active=1", con=pro_connect())
vendor_pro = pd.merge(left=vendor_map, right=pro_dub, on='product_id')
uom = pd.read_sql_query("SELECT product_id,uom_unit FROM cscart_products", con=pro_connect())
pro_uom = pd.merge(left=vendor_pro, right=uom, on='product_id').drop_duplicates(subset='product_id')
print(pro_uom)
# pro_uom.to_excel("G:/isabel_rol_uom.xlsx")