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



---

# Arbo Code Challenge: Cart API

## Intro

Cart API Code Challenge: part of the interview process at Arbo.

_Dear candidate,_

_We are confident you are excited to take on this challenge, just as much as we are excited to review your code._

## Forewords

_The aim is not to develop a fully working, production-ready project, but rather to get a glimpse of your skills: how you approach and solve a problem._

You don’t need to rush into delivering a solution, but it also can’t take forever.

Take the right amount of time to evaluate this challenge: time is important, but not the most...

You don’t need to overdo or develop every possible aspect of the application, **focus on the most relevant aspects** and those requested by the specification.

We will support you in accessing this repo and cloning it.

**IMPORTANT**: as soon as you clone this repo:

- add your CONTRIBUTING.md file
- push it back to your working repository on your GitHub account
- right after this, before starting any development, please share your working repo with us
- you will need CONTRIBUTING.md to include additional information about your development—any info you consider relevant to share with us before we discuss your challenge solution together

## Cart Challenge Description

We are a retail company. Our pricing system is very complicated, and we do not have a final price for each product. Instead, we use specific discount rules to find the final price for our customers.

We ask you to create a REST API to implement the following business requirements, gathered from our e-commerce Cart use case session:

- Customers connect to our e-commerce.
- The e-commerce system identifies whether the customer is private or business.
- The e-commerce system shows the correct price list for each customer.
- Choose a product and configure it.
- Select a quantity.
- Add the product to the cart.
- Checkout the cart.

To have an idea on our products, please have look at a live example: [Product Page](https://arbo.it/ricambi/ricambi-commerciali-caldaie-e-bruciatori/bruciatori/)

### Cart Creation

We create a cart by specifying:

`ecommerce_id`, `customer_id`, a `status`, `created_at`, `updated_at`.

Cart `status` possible values are: `created`, `building`, `checkout`.

Customers are identified by `customer_role`. Possible values are: `private`, `business`.

### Add Items to Cart

We add items to the cart by providing `ecommerce_id`, `customer_id`, and `item_list`.

Each entity in `item_list` has the following details:

`product_sku`, `product_name`, `product_category`, `quantity`.

For this challenge, consider:

The `quantity` is the number of items for the same product.

The `product_category` possible values are: `spare_parts` value=1, `refrigeration` value=2, `photovoltaic` value=3.

### View a Cart

The client should be able to query an API endpoint to check what's inside the cart.

The API will return the following details:

Cart `ecommerce_id`, `customer_id`, `created_at`, the `status`, and a total `price`.

The `item_list` with `product_sku`, `product_name`, `product_category`, `quantity`.

The calculated `price` for the item based on the policies below.

### Cart Checkout

The customer will checkout the cart, and the API will set the cart `date_checkout` and will calculate and set the final price for the cart.

### Price Policies Calculation

- Let’s assume all the products in our catalog have the same standard base price of €100.00 per item.

- When you buy more items of the same `product_sku`:

  - No discount is applied for quantities up to 10.
  - A 5% discount is applied for quantities above 10.
  - A 10% discount is applied for quantities above 25.
  - A 15% discount is applied for quantities above 50.
  - A 20% discount is applied for quantities above 100.

- When you buy more items of the same `product_sku` in a specific category, you receive a gift:

  - Buy 5 or a multiple of 5 `product_sku` in category 3, and you receive 1 free for each multiple you buy.

- When it is the last Friday of the month, there’s a special promotion called "one-shot" (based on the cart’s checkout date):

  - For 24 hours, some specific `product_sku` in `category` 1 has a net price of €25.00.
  - For this specific `product_sku`, no discount is applied.

## What's Desirable from This Project

- **Technical stack**: You can choose your favorite stack of technologies for this project.
- **Readability**: Create clean code, following standards and good principles of code design. Comment the code where needed.
- **Compliance**: Meet the specifications.
- **Testability**: Make the code easy to understand and test.
- **Documentation**: Provide a summary of the activity.
- **Feedback**: Please leave us some comments on what you think about the test.

_Have fun coding this challenge!_

Please let us know when you are done and have committed everything to your GitHub repo.

Do not hesitate to contact us for any questions about this challenge.

technical reference => l.casini@arbo.it
