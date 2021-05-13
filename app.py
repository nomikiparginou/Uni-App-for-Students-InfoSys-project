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

    if users.find_one({"username":data['username']}).count()==0:
        user = {"username": data['username'], "password": data['password']}
        users.insert_one(user)
        return Response(data['username']+" was added to the MongoDB", status=200,mimetype='application/json')
    else:
        return Response("A user with the given email already exists", status=200 ,mimetype='application/json')
    
'''
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

    user = users.find_one({"username":data["username"]})
    if user== None:
        return Response('No user found with that username' ,status=500,mimetype='application/json')
    if user["password"] == data["password"]:
        user_uuid = create_session(data["username"])
        res = {"uuid": user_uuid, "username": data["username"]}
        return Response(json.dumps(res), status=200, mimetype='application/json')
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

    uuid = request.headers.get['authorization']
    auth = is_session_valid(uuid)
    if auth == False:
        return Response('User was not authorized', status=401, mimetype="application/json")
    else:
        student = students.find_one({"email":data["email"]})
        return Response(json.dumps(student), status=200, mimetype='application/json')
    """
        Στα headers του request ο χρήστης θα πρέπει να περνάει το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα. 
            Π.Χ: uuid = request.headers.get['authorization']
        Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid. 
            * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401. 
            * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί. 

        Το συγκεκριμένο endpoint θα δέχεται σαν argument το email του φοιτητή και θα επιστρέφει τα δεδομένα του. 
        Να περάσετε τα δεδομένα του φοιτητή σε ένα dictionary που θα ονομάζεται student.
        
        Σε περίπτωση που δε βρεθεί κάποιος φοιτητής, να επιστρέφεται ανάλογο μήνυμα.
    """
'''
    # Η παρακάτω εντολή χρησιμοποιείται μόνο στη περίπτωση επιτυχούς αναζήτησης φοιτητών (δηλ. υπάρχει φοιτητής με αυτό το email).

# # ΕΡΩΤΗΜΑ 4: Επιστροφή όλων των φοιτητών που είναι 30 ετών
# @app.route('/getStudents/thirties', methods['GET'])
# def get_students_thirty():
#     """
#         Στα headers του request ο χρήστης θα πρέπει να περνάει το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα. 
#             Π.Χ: uuid = request.headers.get['authorization']
#         Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid. 
#             * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401. 
#             * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί. 
        
#         Το συγκεκριμένο endpoint θα πρέπει να επιστρέφει τη λίστα των φοιτητών οι οποίοι είναι 30 ετών.
#         Να περάσετε τα δεδομένα των φοιτητών σε μία λίστα που θα ονομάζεται students.
        
#         Σε περίπτωση που δε βρεθεί κάποιος φοιτητής, να επιστρέφεται ανάλογο μήνυμα και όχι κενή λίστα.
#     """
    
#     # Η παρακάτω εντολή χρησιμοποιείται μόνο σε περίπτωση επιτυχούς αναζήτησης φοιτητών (δηλ. υπάρχουν φοιτητές που είναι 30 ετών).
#     return Response(json.dumps(students), status=200, mimetype='application/json')

# # ΕΡΩΤΗΜΑ 5: Επιστροφή όλων των φοιτητών που είναι τουλάχιστον 30 ετών
# @app.route('/getStudents/oldies', methods['GET'])
# def get_students_thirty():
#     """
#         Στα headers του request ο χρήστης θα πρέπει να περνάει και το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα. 
#             Π.Χ: uuid = request.headers.get['authorization']
#         Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid. 
#             * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401. 
#             * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί. 
        
#         Το συγκεκριμένο endpoint θα πρέπει να επιστρέφει τη λίστα των φοιτητών οι οποίοι είναι 30 ετών και άνω.
#         Να περάσετε τα δεδομένα των φοιτητών σε μία λίστα που θα ονομάζεται students.
        
#         Σε περίπτωση που δε βρεθεί κάποιος φοιτητής, να επιστρέφεται ανάλογο μήνυμα και όχι κενή λίστα.
#     """

