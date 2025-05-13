from fastapi import FastAPI, HTTPException, Query
from datetime import date, datetime
from pydantic import BaseModel
from zoneinfo import ZoneInfo
from enum import Enum
import calendar
import uuid

carts = {} # this will store the carts
customers = [{"customer_id": 1, "role": "private"}, {"customer_id": 2, "role": "business"}] # this will store the customers

app = FastAPI()

### CART CREATION ###

# For testing purposes, we will use a simple in-memory store for the carts
# and suppose that ecommerce_id(random str) and customer_id{private: 1, business: 2} are passed in the request body
class CartRequest(BaseModel):
    ecommerce_id: str
    customer_id: str

@app.post("/cart")
def create_cart(data: CartRequest):
    cart_id = str(uuid.uuid4())  # Defines a unique cart id
    now = datetime.now(ZoneInfo("Europe/Rome")).isoformat()
    carts[cart_id] = {
        "ecommerce_id": data.ecommerce_id,
        "customer_id": data.customer_id,
        "status": "CREATED",
        "created_at": now,
        "updated_at": now,
        "date_checkout": None,
        "items": []
    }
    return {"cart_id": cart_id}

### CART DETAILS ###

class CartView(BaseModel):
    ecommerce_id: str
    customer_id: str
    created_at: str
    status: str
    total: float
    items: list

@app.get("/cart/{cart_id}", response_model=CartView)
def get_cart(cart_id: str):
    cart = carts.get(cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    # Separating the price for private and business customers as it was mentioned on the use case sessions
    unit_price = 100.00 if cart["customer_id"] == "1" else 80.00
    total = sum(unit_price * item.get("quantity", 1) for item in cart["items"])

    return {
        "ecommerce_id": cart["ecommerce_id"],
        "customer_id": cart["customer_id"],
        "created_at": cart["created_at"],
        "status": cart["status"],
        "total": total,
        "items": cart["items"]
    }

### ADD ITEM TO CART ###

# Defining models
class ProductCategory(int, Enum):
    spare_parts = 1
    refrigeration = 2
    photovoltaic = 3

class Product(BaseModel):
    product_sku: str
    product_name: str
    product_category: ProductCategory
    quantity: int

class ProductList(BaseModel):
    products: list[Product]
 
@app.post("/shop/add")
def add_products(cart_id: str, product_list: ProductList):
    cart = carts.get(cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    for product in product_list.products:
        # Validate quantity
        if product.quantity <= 0:
            raise HTTPException(status_code=400, detail=f"Quantity for product {product.product_sku} must be positive")
        
        # Search for the product in the cart
        for item in cart["items"]:
            if item["product_sku"] == product.product_sku:
                # If the product is already in the cart, update the quantity
                item["quantity"] += product.quantity
                break
        else:
            # If the product is not in the cart, add it
            cart["items"].append(product.dict())
    
    # Update cart metadata
    cart["status"] = "BUILDING"
    cart["updated_at"] = datetime.now(ZoneInfo("Europe/Rome")).isoformat()

    return {"message": "Products added to cart"}

### CHECKOUT ###

@app.get("/cart/checkout/{cart_id}")
def checkout(
    cart_id: str,
    friday: bool | None = Query(default=None, description="Is it Friday?"),
    ):
    cart = carts.get(cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    # Check if the cart is empty
    if not cart["items"]:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    # Check if the customer is private or business by iterating through the customers
    # and checking if the customer_id matches
    customer = next((c for c in customers if c["customer_id"] == int(cart["customer_id"])), None)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Update the cart status and date_checkout
    cart["status"] = "CHECKED_OUT"
    cart["date_checkout"] = datetime.now(ZoneInfo("Europe/Rome")).isoformat()
    
    ### APPLY DISCOUNTS ###
    total = 0.0
    # Here i am assuming that the price of the product is 100.00 as said on the README, and
    # Since i grouped products with the same sku, i can just iterate through the items
    for product in cart["items"]:
        quantity = product["quantity"]
        unit_price = 100.00 if customer["role"] == "private" else 80.00
        subtotal = 0.0
        # One-shot discount policy
        if (is_last_friday_of_month() or (friday is True)) and product["product_category"] == 1 and product["product_sku"] == "FR-1234":
            subtotal = 25.00 * quantity
        else:
            # Applying the discount based on the quantity
            subtotal = unit_price * (1.00 - amount_discount(quantity)) * quantity
            # Apply the gift discount for category 3
            if product["product_category"] == 3:
                free_items = quantity // 5
                subtotal -= free_items * unit_price * (1.00 - amount_discount(quantity))
        total += subtotal
    return {"message": "Cart checked out successfully", "cart": cart, "total": total}

def amount_discount(quantity):
    if quantity > 100:
        discount = 0.20
    elif quantity > 50:
        discount = 0.15
    elif quantity > 25:
        discount = 0.10
    elif quantity > 10:
        discount = 0.05
    else:
        discount = 0.00
    return discount

def is_last_friday_of_month():
    today = date.today()
    year = today.year
    month = today.month

    month_cal = calendar.monthcalendar(year, month)
    fridays = [week[calendar.FRIDAY] for week in month_cal if week[calendar.FRIDAY] != 0]

    return today.day == fridays[-1]
