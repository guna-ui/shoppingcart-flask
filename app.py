from flask import Flask,jsonify,request

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop", "price": 75000},
    {"id": 2, "name": "Phone", "price": 25000},
    {"id": 3, "name": "Tablet", "price": 30000}
]


@app.route("/")
def home():
   return "Welcome to Flask API!"

@app.route('/products',methods=["GET"])
def get_products():
    min_price=request.args.get('min_price',type=int)
    Name     =request.args.get('name')
    if min_price:
        filterd_products=[p for p in products if p['price']>=min_price]
        return jsonify(filterd_products)
    if Name :
        filtered_products=[p for p in products if p['name']==Name]
        return jsonify(filtered_products)
    return jsonify(products)

@app.route('/products',methods=['POST'])
def add_product():
    data=request.get_json()
    products.append(data)
    return jsonify({"message":"Products are added!","product":products}),201

@app.route('/product/<int:id>',methods=["GET"])
def get_product(id):
    product=next((d for d in products if d["id"]==id),None)
    if product:    
     return jsonify({"product":product})
    return jsonify({"error":"Product not found"}),404

@app.route('/product/<int:id>',methods=["PUT"])
def update_product(id):
    product=next((d for d in products if d["id"]==id),None)
    if not product:
        return jsonify({"error":"product not found"}),404
    data=request.get_json()
    if "name" in data:
        product["name"]=data["name"]
    if "price" in data:
        product["price"]=data["price"]

    return jsonify({"message": "Product updated!", "product": product})

@app.route('/product/<int:id>',methods=["DELETE"])
def delete_product(id):
    global products;
    product=next((d for d in products if d["id"]==id),None)
    if not product:
        return jsonify({"error":"product not found"})
    products=[p for p in products if p["id"]!=id]
    return jsonify({"message": "Product deleted successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
