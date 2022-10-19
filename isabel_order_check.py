import pandas as pd
from Connection import pro_connect
# from SqlAlchemyConnection import connection_production

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', None)

# order_1 = pd.read_excel("G:\isabel_order.xlsx")
order_2 = pd.read_excel("G:\Isabel_order_genwork_26_5.xlsx")
order_2 = order_2.rename(columns={'product_id': 'CSCART_PRODUCT_ID'})
order_3 = pd.read_excel("G:\PRAXIA\isabel-9.5,22\Book7.xlsx")
order_3 = order_3.rename(columns={'Item Code': 'HOSPITAL_ITEM_ID'})
order_12 = pd.merge(left=order_2, right=order_3, on='CSCART_PRODUCT_ID', how='left', indicator=True)
order_12 = order_12[order_12['_merge'] == 'both']
order_12 = order_12[['CSCART_PRODUCT_ID', 'amount', 'HOSPITAL_ITEM_ID', 'Hospital_Description', 'Carepact_Item_Id',
                     'REORDER_LEVEL', 'reorder_qty']]
stock = pd.read_sql_query("select HOSPITAL_ITEM_ID , QUANTITY, EXPR_DATE from "
                          "cscart_HOSPITAL_INVCONTROL where HOSPITAL_ID=93", con=pro_connect())
order_stock = pd.merge(left=order_12, right=stock, on='HOSPITAL_ITEM_ID', how='left', indicator=True)