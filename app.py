import os
import redis
import json
from flask import Flask,request,jsonify

app = Flask(__name__)



db=redis.StrictRedis(
        host='node9151-advweb-13.app.ruk-com.cloud',
        port=11148,
        password='YCTydi14237',
        decode_responses=True)

# Get All Staffs
@app.route('/',methods=['GET'])
def Show_keys():
    name=db.keys() #ข้อมูลทั้งหมด
    name.sort() #เรียงข้อมูลลลล
    req = []
    for i in name :
        req.append(db.hgetall(i))
    return jsonify(req)


# Get Single 
@app.route('/<id>',methods=['GET'])
def Show_key(id):
    req = db.hgetall(id)

    return jsonify(req)


 # Create 
@app.route('/', methods=['POST'])
def add_animal():
    id = request.json['id'] #แปลงค่าเป็น js 
    name = request.json['name']
    type = request.json['type']
    
    user = {"id":id, "name":name, "type":type}

    db.hmset(id, user)
    return jsonify(user)


# Update a Staff
@app.route('/<Key>', methods=['PUT'])
def update_animal(Key):

    name = request.json['name']
    type = request.json['type']
    user = {"id":Key, "name":name, "type":type}
    db.hmset(Key, user)
    return jsonify(user)



# Delete Staff
@app.route('/<Key>', methods=['DELETE'])
def delete_animal(Key):
    db.delete(Key)
    return "DELETE"

if __name__ == '__main__':
    app.run()