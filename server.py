from flask import Flask, request, jsonify, render_template, send_file
import sqlite3


app = Flask(__name__)

# Sample in-memory data store
data_store = {}

@app.route('/audio')
def served_audio():
    return send_file('audio/mixkit-bell-notification-933.wav', mimetype='audio/wav')

@app.route('/admin')
def home():
    return render_template('admin.html')

@app.route('/user')
def render():
    return render_template('user.html')

@app.route('/colorPicker')
def colorPicker():
    return render_template('colorPicker.html')

@app.route('/')
def renderlogin():
    return render_template('login.html')

@app.route('/adduser', methods=['GET', 'POST', 'DELETE'])
def adduser():
    con = sqlite3.connect("save.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, pwd TEXT, ld TEXT)")

    if request.method == 'GET':
        return jsonify({
            'method': 'GET',        
            'name': cur.execute("SELECT name FROM users").fetchall(),
            'pwd': cur.execute("SELECT pwd FROM users").fetchall(),
            'ld': cur.execute('SELECT ld FROM users').fetchall()
        }), 200

    elif request.method == 'POST':
        new_data = request.json
        cur.execute("""
            INSERT INTO users (name, pwd, ld)
            VALUES (?, ?, ?)
        """, (
            new_data["name"],
            new_data["pwd"],
            new_data["ld"]
        ))
        con.commit()
        return jsonify({
        'method': 'POST',
        'message': 'User added',
        'name': cur.execute("SELECT name FROM users").fetchall(),
        'pwd': cur.execute("SELECT pwd FROM users").fetchall(),
        'ld': cur.execute("SELECT ld FROM users").fetchall()
        }), 201


    elif request.method == 'DELETE':
        keys_to_delete = request.json
        s = " AND ".join([f"""{k}='{v}'""" for k, v in keys_to_delete.items()])
        cur.execute(f"""DELETE FROM users WHERE {s}""")
        
        con.commit()

        return jsonify({
            'method': 'DELETE',
            'message': 'Data deleted',
            'name': cur.execute("SELECT name FROM users").fetchall(),
            'pwd': cur.execute("SELECT pwd FROM users").fetchall(),
            "ld": cur.execute("SELECT ld FROM users").fetchall()
        }), 200

@app.route('/themes', methods=['GET', 'POST', 'DELETE'])
def themes():
    con = sqlite3.connect('save.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS themes(username TEXT)")
    if request.method == 'GET':
        return jsonify({
            'method': 'GET',
            'names': cur.execute("SELECT username FROM themes").fetchall()
        }), 200

    elif request.method == 'POST':
        new_data = request.json
        cur.execute("""
            INSERT INTO themes (username)
            VALUES (?)
        """, (
            new_data["username"]
        ))
        con.commit()
        return jsonify({
        'method': 'POST',
        'message': 'Data added'
        }), 201


    elif request.method == 'DELETE':
        keys_to_delete = request.json
        cur.execute(f"""DELETE FROM themes WHERE {keys_to_delete}""")
        con.commit()

        return jsonify({
            'method': 'DELETE',
            'message': 'Data deleted'
        }), 200


@app.route('/adminadmin', methods=['GET', 'POST', 'PUT', 'DELETE'])
def admin():
    con = sqlite3.connect("save.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS events(name TEXT, month INTEGER, day INTEGER, year INTEGER, time TEXT, eventName TEXT)")

    if request.method == 'GET':
        return jsonify({
            'method': 'GET',        
            'name': cur.execute("SELECT name FROM events").fetchall(),
            'month': cur.execute("SELECT month FROM events").fetchall(),
            'day': cur.execute("SELECT day FROM events").fetchall(),
            'year': cur.execute("SELECT year FROM events").fetchall(),
            'time': cur.execute("SELECT time FROM events").fetchall(),
            'eventName': cur.execute("SELECT eventName FROM events").fetchall()
        }), 200

    elif request.method == 'POST':
        new_data = request.json
        cur.execute("""
            INSERT INTO events (name, month, day, year, time, eventName)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            new_data["name"],
            new_data["month"],
            new_data["day"],
            new_data["year"],
            new_data["time"],
            new_data["eventName"]
        ))
        con.commit()
        return jsonify({
        'method': 'POST',
        'message': 'Data added',
        'name': cur.execute("SELECT name FROM events").fetchall(),
        'month': cur.execute("SELECT month FROM events").fetchall(),
        'day': cur.execute("SELECT day FROM events").fetchall(),
        'year': cur.execute("SELECT year FROM events").fetchall(),
        'time': cur.execute("SELECT time FROM events").fetchall(),
        'eventName': cur.execute("SELECT eventName FROM events").fetchall()
        }), 201

    elif request.method == 'PUT':
        updated_data = request.json
        for key in updated_data:
            if key in data_store:
                data_store[key] = updated_data[key]
        return jsonify({
            'method': 'PUT',
            'message': 'Data updated',
            'data': data_store
        }), 200



    elif request.method == 'DELETE':
        keys_to_delete = request.json
        cur.execute("PRAGMA table_info(events)")
        fetch_types = cur.fetchall()
        columns_types = {}
        for i in fetch_types:
            columns_types.update({i[1] : i[2]})
        lsOfConditions = []
        for k, v in keys_to_delete.items():
            if columns_types[k] == 'TEXT':
                lsOfConditions.append(f"""{k}='{v}'""")
            elif columns_types[k] == 'INTEGER':
                lsOfConditions.append(f"""{k}={v}""")
            else:
                print(k, "not text!!")

        s = " AND ".join(lsOfConditions)
        cur.execute(f"""DELETE FROM events WHERE {s}""")
        con.commit()

        return jsonify({
            'method': 'DELETE',
            'message': 'Data deleted',
            'name': cur.execute("SELECT name FROM events").fetchall(),
            'month': cur.execute("SELECT month FROM events").fetchall(),
            'day': cur.execute("SELECT day FROM events").fetchall(),
            'year': cur.execute("SELECT year FROM events").fetchall(),
            'time': cur.execute("SELECT time FROM events").fetchall(),
            'eventName': cur.execute("SELECT eventName FROM events").fetchall()
        }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)
    # set host to 0.0.0.0 for public access
        # to access go to 10.0.0.12:5000
    # set host to 127.0.0.1 for localhost
    # app.run(debug=True, port=5000)
