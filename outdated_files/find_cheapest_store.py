import matplotlib.pyplot as plt
import pandas as pd

# read in data
data_name = "data\grocery_prices.xlsx"
data = pd.read_excel('data\grocery_prices.xlsx')

#print(data)

result = data[data['Food'] == 'eggs']

# for column in result:
#     #print(column)
#     print(result[column])

# print(data.iloc[0]['Costco'])

# 0 = Costco, 1 = Walmart, 2 = Safeway, 3 = Loblaws

# set an arbitrary minimum pruce
min_price = float("inf") #1000.0
# Define the stores we are looking at
stores = ["Costco", "Walmart", "Safeway", "Loblaws"]

# get the minimum price in each store
for store in stores:
    # Get the current price we are looking at and turn it into a type float
    current_price = data.iloc[7][store]
    current_price = current_price.item()
    # compare the current price to the minimum price to see if it is smaller
    if  current_price < min_price:
        min_price = data.iloc[7][store] 
    print(current_price)
print("cheapest price:", min_price)