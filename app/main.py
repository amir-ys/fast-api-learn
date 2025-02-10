
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(debug=True)


@app.get('id/{id}')
def hello(id : int):
    return {
       "message" : f"id:{id}"
    }

class Item(BaseModel):
    name : str
    age : int
@app.post('/item/store')
def item(item : Item):
    return {
       "name" : item.name,
       "age" : item.age,
    }


@app.get('/')
def name(name : str =  "کاربر مهمان"):
    return {
       "message" : name
    }


@app.get('/get-id/{id}')
def getId(id : int):
    if id < 1:
        raise HTTPException(
            status_code=400, detail="ID باید بزرگتر از 0 باشد."
        )
    
    return {"id":id}


@app.get('/sum')
def sum_c(a:int = 0 ,b : int = 0):
    return {
        "sum" : a + b
    }


class User(BaseModel):
    username  : str
    password : str

@app.post('/user')
def user(user : User):
    if len(user.username) < 3:
        raise HTTPException(status_code=400, detail="username باید حداقل 3 کاراکتر باشد.")

    if len(user.password) < 6:
        raise HTTPException(status_code=400, detail="password باید حداقل 6 کاراکتر باشد.")

    if not re.search(r'[A-Z]', user.password) or not re.search(r'\d', user.password):
        raise HTTPException(status_code=400, detail="password باید حداقل یک حرف بزرگ و یک عدد داشته باشد.")
    
    return {
        "username" : user.username,
        "password":  user.password
    }



class StoreProduct(BaseModel):
    price : int
    name: str
    quantity : int
@app.post('/products/add')
def store_product(product : StoreProduct):
    if product.price < 1:
        raise HTTPException(status_code=400 , detail="price must greater than 0")

    if product.quantity < 0:
        raise HTTPException(status_code=400 , detail="price must greater than 0")

    return {
        "name" : product.name ,
        "quantity" : product.quantity ,
        "price" : product.price 
    }

@app.get('/products')
def product_list(min_price: Optional[int] = None):
        products = [
             {
                "name" : 'a' ,
                 "quantity" : 1 ,
                  "price" : 1000 
             },
             {
                "name" : 'b' ,
                 "quantity" : 0 ,
                  "price" : 230 
             },
             {
                "name" : "c" ,
                 "quantity" : 9 ,
                  "price" : 450
             }
        ]
        if min_price != None:
            return [product for product in products if product["price"] >= min_price]

        return products


@app.get('/products/item/{name}')
def product_list(name: str):
        products = [
             {
                "name" : 'a' ,
                 "quantity" : 1 ,
                  "price" : 1000 
             },
             {
                "name" : 'b' ,
                 "quantity" : 0 ,
                  "price" : 230 
             },
             {
                "name" : "c" ,
                 "quantity" : 9 ,
                  "price" : 450
             }
        ]
        filtered =  [product for product in products if product["name"] == name]
        if len(filtered):
            return filtered
        
        raise HTTPException(status_code=404 , detail="not found")



@app.delete('/products/{name}')
def product_list(name: str):
    global products
    
    if not any(product['name'] != name for product in products):
        raise HTTPException(status_code=404 , detail="not found")

    products =  [product for product in products if product['name'] != name]

    return {"message": "محصول حذف شد", "remaining_products": products}


class UpdateProduct(BaseModel):
    quantity : int
    price : int

@app.patch('/products/{name}')
def product_update(name :str , updateProduct : UpdateProduct):
    global products
    
    for product in products:
        if product["name"] == name:
            product["quantity"] = updateProduct.quantity
            product["price"] = updateProduct.price
            return {"message": "محصول ویرایش شد", "updated_product": product}
    
    # اگر محصول وجود نداشت
    raise HTTPException(status_code=404, detail="محصول یافت نشد")


@app.get('/products/total-quantity')
def total_quantity():
    global products
    return {"message": "تعداد کل محصولات", "total_quantity": len(products)}

@app.get('/products/out-of-stock')
def products():
    global products
    out_of_stock_products =[]
    for product in products:
        if product['quantity'] == 0:
            out_of_stock_products.append(product)
            
    return {"message": "تعداد کل محصولات 0", "out_of_stock": out_of_stock_products}


products = [
    {"name": 'a', "quantity": 1, "price": 1000},
    {"name": 'b', "quantity": 0, "price": 230},
    {"name": "c", "quantity": 9, "price": 450}
]

@app.get('/products/most-expensive')
def get_most_expensive_product():
    global products
    if not products: 
        raise HTTPException(status_code=404, detail="محصولی یافت نشد")

    def get_price(product):
       return product['price']

    max_price_product = max(products, key=get_price)

    return {
        "most_expensive": max_price_product
    }

@app.get('/products/average-price')
def get_most_expensive_product():
    global products
    if not products: 
        raise HTTPException(status_code=404, detail="محصولی یافت نشد")
    
    prices = [product['price'] for product in products]
    average_price = sum(prices) / len(prices)

    return {
        "average_price": average_price
    }

@app.post('/products/new')
def store_p(store_product : StoreProduct):

    if any(store_product.name == product['name'] for product in products):
        raise HTTPException(status_code=500 , detail= "dublicate product")
    
    products.append(store_product.dict())

    return store_product