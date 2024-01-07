import matplotlib.pyplot as plt
import pandas as pd

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
stores = ["Costco", "Walmart", "Safeway", "Loblaws"]
for store in stores:
    current_price = data.iloc[0][store]
    current_price = current_price.item()
    if  current_price < min_price:
        min_price = data.iloc[0][store] 
print(min_price)