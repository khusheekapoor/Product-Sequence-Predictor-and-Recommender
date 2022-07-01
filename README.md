# Product-Sequence-Predictor-and-Recommender

The objective of this project is to enhance the online retail experience of a user by providing recommendations by gaining insights into the user behaviour 
and predicting the user's next purchase using Association Rule Mining and Markov Chains.

## Libraries Used

| Library | Function |
|--|--|
| [numpy](https://numpy.org/) | To manipulate the data | 
| [pandas](https://pandas.pydata.org/) | To manipulate the data |
| [matplotlib](https://matplotlib.org/) | For data visualization |
| [seaborn](https://seaborn.pydata.org/) | For data visualization |
| [mlxtend](http://rasbt.github.io/mlxtend/#:~:text=Mlxtend%20(machine%20learning%20extensions)%20is,to%2Dday%20data%20science%20tasks.) | For association rule mining |
| [fastapi](https://fastapi.tiangolo.com/) | For creating [API](/main.py) |
| [uvicorn](https://www.uvicorn.org/) | For model deployment |
| [streamlit](https://streamlit.io/) | To build the [UI](/app.py) |
| [requests](https://pypi.org/project/requests/) | To connect the [UI](/app.py) with the [API](/main.py) |

## [Data Source Used](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

This is a Brazilian ecommerce public dataset of orders made at Olist Store. The dataset has information of 100k orders from 2016 to 2018 made at multiple marketplaces 
in Brazil. Its features allows viewing an order from multiple dimensions: from order status, price, payment and freight performance to customer location, product 
attributes and finally reviews written by customers. There is also a geolocation dataset that relates Brazilian zip codes to lat/lng coordinates.

This dataset was generously provided by Olist, the largest department store in Brazilian marketplaces. Olist connects small businesses from all over Brazil to channels 
without hassle and with a single contract. Those merchants are able to sell their products through the Olist Store and ship them directly to the customers using Olist 
logistics partners.

After a customer purchases the product from Olist Store a seller gets notified to fulfill that order. Once the customer receives the product, or the estimated delivery 
date is due, the customer gets a satisfaction survey by email where he can give a note for the purchase experience and write down some comments.

### [Database](/Datasets) Schema

<img src="https://user-images.githubusercontent.com/74901388/176829393-ea1aef06-82d4-47fe-971a-4319644ab9fa.png" width="700" height="400" alt="Database Schema">

## [Exploratory Data Analysis](/Exploratory&#32;Data&#32;Analysis.ipynb)

Due to huge size of the database, each table is explored individually and the required pre-processing is performed with the help of charts and graphs.

## Churn Analysis

After performing Churn Analysis on the database, we infer that 97% of the customers churn out of the system, i.e., they make only one purchase in the entire lifetime 
of their purchase history. However, since the dataset has 10,00,000 data entries, we still have 3,000 entries to analyze.

## Web Application

The Home Screen of the Web Application initially consists of two rows: Login and Trending Products. The user is prompted to enter their Unique Customer ID and login to 
the site. Based on the purchase history of the customer, one of the three cases is triggered.

<img src="https://user-images.githubusercontent.com/74901388/176849879-bf7e0b26-8365-47bf-a527-04b6825f8c1f.png" width="650" height="600" alt="Home Page">


### Case-1: Cold-Start

If a new user, who has no purchase history, logs in, then the Top 5 trending products are recommended. This is the same as the Trending Products on the Home Page.

<img src="https://user-images.githubusercontent.com/74901388/176850267-26a24cc3-c4b0-4eaf-83f6-4616263879d1.png" width="650" height="600" alt="Cold Start">


### Case-2: Sequence Chain

If the user has previously purchased from the store, and their purchase is in a **Chain** of Products obtained using Association Rule Mining (Antecendent->Consequent:Antecedent->Consequent::) 
and Markov Chains (P(Conequent|Antecedent)), then the remaining items in the chain after the previously purchased product are recommended. If there is no remaining product 
in the Chain, then the Cold-Start case is triggered.

<img src="https://user-images.githubusercontent.com/74901388/176850950-4b0245bc-ee08-4fc9-aee6-85bf865e4121.png" width="550" height="650" alt="Sequence Chain">


### Case-3: Cross-Category Sell

If the user has previously purchased from the store, and their purchase is not in the Chain, then the category of the previous purchase is considered as the Antecedent, 
and the next category for purchase is obtained using Association Rule Mining. The Top 5 products of the Consequent category are then recommended. If there is no category 
in the Consequent, then the Cold-Start case is triggered.

<img src="https://user-images.githubusercontent.com/74901388/176851310-b5ee5e96-7152-4ab7-ba83-2b24b12d8b01.png" width="650" height="600" alt="Cross-Category Sell">


## Conclusion & Future Work

The API works accurately, however, takes a lot of time to render the output owing to the large size of the dataset, time complexity of generating association rules 
and building the chain. When deployed on a larger scale, the working of the algorithm can be parallelized to improve the time efficiency and achieve micro-second response. 
Also, the database can be dynamically updated to store the entries of the new purchases made by the customer, which may lead to changes in the chain of products and cross-category 
sales.






