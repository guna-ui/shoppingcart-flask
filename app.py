from flask import Flask,jsonify,request

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop", "price": 75000},
    {"id": 2, "name": "Phone", "price": 25000}
]


@app.route("/")
def home():
   return "Welcome to Flask API!"

@app.route('/products',methods=["GET"])
def get_products():
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


if __name__ == "__main__":
    app.run(debug=True)
