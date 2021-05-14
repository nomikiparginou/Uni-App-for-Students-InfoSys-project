#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
import json
import uuid
import time

# Connect to our local MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Choose database
db = client['InfoSys']

# Choose collections
students = db['Students']
users = db['Users']

# Initiate Flask App
app = Flask(__name__)

users_sessions = {}

def create_session(username):
    user_uuid = str(uuid.uuid1())
    users_sessions[user_uuid] = (username, time.time())
    return user_uuid  

def is_session_valid(user_uuid):
    return user_uuid in users_sessions

# ΕΡΩΤΗΜΑ 1: Δημιουργία χρήστη
@app.route('/createUser', methods=['POST'])
def create_user():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "username" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    if users.find({"username":data['username']}).count() == 0 :
        user = {"username": data['username'], "password": data['password']}
        users.insert_one(user)
        return Response(data['username']+" was added to the MongoDB", status=200,mimetype='application/json')
    else:
        return Response("A user with the given email already exists", status=200 ,mimetype='application/json')
    

# ΕΡΩΤΗΜΑ 2: Login στο σύστημα
@app.route('/login', methods=['POST'])
def login():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "username" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    user = users.find_one({"username":data['username']})
    if user == None:
        return Response('No user found with that username' ,status=500,mimetype='application/json')
    if user['password'] == data['password']:
        user_uuid = create_session(data['username'])
        res = {"uuid": user_uuid, "username": data['username']}
        return Response(json.dumps(res , indent = 4), status=200, mimetype='application/json')
    else:
        return Response("Wrong username or password.", status=400, mimetype='application/json')

# ΕΡΩΤΗΜΑ 3: Επιστροφή φοιτητή βάσει email
@app.route('/getStudent', methods=['GET'])
def get_student():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    uuid = request.headers.get('authorization')
    auth = is_session_valid(uuid)
    if auth == False:
        return Response('User was not authorized', status=401, mimetype="application/json")
    else:
        student = students.find_one({"email":data['email']})
        if student != None:
            student['_id'] = None
            return Response(json.dumps(student, indent = 4), status=200, mimetype='application/json')
        else:
            return Response('No user with that email found')
   


# ΕΡΩΤΗΜΑ 4: Επιστροφή όλων των φοιτητών που είναι 30 ετών
@app.route('/getStudents/thirties', methods=['GET'])
def get_students_thirty():
 
    uuid = request.headers.get('authorization')
    auth = is_session_valid(uuid)
    if auth == False:
        return Response('User was not authorized', status=401, mimetype="application/json")
    else:
        studentsThirty = students.find({"yearOfBirth": (1991)})
        thirty = []
        if studentsThirty :
            for student in studentsThirty:
                student['_id'] = None
                thirty.append(student)
            return Response (json.dumps(thirty, indent=4))
        else :
            return response("No students at the age of 30")        

	
     
# ΕΡΩΤΗΜΑ 5: Επιστροφή όλων των φοιτητών που είναι τουλάχιστον 30 ετών
@app.route('/getStudents/oldies', methods=['GET'])
def get_students_oldies():
    
    uuid = request.headers.get('authorization')
    auth = is_session_valid(uuid)
    if auth == False:
        return Response('User was not authorized', status=401, mimetype="application/json")
    else:
        studentsOldies = students.find({"yearOfBirth":{ "$lt": 1991 }})
        oldies = []
        if studentsOldies:
            for student in studentsOldies:
                student['_id'] = None
                oldies.append(student)
            return Response (json.dumps(oldies, indent=4), status=200, mimetype="application/json")
        else:
            return response("No students at and over the age of 30")        



# ΕΡΩΤΗΜΑ 6: Επιστροφή φοιτητή που έχει δηλώσει κατοικία βάσει email 
@app.route('/getStudentAddress', methods=['GET'])
def get_student_address():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
         
    uuid = request.headers.get('authorization')
    auth = is_session_valid(uuid)
    if auth == False:
        return Response('User was not authorized', status=401, mimetype="application/json")
    else:
        student = students.find_one({"$and":[{"email":data['email']}, {"address":{"$ne":None}}]})
        if student:
            student = {'name':student["name"],'street':student["address"][0]["street"], 'postcode':student["address"][0]["postcode"]}
            return Response (json.dumps(student, indent=4), status=200, mimetype="application/json")
        else:
            return Response("No student with that email and a declared address",status=500,mimetype="application/json")



# ΕΡΩΤΗΜΑ 7: Διαγραφή φοιτητή βάσει email 
@app.route('/deleteStudent', methods=['DELETE'])
def delete_student():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    uuid = request.headers.get('authorization')
    auth = is_session_valid(uuid)
    if auth == False:
        return Response('User was not authorized', status, mimetype="application/json")
    else:
        student = students.find_one({"email":data['email']})
        if student:
            msg = "Student "+student['name']+" was deleted from the database."
            students.delete_one({"email":student['email']})
            status=200
        else:
            email = {"email":data['email']}
            msg = "No student under the email " +data['data']
            status=500
        return Response(msg,status,mimetype="application/json")



# ΕΡΩΤΗΜΑ 8: Εισαγωγή μαθημάτων σε φοιτητή βάσει email 
@app.route('/addCourses', methods=['PATCH'])
def add_courses():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "courses" in data:
        return Response("Information incomplete",status=500,mimetype='application/json')

    uuid = request.headers.get('authorization')
    auth = is_session_valid(uuid)
    if auth == False:
        return Response('User was not authorized', status=401, mimetype='application/json')
    else:
        student = students.find_one({"email":data['email']})
        if student:
            students.update_one({"email":data['email']},{"$set": {"courses":data['courses']}})
            msg = "The given courses and their scores were added to database for "+student['name']
            status=200
        else:
            msg = "No student with the given email: "+student['email']
            status=500
        return Response(msg, status, mimetype='application/json')



# ΕΡΩΤΗΜΑ 9: Επιστροφή περασμένων μαθημάτων φοιτητή βάσει email
@app.route('/getPassedCourses', methods=['GET'])
def get_courses():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    uuid = request.headers.get('authorization')
    auth = is_session_valid(uuid)
    if auth == False:
        return Response('User was not authorized', status=401, mimetype='application/json')
    else:
        student = students.find_one({"email":data['email']})
        if student:
            student['_id'] = None
            if "courses" not in student:
                return Response("Student has no courses")
            else:
                passed = {}
                courseList = {"courses":student['courses']}
                for item in courseList.values():
                    for course in item:
                        for score in course:
                            if course.get(score) >= 5:
                                passed[score] = course.get(score)
                if len(passed) == 0:
                    return Response("Student "+student['name']+" has not passed any courses.", status=200, mimetype='application/json')
                else:
                    return Response(json.dumps(passed, indent=4), status=200, mimetype='application/json')
        else:
            return Response("No student with the given email: "+data['email'], status=500, mimetype='application/json')

 
if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0', port=5000)
