from flask import Flask, jsonify, request
import sys
from model import DBconn

app = Flask(__name__)

def spcall(qry, param, commit=False):
    try:
        dbo = DBconn()
        cursor = dbo.getcursor()
        cursor.callproc(qry, param)
        res = cursor.fetchall()
        if commit:
            dbo.dbcommit()
        return res
    except:
        res = [("Error: " + str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1]),)]
    return res


@app.route('/')
def index():
    return 'Protected Resources'

@app.route('/cities', methods=['GET'])
def cities():
    try:
        #getcities in spcall is a postgresql function
        cities = spcall("getcities", ())

        if 'Error' in str(cities[0][0]):
            return jsonify({'status': 'error', 'message': cities[0][0]})

        recs = []
        for r in cities:
            recs.append(r)
        return jsonify({'status': 'ok', 'cities': recs, 'count': len(recs)})

    except Exception as e:
        print(e)

@app.route('/clinics/<string:city>', methods=['GET'])
def clinics(city):
    try:
        clinics = spcall("getclinics", (city,))

        if 'Error' in str(clinics[0][0]):
            return jsonify({'status': 'error', 'message': clinics[0][0]})

        recs = []
        for r in clinics:
            recs.append(r)
        return jsonify({'status': 'ok', 'clinics': recs, 'count': len(recs)})

    except Exception as e:
        print(e)

@app.route('/counselors/<string:city>/<string:clinic>')
def counselor(city, clinic):
    try:
        counselor = spcall("getcounselor", (city, clinic,))

        if 'Error' in str(counselor[0][0]):
            return jsonify({'status': 'error', 'message': counselor[0][0]})

        recs = []
        for r in counselor:
            recs.append(r)
        return jsonify({'status': 'ok', 'counselors': recs, 'count': len(recs)})

    except Exception as e:
        print(e)

#after clicking the counselor of choice get the schedule of the preferred counselor, this will be called
#the parameter for code will come from counselor(city, clinic)
@app.route('/schedule/<string:code>')
def schedule(code):
    try:
        username = spcall("getusername", (code,))[0][0]

        print(username)

        if 'Error' in str(username[0][0]):
            return jsonify({'status': 'error', 'message': username[0][0]})


        schedule = spcall("getschedule", (username,))

        if 'Error' in str(schedule[0][0]):
            return jsonify({'status': 'error', 'message': schedule[0][0]})

        recs = []
        for r in schedule:
            recs.append({'monday':r[0], 'tuesday':r[1], 'wednesday':r[2], 'thursday':r[3], 'friday':r[4]})
        return jsonify({'status': 'ok', 'schedule': recs, 'count': len(recs)})

    except Exception as e:
        print(e)


@app.route('/newappointment', methods=['POST'])
def newappointment():
    params = request.get_json(force=True)
    city = params["city"]
    clinic = params["clinic"]
    unid = params["unid"]
    counselorcode = params["counselorcode"]
    date = params["date"]
    time = params["time"]

    try:
        res = spcall("newappointment", (city, clinic, unid, counselorcode, date, time),True)
        if 'Error' in res[0][0]:
            return jsonify({'status':'error', 'message': res[0][0]})
        return jsonify({'status':'ok', 'message': res[0][0]})
    except Exception as e:
        print(e)






if __name__ == '__main__':
    app.run(debug=True)
