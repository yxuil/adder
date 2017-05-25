from flask import request, jsonify, url_for, render_template
from app import app

import peewee as pw
import sqlite3 as sql
database = pw.SqliteDatabase("num_app.db")

def before_request_handler():
    database.connect()
def after_request_handler():
    database.close()

class Numbers(pw.Model):
    initialy = pw.IntegerField()
    plusone = pw.IntegerField(null = True)
    timestwo = pw.IntegerField(null = True)
    class Meta:
        database = database

@app.route('/api/numbers', methods = ['POST'])
def loadNum():
    assert request.method == "POST"
    data = request.get_json()
    allnumbers = [int(i) for i in data["num"].split(",")]
    for num in allnumbers:
        newrecord = Numbers.create(initialy=num)
        newrecord.save()
    return jsonify({"total records": Numbers.select().count(),
                    "new added num": "; ".join(map(str, allnumbers))})


@app.route("/api/numbers", methods = ['GET'])
def allnum():
    table = Numbers.select().group_by(Numbers.id).dicts()
    print(table)
    return jsonify(list(table))

@app.route("/api/numbers/<int:id1>/<int:id2>", methods = ["POST","GET"])
def numbyrange(id1, id2):
    start, end = sorted([id1, id2])
    table = Numbers.select().where(start <= Numbers.id <= end)
    return jsonify(list(table.dicts()))

@app.route("/api/numbers/<int:id1>/add", methods=['POST'])
def add(id1):
    records = Numbers.select().where(Numbers.id == id1)
    for record in records:
        record.plusone = record.initialy + 1
        record.save()
    return jsonify(list(records.dicts()))

@app.route("/api/numbers/<int:id1>/double", methods=['POST'])
def double(id1):
    records = Numbers.select().where(Numbers.id == id1)
    for record in records:
        record.timestwo = record.plusone * 2
        record.save()
    return jsonify(list(records.dicts()))
    
@app.route("/")
@app.route("/index")
def frontend():
    return render_template("index.html")

