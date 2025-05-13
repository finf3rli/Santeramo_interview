# Development info

here follows all the decisions i've taken during the development of this REST API.

## Stack adopted:
  
  - FastAPI as suggested to create a RESTful API easily with Python. I learnt it line by line of code since i never used it;
  - Pydantic to create data models and validate input;
  - Dictionaries directly in memory to simulate temporary storage, in absence of a DB.

## API Routes

  - **POST /cart:** \
    receives ecommerce_id and customer_id{private: 1, business: 2} as input. Saves cart in memory and sets state to *CREATED*
  - **GET /cart/{cart_id}:**\
    given the cart's id, user can use this endpoint to get track of what is inside the cart. Also sets a preview(before discounts) of the total price, considering as said below that each item costs 100.00. Since the specific mentions the separation between private and business customers, i've put 80.00 as business price;
  - **POST /shop/add:**\
    it receives a json list of products with the given data specifics(sku, name, category, amount). Updates cart to *BUILDING*;
  - **GET /cart/checkout/{cart_id}:**\
    if cart exists and not empty, calculates total price considering discount policies. Changes state to *CHECKED_OUT*.

## Functions additional info

**create_cart(data: CartRequest) -> /cart**

Simply returns a cart by creating a uuid4. This is how we get to use the cart.

**get_cart(cart_id: str) -> /cart/{cart_id}, response_model = CartView**

Given a uuid4 it returns the item list of the chosen cart. It has a response_model in order to accomplish what the specifics say about the cart view. Error 404 if no cart has been found. Setting unit price based on customer's role.

**add_products(cart_id: str, product_list: ProductList) -> /shop/add**

Receives a list of products and adds to them to the chosen cart. Validates quantity input(quantity > 0) else error 400. It searches for already existing items in the cart in case the customer adds articles in more than 1 operations, then adds up to the quantity: else, append to list. Defined models to accept data and a Enum to manage product category. Changes cart status to BUILDING.

**checkout(cart_id: str, friday: bool | None = Query(default=None, description="Is it Friday?")) -> /cart/checkout/{cart_id}**

Manipulates final total price. For testing purposes i added a optional field to set the day as friday for the "one-shot" policy. Once obtained the cart, the function checks what is the customer's role to set the unit price, then proceeds with the discount policies evaluation in this order:

  - **ONE-SHOT:** If it's last friday of the month(and only for items with sku "FR-1234" in category 1), sets unit price(hard-coded) to 25.00. This items won't get any other discounts;
  - **Quantity:** Based on the amount the customer is going to buy of any single product(not eligible for ONE-SHOT), the subtotal will be update following the chart down below;
  - **Gift:** If customer buys a multiple of 5 items with same SKU from category 3, gets 1 item free. Unit price is evaluated after discount(if any) and reduced from the subtotal(this is also cumulative with the quantity policy). Since the code is already adding up all the items with the same SKU, i didn't need to check for it(Given that a SKU is unique and so there cannot exist more articles with same SKU and different category).

Now returns the cart view with:
  - Checkout date;
  - Total;
  - State changes to CHECKED_OUT.

On the bottom of the file are defined additional functions, such as *is_last_friday_of_month()* and *amount_discount()*.

### Test cases

[Here](INPUT_TEST) a few examples ready to be tested. I used fastAPI's doc interface to test inputs.

# Final considerations

I really enjoyed developing this API. It was my first time creating a complete REST API and using FastAPI. I found the framework very straightforward and enjoyable to use.
