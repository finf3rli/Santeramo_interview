
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
