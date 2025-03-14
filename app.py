from flask import Flask,jsonify,request
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt_identity

app = Flask(__name__)

app.config["JWT_SECRET_KEY"]='gunasekhar'
jwt=JWTManager(app)

users={"admin":"password123"}

@app.route('/login',methods=["POST"])
def login():
    data=request.get_json()
    username=data.get("username")
    password=data.get("password")
    
    if username in users and users[username]==password:
        access_token=create_access_token(identity=username)
        return jsonify({"access_token":access_token})
    return jsonify({"error":"Invalid credentials"}),404

products = [
    {"id": 1, "name": "Laptop", "price": 45000},
    {"id": 2, "name": "Mobile", "price": 20000},
    {"id": 3, "name": "Tablet", "price": 15000},
    {"id": 4, "name": "Smartwatch", "price": 5000},
    {"id": 5, "name": "Earbuds", "price": 3000},
    {"id": 6, "name": "Monitor", "price": 12000},
    {"id": 7, "name": "Keyboard", "price": 2500},
    {"id": 8, "name": "Mouse", "price": 1500}
]


@app.route("/")
def home():
   return "Welcome to Flask API!"

# curl "http://127.0.0.1:5000/products?limit=3&offset=0"
# curl "http://127.0.0.1:5000/products?sort_by=price&order=asc"

@app.route('/products',methods=["GET"])
@jwt_required()
def get_products():
    # Get pagination params
    current_user=get_jwt_identity()
    limit = request.args.get('limit', default=5, type=int)
    offset = request.args.get('offset', default=0, type=int)

    # Get sorting params
    sort_by = request.args.get('sort_by', default='id', type=str)  # Default: sort by 'id'
    order = request.args.get('order', default='asc', type=str)  # Default: ascending

    # Validate sort_by field
    valid_sort_fields = {'id', 'name', 'price'}
    if sort_by not in valid_sort_fields:
        return jsonify({"error": f"Invalid sort field. Choose from {valid_sort_fields}"}), 400

    # Validate order field
    if order not in {'asc', 'desc'}:
        return jsonify({"error": "Invalid order. Choose 'asc' or 'desc'"}), 400

    # Sort the products
    sorted_products = sorted(products, key=lambda x: x[sort_by], reverse=(order == 'desc'))

    # Apply pagination
    paginated_products = sorted_products[offset: offset + limit]

    return jsonify({
        "total": len(products),
        "limit": limit,
        "offset": offset,
        "sort_by": sort_by,
        "order": order,
        "products": paginated_products,
        "user":current_user
    })

@app.route('/products',methods=['POST'])
def add_product():
    data=request.get_json()
    if not data:
        return jsonify({"error":"Empty request body"}),404
    required_fields=["id","name","price"]
    missing_fields=[field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error":f"Missing fields : {', '.join(missing_fields)} "}),400
    if not isinstance(data["id"],int) or not isinstance(data["price"],(int,float)):
         return jsonify({"error": "Invalid data type: 'id' should be int, 'price' should be int or float"}), 400
    if any(p["id"]==data["id"] for p in products):
        return jsonify({"error":"Product id already existes"},400)
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
    
    if not data :
        return jsonify({"error":"empty request"}),400
    
    if "name" in data and not isinstance(data["name"],str):
        return jsonify({"error":"name should be string"}),404
    if "price" in data and not isinstance(data["price"],(int,float)):
        return jsonify({"error":"price should be int or float"}),404
    
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
    return jsonify({
        "message":"product deleted successfully",
        "deleted_product":product})
    

if __name__ == "__main__":
    app.run(debug=True)
