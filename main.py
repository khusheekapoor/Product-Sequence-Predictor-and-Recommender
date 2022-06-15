# importing libraries
import numpy as np
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from fastapi import FastAPI
import uvicorn

# creating FastAPI app for deployment
app = FastAPI()

# reading datasets
item = pd.read_csv('C:/Users/khush/mini_project/item.csv')
customer = pd.read_csv('C:/Users/khush/mini_project/customer.csv')
order = pd.read_csv('C:/Users/khush/mini_project/order.csv')
product = pd.read_csv('C:/Users/khush/mini_project/product.csv')
review = pd.read_csv('C:/Users/khush/mini_project/review.csv')

# merging items and orders datasets
item = item.merge(order, on='order_id', how='inner') 
# merging items and products dataset for apriori analysis
df_apriori = item.merge(product[['product_id','product_category_name_english']], on='product_id', how='left') 
# creating a copy of the apriori dataset
df_ap = df_apriori 
# merging items and cutsomers dataset
item_cust = item.merge(customer, on='customer_id', how='left') 

# list to store output
reccomend_prods = []

'''
this function recommends the top 5 products overall in case of cold start
'''
def cold_start():
    item = pd.read_csv('C:/Users/khush/mini_project/item.csv')
    df_cold = item.merge(review, on='order_id', how='inner')
    df_cold = df_cold.sort_values(by='review_score')
    reccomend_prods = list(df_cold.product_id.values[0:5])
    return reccomend_prods

'''
this function recommends the top 5 products of the consequent category obtained using apriori algorithm
hence promoting cross-selling
'''
def prod_rec():
    df_apriori = item.merge(product[['product_id','product_category_name_english']], on='product_id', how='left')
    df_apriori = df_apriori.dropna(subset=['product_category_name_english'])
    # obtaining transactions
    total_transactions = df_apriori.groupby('order_id').product_category_name_english.unique()
    total_transactions_list = total_transactions.tolist()
    # encoding transactions
    encoder = TransactionEncoder()
    category_column_data = encoder.fit_transform(total_transactions_list)
    category_column_data = pd.DataFrame(category_column_data, columns = encoder.columns_)
    # clubbing similar categories together
    category_column_data['books'] = category_column_data['books_imported'] | category_column_data['books_technical']
    category_column_data['sports_leisure_health_beauty'] = category_column_data['sports_leisure'] & category_column_data['health_beauty']
    category_column_data['sports_leisure_health_beauty'] = category_column_data['sports_leisure'] & category_column_data['health_beauty']
    # finding frequent itemsets
    frequent_item_sets = apriori(category_column_data, use_colnames = True, min_support = 0.00005, max_len = 2)
    # generating association rules
    association_rule = association_rules(frequent_item_sets, metric = 'lift', min_threshold = 1)
    # preprocessing text for further use
    association_rule["antecedents"] = association_rule["antecedents"].apply(lambda x: ', '.join(list(x))).astype("unicode")
    association_rule["consequents"] = association_rule["consequents"].apply(lambda x: ', '.join(list(x))).astype("unicode")
    return association_rule

'''
this function creates a chain of products obtained using markov models and apriori algorithm
if the user has bought a product which is a part of the chain, we recommend the remaining products in the chain
'''
def chain_rec():
    item = pd.read_csv('C:/Users/khush/mini_project/item.csv')
    item = item.merge(order, on='order_id', how='inner')
    # keeping only those products which have been bought by atleat 50 users to increase space efficiency
    item_freq = item['product_id'].value_counts()
    item = item[item.isin(item_freq.index[item_freq >= 50]).values]
    item['quantity'] = 1
    # finding baskets
    basket = (item.groupby(['order_id','product_id'])['quantity']).sum().unstack().reset_index().fillna(0).set_index('order_id')
    def encode_units(x):
        if x<= 0:
            return 0
        if x>=1:
            return 1    
    basket_sets = basket.applymap(encode_units)
    # finding frequent itemsets
    frequent_itemsets = apriori(basket_sets, min_support = 0.0001, use_colnames = True)
    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    # generating association rules
    rules = association_rules(frequent_itemsets, metric = 'lift', min_threshold = 1)
    rules = pd.DataFrame(rules)
    # preprocessing text for further use
    rules["antecedents"] = rules["antecedents"].apply(lambda x: ', '.join(list(x))).astype("unicode")
    rules["consequents"] = rules["consequents"].apply(lambda x: ', '.join(list(x))).astype("unicode")
    # creating the chain
    chain = []
    for ant in rules.antecedents:
        if item.loc[item['product_id']==ant, 'order_purchase_timestamp'].shape[0]!=0:
            ant_date = item.loc[item['product_id']==ant, 'order_purchase_timestamp'].values[0]
            consequents_ant = rules.loc[rules['antecedents']==ant, 'consequents']
            for cons in consequents_ant:
                if item.loc[item['product_id']==cons, 'order_purchase_timestamp'].shape[0]!=0:
                    cons_date = item.loc[item['product_id']==cons, 'order_purchase_timestamp'].values[0]
                    if ant_date<cons_date and cons not in chain:
                        chain.append(cons)
    return chain


'''
get function to deploy the app
this function decides which function to use based on the user's purchase history
'''
@app.get('/recommend/{in_user}')
async def recommend(in_user: str):

    if item_cust.loc[item_cust['customer_unique_id']==in_user, :].shape[0]!=0:
        chain = chain_rec()
        association_rule = prod_rec()
        user_items = list(item_cust.loc[item_cust['customer_unique_id']==in_user, 'product_id'].unique())
        for i in user_items:
            if i in chain:
                reccomend_prods = chain[:chain.index(i)] + chain[chain.index(i)+1:]
            elif df_ap.loc[df_ap['product_id']==i, :].shape[0]!=0:
                if df_ap.loc[df_ap['product_id']==i, 'product_category_name_english'].shape[0]!=0:
                    prod_category = df_ap.loc[df_ap['product_id']==i, 'product_category_name_english'].values[0]
                    if association_rule.loc[association_rule['antecedents']==prod_category, 'consequents'].shape[0]!=0:
                        print('rec')
                        rec_category = association_rule.loc[association_rule['antecedents']==prod_category, 'consequents'].values[0]
                        rec_df = review.merge(df_ap.loc[df_ap['product_category_name_english']==rec_category, ['product_id', 'order_id', 'product_category_name_english']], on='order_id', how='right')
                        reccomend_prods = list(rec_df.sort_values(by='review_score', ascending=False).product_id.values[0:5])
                    else:
                        reccomend_prods = cold_start()
                else:
                    reccomend_prods = cold_start()
            else:
                reccomend_prods = cold_start()
    else:
        reccomend_prods = cold_start()

    return reccomend_prods


# running the app
if __name__ == '__main__':
    uvicorn.run(app, host = '127.0.0.1', port = 4000)
