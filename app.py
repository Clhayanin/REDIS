import os
import redis
import json
from flask import Flask,request,jsonify
app = Flask(__name__)


#ให้ตัวแปร db เก็บข้อมูลใน redis เพื่ออ้างอิงในการแสดงค่า เก็บค่า แก้ไข ลบ 
db=redis.StrictRedis(
        host='10.100.2.128', 
        port=6379,
        # host='node9151-advweb-13.app.ruk-com.cloud',
        # port=11148,
        password='YCTydi14237',
        decode_responses=True)


# Get All Staffs
#โชว์ข้อมูลใน Redis ทั้งหมด
@app.route('/',methods=['GET'])
def Show_keys():
    name=db.keys() #เก็บข้อมูลทั้งหมดใน  name
    name.sort() #เรียงข้อมูลลลล
    req = [] #สร้าง req เป็นarray
    for i in name :  #ใช้ for ให้วนตั้งแต่ i จนถึง name 
        req.append(db.hgetall(i)) #ให้ตัวแปร req เก็บค่าแต่ละตัวที่มีใน db
    return jsonify(req) #ส่งค่า req ให้ไปแสดง


# Get Single 
#โชว์ข้อมูลใน Redis แค่ตัวที่ต้องการ
@app.route('/<id>',methods=['GET']) #ส่งไอดีไปในฟังชั่น การใส่ 127.0.0.1/5000/A001
def Show_key(id):
    req = db.hgetall(id) #แปร req เก็บค่าข้อมูลที่ตรงกับ id ที่เราส่งเข้ามา

    return jsonify(req) #ส่งค่า req ให้ไปแสดง


 # เพิ่มข้อมูล 
@app.route('/', methods=['POST']) 
def add_animal():
    #แปลงค่าเป็น js
    id = request.json['id'] #ให้ตัวแปร id เก็บค่า ตัวแปร id จาก postman
    name = request.json['name']#ให้ตัวแปร name เก็บค่า ตัวแปร name จาก postman
    type = request.json['type'] #ให้ตัวแปร type เก็บค่า ตัวแปร type จาก postman
    
    #ให้ตัวแปร user เก็บข้อมูล ของ id name type โดย ให้ id = ตัวแปร id , name = ตัวแปร name
    #type = ตัวแปร type
    user = {"id":id, "name":name, "type":type}

    db.hmset(id, user) #set ข้อมูลใน user โดยให้  user ชี้ไปตำแหน่ง id 
    return jsonify(user) #ส่ง user กลับไป


# Update แก้ไขข้อมูล
@app.route('/<Key>', methods=['PUT']) #รับค่าkey หรือ id มา เช่น 127.0.0.1/5000/A001
def update_animal(Key):
    name = request.json['name'] #ให้ตัวแปร name เก็บค่า ตัวแปร name จาก postman
    type = request.json['type'] #ให้ตัวแปร type เก็บค่า ตัวแปร type จาก postman

    #ให้ตัวแปร user เก็บข้อมูล ของ id name type โดย ให้ id = key, name = ตัวแปร name
    #type = ตัวแปร type
    user = {"id":Key, "name":name, "type":type}
    db.hmset(Key, user) #set ข้อมูลใน user โดยให้  user ชี้ไปตำแหน่ง key โดยใส่ข้อมูลทับลงไป
    return jsonify(user) #ส่ง user กลับไป



# Delete Staff
@app.route('/<Key>', methods=['DELETE']) #รับค่าkey หรือ id มา เช่น 127.0.0.1/5000/A001
def delete_animal(Key):
    db.delete(Key) #ทำการลบข้อมูลที่ตำแหน่ง key
    return "DELETE" #เมื่อทำเสร็จแสดง DELETE

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
# if __name__ == '__main__':
#     app.run()