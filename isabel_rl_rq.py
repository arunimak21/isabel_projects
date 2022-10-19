import pandas as pd
from Connection import pro_connect
from SqlAlchemyConnection import connection_production

production = pro_connect()
if production.open:
    cur = production.cursor()

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', None)

excel = pd.read_excel("G:\PRAXIA\isabel-9.5,22\MAIN_ROL.xlsx")
excel['Drug Name'] = excel['Drug Name'].str.strip()
excel['Drug Code'] = excel['Drug Code'].str.strip()

excel = excel.rename(columns={'Drug Name': 'ITNAME', 'Drug Code': 'ID', 'ROL': 'REORDER_LEVEL',
                              'ROQ': 'quantity_ordered'})
excel['REORDER_LEVEL'] = excel['REORDER_LEVEL'].astype('Int64')
excel['quantity_ordered'] = excel['quantity_ordered'].astype('Int64')

hospital_items = pd.read_sql_query("SELECT * FROM cscart_HOSPITAL_ITEMS where HOSPITAL_ID=93", con=pro_connect())
hospital_item = pd.merge(left=excel, right=hospital_items, on=['ID'], how='left', indicator=True)
hospital_item1 = hospital_item[hospital_item['_merge'] == 'both']
print(hospital_item1.loc[hospital_item1['ID'] == 'MAG014'])
print(hospital_item1.loc[hospital_item1['ID'] == 'CLE003'])

# hospital_item1.to_excel("G:/no_items.xlsx")
hospital_item1 = hospital_item1.rename(columns={'REORDER_LEVEL_x': 'REORDER_LEVEL', 'ITNAME_y': 'ITNAME',
                                                'product_id': 'CSCART_PRODUCT_ID'})
# hospital_item['HOSPITAL_ID'] = hospital_item['HOSPITAL_ID'].astype('Int64')
hospital_item1['CSCART_PRODUCT_ID'] = hospital_item1['CSCART_PRODUCT_ID'].astype('Int64')
hospital_item1['HOSPITAL_ID'] = hospital_item1['HOSPITAL_ID'].astype('Int64')
hospital_item1 = hospital_item1[['ID', 'CSCART_PRODUCT_ID', 'ITNAME', 'REORDER_LEVEL', 'quantity_ordered']]
hospital_item1['HOSPITAL_ID'] = 93
print(hospital_item1)

# for index, row in hospital_item1.iterrows():
#     cur.execute("update cscart_HOSPITAL_ITEMS set REORDER_LEVEL = %s where ID = %s and CSCART_PRODUCT_ID = %s "
#                 "and HOSPITAL_ID = %s",
#                 (row['REORDER_LEVEL'], row['ID'], row['CSCART_PRODUCT_ID'], row['HOSPITAL_ID']))
#     production.commit()
# print('done')
# #
pro_sub = pd.read_sql_query("SELECT * FROM cscart_products_subscription where user_id=424", con=pro_connect())
hospital_item1 = hospital_item1.rename(columns={'CSCART_PRODUCT_ID': 'product_id'})
# hospital_item1 = hospital_item1.drop(['_merge'], axis=1)
pro_subs = pd.merge(left=hospital_item1, right=pro_sub, on='product_id', how='left', indicator=True)
pro_subs['user_id'] = 424
pro_subs = pro_subs[['user_id', 'product_id', 'quantity_ordered_x']]
pro_subs['product_id'] = pro_subs['product_id'].astype('Int64')
#
# for index, row in pro_subs.iterrows():
#     cur.execute("update cscart_products_subscription set quantity_ordered = %s where product_id = %s and user_id = %s",
#                 (row['quantity_ordered_x'], row['product_id'], row['user_id']))
#     production.commit()
# print('done')