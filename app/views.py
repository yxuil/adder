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

@app.route('/api/load', methods = ['POST'])
def loadNum():
    assert request.method == "POST"
    data = request.get_json()
    allnumbers = [int(i) for i in data["num"].split(",")]
    for num in allnumbers:
        newrecord = Numbers.create(initialy=num)
        newrecord.save()
    return jsonify({"total records": Numbers.select().count(),
                    "new added num": "; ".join(map(str, allnumbers))})

def allnum():
    table = Numbers.select().group_by(Numbers.id).dicts()
    print(table)
    return jsonify(list(table))

@app.route("/api/numbers", methods = ["POST", "GET"])
def numbyrange():
    params = request.get_json()
    print(request.url, params, type(params))
    if request.method == "POST":
        start = int(params["start"]) if params["start"] != "" else 0
        end = int(params["end"]) if params["end"] != "" else 0
        if start > end:
            start = end
    elif request.method == "GET":
        print("GET")
    
    if end==0 and start==0:
        table = Numbers.select().group_by(Numbers.id)
    else:
        table = Numbers.select().group_by(Numbers.id).where( (start <= Numbers.id) & (Numbers.id  <= end))
    print(list(table.dicts()))
    return jsonify(list(table.dicts()))

@app.route("/api/add", methods=['POST'])
def add():
    params = request.get_json()
    print(params)
    ids = params["select"]
    records = Numbers.select().where(Numbers.id << ids)
    for record in records:
        record.plusone = record.initialy + 1
        record.save()
    return jsonify(list(records.dicts()))

@app.route("/api/double", methods=['POST'])
def double():
    params = request.get_json()
    print(params)
    ids = params["select"]
    records = Numbers.select().where(Numbers.id << ids)
    for record in records:
        record.timestwo = record.plusone * 2
        record.save()
    return jsonify(list(records.dicts()))


@app.route("/")
@app.route("/index")
def frontend():
    return render_template("index.html")

