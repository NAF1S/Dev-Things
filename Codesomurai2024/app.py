#allah vorosa
import sqlite3
from flask import Flask
from flask import request,make_response,json,jsonify


app = Flask(__name__)
#POST api
@app.route("/api/users",methods = ["POST"])
def add_user():
     #for adding user
    data = request.get_json()
    db = sqlite3.connect("store.db")
    db.cursor().execute("INSERT INTO User (user_id,user_name,balance) VALUES (?,?,?)",(data["user_id"],data["user_name"],data["balance"]))
    db.commit()
    db.close()
    return make_response({"user_id":data["user_id"],"user_name":data["user_name"],"balance":data["balance"]},201)

@app.route("/api/stations",methods = ["POST"])
def add_station():
     #for adding station
    data = request.get_json()
    db = sqlite3.connect("store.db")
    db.cursor().execute("INSERT INTO Station (station_id,station_name,longitude,latitude) VALUES (?,?,?,?)",(data["station_id"],data["station_name"],data["longitude"],data["latitude"]))
    db.commit()
    db.close()
    return make_response({"station_id":data["station_id"],"station_name":data["station_name"],"longitude":data["longitude"],"latitude":data["latitude"]},201)

@app.route("/api/trains",methods = ["POST"])
def trains():
     #for adding trains
    data = request.get_json()
    db = sqlite3.connect("store.db")
    db.cursor().execute(("INSERT INTO Trains (train_id, train_name, capacity) VALUES (?, ?, ?)",(data['train_id'], data['train_name'], data['capacity'])))
    for station in data['stations']:
        db.cursor().execute("INSERT INTO Stations (station_name,arrival_time,departure_time,fare) VALUES(?,?,?,?)",(station['station_name'], station['arrival_time'], station['departure_time'], station['fare']))

    db.commit()
    first_departure_time = db.cursor().execute(f"SELECT departure_time FROM Stations WHERE train_id = {data['train_id']}  ORDER BY station_id ASC LIMIT 1", ({data['train_id']},)).fetchone()[0]
    last_arrival_time  = db.cursor().execute(f"SELECT arrival_time  FROM Stations WHERE train_id = {data['train_id']}  ORDER BY station_id DESC LIMIT 1", ({data['train_id']},)).fetchone()[0]
    cnt = db.cursor().execute(f"SELECT COUNT(*) FROM Stations WHERE train_id = {data['train_id']}", ({data['train_id']}))
    return make_response({"train_id":data['train_id'],"train_name":data['train_name'],'capacity':data['capacity'],'service_start':first_departure_time,'service_ends':last_arrival_time,'num_stations':cnt},201),db.close()

        

@app.route("/api/stations",methods = ["GET"])
def get_station():
    db = sqlite3.connect("store.db")
    stations = db.cursor().execute("SELECT * FROM Station ORDER BY station_id ASC").fetchall()
    results = []
    for station in stations:
        result = {
            'station_id':station[0],
            'station_name': station[1],
            'longitude': station[2],
            'latitude':station[3]
        }
        results.append(result)
    if(len(results)>0):
        return make_response({"station":jsonify(results)},200)
    else:
        return make_response({"station":"[]"},200)
    
@app.route("/api/stations/<int:id>/trains",methods=["GET"])
def get_train():
    db = sqlite3.connect("store.db")
    return make_response("helo",200)
@app.route("/api/wallets/<int:walletid>",methods=["GET"])
def wallet(walletid):
    db = sqlite3.connect("store.db")
    Id=db.cursor().execute(f"SELECT * FROM User WHERE user_id = {walletid}")
    if(len(Id)>0):
        return make_response({"wallet_id":walletid,"balance":Id["balance"],"wallet_user":{"user_id":walletid,"user_name":Id["user_name"]}},200)
    else:
        return make_response({"message": f"wallet with id: {walletid} was not found"},404)

@app.route("/api/wallets/<int:walletid>",methods=["PUT"])
def add_wallet(walletid):
    data = request.get_json()
    db = sqlite3.connect("store.db")
    db.cursor().execute(f"UPDATE User SET balance='{data['recharge']}' WHERE user_id = {walletid}")
    Id=db.cursor().execute(f"SELECT * FROM User WHERE user_id = {walletid}")
    db.commit()
    db.close()
    if(int(data['recharge'])<100 or int(data['recharge'])>10000):
        return make_response({"message": f"invalid amount: {walletid}"})
    if(db.cursor().rowcount > 0):
        return make_response({"wallet_id":walletid,"balance":data['recharge'],"wallet_user":{"user_id":walletid,"user_name":Id["user_name"]}})
    else:
        return make_response({"message": f"wallet with id: {walletid} was not found"},404)

#Purchase Ticket
@app.route("/api/tickets",methods=["POST"])
def Purchase_Ticket():
    data = request.get_json()
    return make_response("helo",201)

#optiamal routes
@app.route("/api/routes",methods=["GET"])
def optiamal():
    q = request.args.to_dict()
    return make_response("Ami lokman",201)
if __name__ == "main":
    app.run(debug=True)

