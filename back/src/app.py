from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/pyreactmongo'


mongo = PyMongo(app)

CORS(app)

db = mongo.db.users

@app.route('/users', methods=['POST'])
def createUser():
    newUser = {
        "name": request.json['name'],
        "email": request.json['email'],
        "password": request.json['password'],
        "hobbys": request.json['hobbys'],
        "imagen": request.json['imagen']
    }
    result = db.insert_one(newUser)
    return jsonify(str(result.inserted_id))


@app.route('/users', methods=['GET'])
def getUsers():
    users = []
    for user in db.find():
        users.append({
            "_id": str(ObjectId(user["_id"])),
            "name": user["name"],
            "hobbys": user["hobbys"],
            "imagen": user["imagen"],
            "email": user["email"],
            "password": user["password"],
        })
    return jsonify(users)

@app.route('/users/<id>', methods=['GET'])
def getUser(id):
    print(id)
    userById = db.find_one({"_id": ObjectId(id)})
    return jsonify({
         "_id": str(ObjectId(userById["_id"])),
         "name": userById["name"],
            "hobbys": userById["hobbys"],
            "imagen": userById["imagen"],
            "email": userById["email"],
            "password": userById["password"],
    })


@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
    db.delete_one({"_id": ObjectId(id)})
    return jsonify({"msg": "user deleted"})

@app.route('/users/<id>', methods=['PUT'])
def updateUser(id):
    db.update_one({'_id': ObjectId(id)}, {'$set': {
        "name": request.json['name'],
        "email": request.json['email'],
        "password": request.json['password'],
         "hobbys": request.json['hobbys'],
        "imagen": request.json['imagen']
    }})
    return jsonify({"msg": "user update"})

if __name__ == '__main__':
    app.run(debug=True)