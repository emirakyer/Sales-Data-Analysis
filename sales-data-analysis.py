import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from warnings import filterwarnings


### Data Preparation

all_data = pd.read_feather(r"venv/data-sets/Udemy PS/P4/Sales_data.ftr")


# Missing Values Detection

all_data.isnull().sum()
all_data = all_data.dropna(how="all")

all_data.duplicated()
all_data[all_data.duplicated()]
all_data = all_data.drop_duplicates()


# 1) Which is the best month for sale?

def return_month(x):
    return x.split("/")[0]

all_data["Month"] = all_data["Order Date"].apply(return_month)

all_data["Month"].unique()


# --> Editing the data

filter1 = all_data["Month"] == "Order Date"

all_data[-filter1]

all_data=all_data[-filter1]


# --> Data type change

all_data["Month"] = all_data["Month"].astype(int)

all_data["Quantity Ordered"] = all_data["Quantity Ordered"].astype(int)

all_data["Price Each"] = all_data["Price Each"].astype(float)


all_data.dtypes



# --> Here we can see how many times the product has been ordered in months Month 12 reached the highest number of order attempts. We see that we see the minimum and maximum order numbers.


all_data.groupby(["Month"]).agg({"Quantity Ordered" : ["sum","min","max"]}).sort_values(by=("Quantity Ordered", "sum"), ascending=False)



# --> Let's look at the monthly returns of the total product orders made.

all_data["Sales"] = all_data["Quantity Ordered"] * all_data["Price Each"]
all_data.groupby(["Month"])["Sales"].sum().sort_values(ascending=False)



# Bar Chart

all_data.groupby(["Month"])["Sales"].sum().plot(kind="bar",width=0.8,color="orange")
plt.title("Total Revenue by Month")
plt.xlabel("Months")
plt.ylabel("Amount of Income")



# 2) Analyzing which city has Maximum Order

def return_city(x):
    return x.split(",")[1]

all_data["City"] = all_data["Purchase Address"].apply(return_city)

all_data["City"].value_counts()



# --> We are displaying the total and average amount of money received as a result of the orders made below.

all_data.groupby("City").agg({"Sales": ["sum","mean","max", "min"]}).sort_values(by=("Sales", "sum"), ascending=False)



# --> Let's make it more understandable with a graph

all_data.groupby("City").agg({"Sales": ["mean","max","min"]}).plot(kind="barh", stacked=True, figsize=(12, 6))



# --> A pie chart would be best for this demonstration

all_data["City"].value_counts().plot(kind="pie",explode=(0.3,0.2,0.1,0.1/2,0, 0, 0, 0, 0),autopct="%.0f%%",shadow=True,figsize=(12,8))
plt.title("Which City Has Maximum Order")
plt.text(1.6, 1, "Percentage of Order", fontsize=12)

# The cities of Los Angeles, New York and San Francisco account for more than 50% of the number of orders.




# 3) Understand What product sold the most & Why ?

all_data["Product"].value_counts()[0:10].plot(kind="pie",figsize=(12,8),autopct="%.0f%%",title="Top 10 Most Sold Product Percentage")
all_data.groupby("Product").agg({"Sales": ["sum","mean"],"Quantity Ordered":["sum"]}).sort_values(by=[("Sales", "sum")], ascending=False)

# As we can see from this code output, ordering a lot of the product does not always mean that it will bring a lot of revenue.



count_df = all_data.groupby(["Product"]).agg({"Quantity Ordered":"sum","Price Each" : "mean"})
count_df = count_df.reset_index()
products = count_df["Product"].values
count_df["Product"].values



fig, ax1 = plt.subplots(figsize=(12,9))
ax2 = ax1.twinx()
ax1.bar(count_df["Product"], count_df["Quantity Ordered"], color="orange")
ax2.plot(count_df["Product"], count_df["Price Each"])
ax1.set_xticklabels(products, rotation="vertical")

ax1.set_ylabel("Order Count")
ax2.set_ylabel("Average Price Of Product")




# 4) Understanding Trend of the most sold product

most_sold_product = all_data["Product"].value_counts()[0:5].index

all_data["Product"].value_counts()[0:5].index



all_data["Product"].isin(most_sold_product)

most_sold_product_df = all_data[all_data["Product"].isin(most_sold_product)]

most_sold_product_df.head()



# Chart
most_sold_product_df.groupby(["Month","Product"]).size()

pivot = most_sold_product_df.groupby(["Month","Product"]).size().unstack()

pivot.plot(figsize=(8,6))



# 5) Analysing What products are most often sold together

df_duplicated = all_data[all_data["Order ID"].duplicated(keep=False)]

dup_products = df_duplicated.groupby(["Order ID"])["Product"].apply(lambda x : ','.join(x)).reset_index().rename(columns={"Product":"grouped_products"})

df_duplicated.groupby(["Order ID"])["Product"].apply(lambda x : ','.join(x)).reset_index().rename(columns={"Product":"grouped_products"})



### Pie chart showing which 7 products are most frequently sold together

dup_products_df = df_duplicated.merge(dup_products,how="left", on="Order ID")

no_dup_df = dup_products_df.drop_duplicates(subset=["Order ID"])

no_dup_df["grouped_products"].value_counts()[0:7].plot.pie()
# top 7 most sold products together































