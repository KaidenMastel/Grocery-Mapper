# format store data as dictionaries
costco = {"eggs": 4.54, "chicken": 16.49, "tomatoes(per kg)": 5.73, "rice": 12.59, "bread":7.39, "milk": 6.91, "fish": 15.59, "broccoli(per kg)": 7.69, "apples(per kg)": 3.23}
walmart = {"eggs": 4.04, "chicken": 11.00, "tomatoes(per kg)": 6.33, "rice": 5.47, "bread": 2.97, "milk": 5.79, "fish": 11.07, "broccoli(per kg)": 6.55, "apples(per kg)": 6.97}
safeway = {"eggs": 5.29, "chicken": 19.96, "tomatoes(per kg)": 3.99, "rice": 5.49, "bread": 5.29, "milk": 5.99, "fish": 12.99, "broccoli(per kg)": 3.49, "apples(per kg)": 2.69}
loblaws = {"eggs": 5.99, "chicken": 15.00, "tomatoes(per kg)": 6.59, "rice": 6.99, "bread": 4.49, "milk": 5.79, "fish": 13.99, "broccoli(per kg)": 3.99, "apples(per kg)": 2.99}

# define the stores to loop through as a list
stores = [costco, walmart, safeway, loblaws]

# define a set minimum price
min_price = float("inf") 
# loop through each store
for store in stores:
    # check if store price for that product is the smallest
    if store["eggs"] < min_price:
        min_price = store["eggs"]