#     # Η παρακάτω εντολή χρησιμοποιείται μόνο σε περίπτωση επιτυχούς αναζήτησης φοιτητών (υπάρχουν φοιτητές που είναι τουλάχιστον 30 ετών).
#     return Response(json.dumps(students), status=200, mimetype='application/json')

# # ΕΡΩΤΗΜΑ 6: Επιστροφή φοιτητή που έχει δηλώσει κατοικία βάσει email 
# @app.route('/getStudentAddress', methods=['GET'])
# def get_student():
#     # Request JSON data
#     data = None 
#     try:
#         data = json.loads(request.data)
#     except Exception as e:
#         return Response("bad json content",status=500,mimetype='application/json')
#     if data == None:
#         return Response("bad request",status=500,mimetype='application/json')
#     if not "email" in data:
#         return Response("Information incomplete",status=500,mimetype="application/json")

#     """
#         Στα headers του request ο χρήστης θα πρέπει να περνάει και το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα. 
#             Π.Χ: uuid = request.headers.get['authorization']
#         Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid. 
#             * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401. 
#             * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί. 

#         Το συγκεκριμένο endpoint θα δέχεται σαν argument το email του φοιτητή. 
#         * Στη περίπτωση που ο φοιτητής έχει δηλωμένη τη κατοικία του, θα πρέπει να επιστρέφεται το όνομα του φοιτητή η διεύθυνσή του(street) και ο Ταχυδρομικός Κωδικός (postcode) της διεύθυνσης αυτής.
#         * Στη περίπτωη που είτε ο φοιτητής δεν έχει δηλωμένη κατοικία, είτε δεν υπάρχει φοιτητής με αυτό το email στο σύστημα, να επιστρέφεται μήνυμα λάθους. 
        
#         Αν υπάρχει όντως ο φοιτητής με δηλωμένη κατοικία, να περάσετε τα δεδομένα του σε ένα dictionary που θα ονομάζεται student.
#         Το student{} να είναι της μορφής: 
#         student = {"name": "Student's name", "street": "The street where the student lives", "postcode": 11111}
#     """

#     # Η παρακάτω εντολή χρησιμοποιείται μόνο σε περίπτωση επιτυχούς αναζήτησης φοιτητή (υπάρχει ο φοιτητής και έχει δηλωμένη κατοικία).
#     return Response(json.dumps(student), status=200, mimetype='application/json')

# # ΕΡΩΤΗΜΑ 7: Διαγραφή φοιτητή βάσει email 
# @app.route('/deleteStudent', methods=['DELETE'])
# def delete_student():
#     # Request JSON data
#     data = None 
#     try:
#         data = json.loads(request.data)
#     except Exception as e:
#         return Response("bad json content",status=500,mimetype='application/json')
#     if data == None:
#         return Response("bad request",status=500,mimetype='application/json')
#     if not "email" in data:
#         return Response("Information incomplete",status=500,mimetype="application/json")

#     """
#         Στα headers του request ο χρήστης θα πρέπει να περνάει και το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα. 
#             Π.Χ: uuid = request.headers.get['authorization']
#         Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid. 
#             * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401. 
#             * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί. 

#         Το συγκεκριμένο endpoint θα δέχεται σαν argument το email του φοιτητή. 
#         * Στη περίπτωση που υπάρχει φοιτητής με αυτό το email, να διαγράφεται από τη ΒΔ. Να επιστρέφεται μήνυμα επιτυχούς διαγραφής του φοιτητή.
#         * Διαφορετικά, να επιστρέφεται μήνυμα λάθους. 
        
#         Και στις δύο περιπτώσεις, να δημιουργήσετε μία μεταβλήτη msg (String), η οποία θα περιλαμβάνει το αντίστοιχο μήνυμα.
#         Αν βρεθεί ο φοιτητής και διαγραφεί, στο μήνυμα θα πρέπει να δηλώνεται και το όνομά του (πχ: msg = "Morton Fitzgerald was deleted.").
#     """

#     return Response(msg, status=200, mimetype='application/json')

