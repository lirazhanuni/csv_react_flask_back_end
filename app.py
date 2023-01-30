import csv
import json

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

FILE_CSV = 'diamond.csv'
  
def load_data():
    json_data = []
    with open(FILE_CSV, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            json_data.append(row)
        return json_data

    return next(csv_reader)
def write_data(data):
    with open(FILE_CSV, 'w',newline='') as outf:
        writer = csv.DictWriter(outf, data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)
        return data
        
@ app.route('/diamond', methods=['GET'])
@ app.route('/diamond/<int:diamond_id>', methods=['GET'])
def get_diamond(diamond_id = -1):
    json_data = load_data()
    if (diamond_id == -1):
        return json_data
    else:
        for d in json_data:
            if int(d['ID']) == diamond_id:
                return d
        return {"msg": "No diamond found"}

@app.route('/diamond', methods=['POST'])
def add_diamond():
    data = request.get_json()   # request data as dict
    file_data = load_data()
    if(len(file_data)>0):
        Newid=int(file_data[len(file_data)-1]["ID"])+1
    else:
        Newid=1
    if type(data)==list:# the json get is in format: array of json [{},{}]
        for el in data:     
            file_data.append({**{'ID':Newid}, **el})
    else:# the json get is in format: a single object json {}
       
        file_data.append({**{'ID':Newid}, **data})
    write_data(file_data)
    return {**{'ID':Newid}, **data}

@app.route('/diamond/<int:diamond_id>', methods=['PUT'])
def update_diamond(diamond_id):    
    data = request.get_json()   
    file_data = load_data()
    diamond_found = False
    for diamond in file_data:
        if (str(diamond_id) == diamond['ID']):
            diamond_found = True
            diamond.update(data)
            break
    if not diamond_found: 
        return {"msg": "No diamond found "}
    write_data(file_data)
    return data

@app.route('/diamond/<int:diamond_id>', methods=['DELETE'])
def delete_diamond(diamond_id):
    json_data = load_data()
    index = 0
    for diamond in json_data:
        if (str(diamond_id) == diamond['ID']):
            json_data.pop(index)
            break
        else:
            index = index + 1
    write_data(json_data)
    return jsonify({'message': diamond_id})


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
