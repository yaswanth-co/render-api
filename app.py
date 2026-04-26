from flask import Flask,request,jsonify
import sqlite3
import os

app = Flask('__name__')

#funtion to display info doc
@app.route('/')
def doc():
    return {
        "message" : "student API",
        "endpoints" : {
            "GET /students" : "get all students",
            "POST /students" : "add students",
            "GET /students/<name>" : "get one student",
            "PUT /students/<name>" : "update student marks",
            "DELETE /student/<name>" : "delete student"
        }
    }

#versioning for later upgrades
@app.route("/api/v1/students")

#funtion to check the health
@app.route("/health")
def health():
    return {"status": "ok"}

#creating table students
def init_db():
    con = sqlite3.connect("students.db")
    cursor = con.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            name TEXT PRIMARY KEY,
            marks INTEGER,
            grade TEXT
        )
    """)

    con.commit()
    con.close()

init_db()

#function for grades
def get_grade(marks):
    if marks>90:
        return "A"
    elif marks>80:
        return "B"
    elif marks>70:
        return "C"
    elif marks>60:
        return "D"
    elif marks>34:
        return "E"
    else:
        return "FAIL"

#funtion for insert the movies
@app.route('/students',methods=['POST'])
def add_students():

    #creating and connecting an database file 
    con = sqlite3.connect("students.db")
    cursor = con.cursor()

    data = request.get_json()

    if isinstance(data,dict):
        data = [data]

    count = 0

    for student in data:
        name = student.get('name')
        marks = student.get('marks')

        if not name or not isinstance(marks,int):
            return jsonify({"error" : "invalid input"}), 400
        
        grade = get_grade(marks)
        
        try:
            cursor.execute(
            "INSERT INTO students(name,marks,grade) VALUES(?,?,?)",
            (name,marks,grade)
            )
            con.commit()
            
        except sqlite3.IntegrityError:
            return jsonify({"error" : f"{name} is already exists"}), 409
        
        count+=1
    con.close()
    return jsonify({
        "status" : "success",
        "add" : count
    }), 201

#funtion to fetch all data
@app.route("/students",methods=['GET'])
def get_students():

    #creating and connecting an database file 
    con = sqlite3.connect("students.db")
    cursor = con.cursor()

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    con.close()

    result = {}

    for row in rows:
        result[row[0]] = {
            "marks" : row[1],
            "grade" : row[2]
        }
    return jsonify({
        "total" : len(result),
        "data" : result
    }), 200

#funtion to fetch data by name
@app.route('/students/<name>',methods=['GET'])
def get_student(name):

    #creating and connecting an database file 
    con = sqlite3.connect("students.db")
    cursor = con.cursor()

    cursor.execute("SELECT * FROM students WHERE name=?",(name,))
    result = cursor.fetchone()
    con.close()

    if not result:
        return jsonify({"error" : "name not found"}), 404
    
    return jsonify({
        "name" : result[0],
        "marks" : result[1],
        "grade" : result[2]
    }), 200

#funtion to delete an row
@app.route("/students/<name>",methods=["DELETE"])
def delete_student(name):

    #creating and connecting an database file 
    con = sqlite3.connect("students.db")
    cursor = con.cursor()    

    cursor.execute("DELETE FROM students WHERE name=?",(name,))
    con.commit()

    if cursor.rowcount == 0:
        return jsonify({"error" : "student not found"}), 404

    con.close()

    return jsonify({"status" : "deleted"}), 200

#funtion to update marks
@app.route('/students/<name>',methods=['PUT'])
def update_student(name):

    #creating and connecting an database file 
    con = sqlite3.connect("students.db")
    cursor = con.cursor()

    data = request.get_json()
    
    if not data or 'marks' not in data:
        return jsonify({"error" : "marks is required"}), 400
    
    try:
        marks = int(data['marks'])
    except:
        return jsonify({"error" : "marks must be in integer format"}), 400
    
    grade = get_grade(marks)

    cursor.execute("UPDATE students SET marks=?,grade=? WHERE name=?",(marks,grade,name))
    con.commit()

    if cursor.rowcount == 0:
        return jsonify({"error" : "name not found"}), 404
    
    con.close()

    return jsonify({"status" : "data updated"}), 200


app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))