# # ΕΡΩΤΗΜΑ 8: Εισαγωγή μαθημάτων σε φοιτητή βάσει email 
# @app.route('/addCourses', methods=['PATCH'])
# def add_courses():
#     # Request JSON data
#     data = None 
#     try:
#         data = json.loads(request.data)
#     except Exception as e:
#         return Response("bad json content",status=500,mimetype='application/json')
#     if data == None:
#         return Response("bad request",status=500,mimetype='application/json')
#     if not "email" in data or not "courses" in data:
#         return Response("Information incomplete",status=500,mimetype="application/json")

#     """
#         Στα headers του request ο χρήστης θα πρέπει να περνάει και το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα. 
#             Π.Χ: uuid = request.headers.get['authorization']
#         Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid. 
#             * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401. 
#             * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί. 

#         Το συγκεκριμένο endpoint θα δέχεται σαν argument το email του φοιτητή. Στο body του request θα πρέπει δίνεται ένα json της παρακάτω μορφής:
        
#         {
#             email: "an email",
#             courses: [
#                 {'course 1': 10, 
#                 {'course 2': 3 }, 
#                 {'course 3': 8},
#                 ...
#             ]
#         } 
        
#         Η λίστα courses έχει μία σειρά από dictionary για τα οποία τα key αντιστοιχούν σε τίτλο μαθημάτων και το value στο βαθμό που έχει λάβει ο φοιτητής σε αυτό το μάθημα.
#         * Στη περίπτωση που υπάρχει φοιτητής με αυτό το email, θα πρέπει να γίνει εισαγωγή των μαθημάτων και των βαθμών τους, σε ένα νέο key του document του φοιτητή που θα ονομάζεται courses. 
#         * Το νέο αυτό key θα πρέπει να είναι μία λίστα από dictionary.
#         * Αν δε βρεθεί φοιτητής με αυτό το email να επιστρέφεται μήνυμα λάθους. 
#     """

#     return Response(msg, status=200, mimetype='application/json')

# # ΕΡΩΤΗΜΑ 9: Επιστροφή περασμένων μαθημάτων φοιτητή βάσει email
# @app.route('/getPassedCourses', methods=['GET'])
# def get_courses():
#     # Request JSON data
#     data = None 
#     try:
#         data = json.loads(request.data)
#     except Exception as e:
#         return Response("bad json content",status=500,mimetype='application/json')
#     if data == None:
#         return Response("bad request",status=500,mimetype='application/json')
#     if not "email" in data:
#         return Response("Information incomplete",status=500,mimetype="application/json")

#     """
#         Στα headers του request ο χρήστης θα πρέπει να περνάει και το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα. 
#             Π.Χ: uuid = request.headers.get['authorization']
#         Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid. 
#             * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401. 
#             * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί. 

#         Το συγκεκριμένο endpoint θα δέχεται σαν argument το email του φοιτητή.
#         * Στη περίπτωση που ο φοιτητής έχει βαθμολογία σε κάποια μαθήματα, θα πρέπει να επιστρέφεται το όνομά του (name) καθώς και τα μαθήματα που έχει πέρασει.
#         * Στη περίπτωη που είτε ο φοιτητής δεν περάσει κάποιο μάθημα, είτε δεν υπάρχει φοιτητής με αυτό το email στο σύστημα, να επιστρέφεται μήνυμα λάθους.
        
#         Αν υπάρχει όντως ο φοιτητής με βαθμολογίες σε κάποια μαθήματα, να περάσετε τα δεδομένα του σε ένα dictionary που θα ονομάζεται student.
#         Το dictionary student θα πρέπει να είναι της μορφής: student = {"course name 1": X1, "course name 2": X2, ...}, όπου X1, X2, ... οι βαθμολογίες (integer) των μαθημάτων στα αντίστοιχα μαθήματα.
#     """

#     # Η παρακάτω εντολή χρησιμοποιείται μόνο σε περίπτωση επιτυχούς αναζήτησης φοιτητή (υπάρχει ο φοιτητής και έχει βαθμολογίες στο όνομά του).
#     return Response(json.dumps(student), status=200, mimetype='application/json')

# # Εκτέλεση flask service σε debug mode, στην port 5000.
@app.route('/getallstudents', methods=['GET'])
def get_all_students():
    iterable = students.find({})
    output = []
    for student in iterable:
        student['_id'] = None
        output.append(student)
    return jsonify(output)
 
if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0', port=5000)
