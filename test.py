import matplotlib.pyplot as plt
import pandas as pd

data_name = "data\grocery_prices.xlsx"
data = pd.read_excel('data\grocery_prices.xlsx')
print(data)

cols = [0,1]
df = data[data.columns[cols]]

print("specific columns")
print(df)
x = list(df["Food"])
y = list(df["Costco"])
plt.bar(x, y, width=20)
plt.xlabel("Food")
plt.ylabel("Prices")
plt.show()

