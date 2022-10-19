import pandas as pd
from Connection import pro_connect

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', None)

production = pro_connect()
if production.open:
    cur = production.cursor()

gen_pro = pd.read_sql_query("SELECT id, CSCART_PRODUCT_ID as Cscart_Id, VENDOR_PRODUCT_NAME, VENDOR_ID, VENDOR_NAME"
                            " FROM cscart_VENDOR_BILL_ITEM_MAP where VENDOR_ID != 426 and"
                            " VENDOR_ID between 425 and 510 order by id desc", con=pro_connect())
gen_pros = gen_pro.groupby(['VENDOR_ID'])['Cscart_Id']
print(gen_pros)
mapping = pd.read_sql_query("SELECT * FROM Carepact_Cscart_Mapping", con=pro_connect())
id_mapping = pd.merge(left=gen_pro, right=mapping, on='Cscart_Id')
item_id = pd.read_sql_query("SELECT Carepact_Item_Id, Carepact_Item_Name FROM cscart_Carepact_Item_Masters",
                            con=pro_connect())
item_id = pd.merge(left=id_mapping, right=item_id, on='Carepact_Item_Id')

# cursor = cur.cursor()
# for index, row in gen_item_id1.iterrows():
#     print(index, row)
#     cur.execute('''DELETE FROM cscart_VENDOR_BILL_ITEM_MAP WHERE id =%s and CSCART_PRODUCT_ID=%s''',
#                 (row['id'], row['Cscart_Id']))
#     production.commit()
# print('done')