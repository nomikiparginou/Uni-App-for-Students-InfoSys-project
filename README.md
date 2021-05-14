# Πρώτη Υποχρωτική Εργασια 
## Πληροφορικά Συστήματα, Τμήμα Ψηφιακών Συστημάτων
### Όνομα : Νομική Παργινού
###  AM : E18130


## ΕΡΩΤΗΜΑ 1: Δημιουργία χρήστη
> Το πρωτο endpoint χρησιμοποιείται για την δημιουργία και εισαγωγή καινούριου χρήστη στη βάση δεδομένων. Εκτελέιται με μια εντολή curl όπως η παρακάτω:
```` bash 
 curl -X POST localhost:5000/createUser -d '{"username":"nomikipar","password":"7253738"}' -H Content-Type:application/json
````
> Στη μεταβλητη data εισάγεται το json που έδωσε ο χρήστης και περιέχει το username και το password του user που θέλει να δημιουργηθεί. Αρχικά ελέγχεται εάν δώθηκε input και άν δώθηκε σωστά. ´Αν όχι, τότε εμφανίζονται ανάλογα ενημερωτικά μηνύματα και τερμαρτίζει. Άν όλα έχουν δωθεί σωστά, τότε ελέγχεται εάν υπάρχει ήδη χρήστης με το username που δώθηκε. Αν βρεθεί κάποιος τότε εμφανίζει *"A user with the given email already exists"*, αλλίως εισάγει τα στοιχεία που δώθηκαν σε μια μεταβλητή **user** και εκτελεί το query "*insert_one(user)*" και μας ενημερώνει πως ο χρήστης εισάχθηκε επιτυχώς στη βάση εμφανίζοντας το μήνυμα *"nomikipar was added to the MongoDB"*.
>  
**Κώδικας**
```` python
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
````

## ΕΡΩΤΗΜΑ 2: Login στο σύστημα
> Το δεύτερο endpoint χρησιμοποείται για να κάνει ο χρήστης login στο στη βάση. Εισάγει τα στοιχεία του ως χρήστης με μια curl εντολή της παρακάτω μορφής:
````bash
curl -X POST localhost:5000/login -d '{"username":"nomikipar","password":"7253738"}' -H Content-Type:application/json

````
> Όπως και στο παραπάνω ερώτημα ελέχγονται τα στοιχεία που έχουν δωθεί για input. Στη συνέχεια, εκτελείται το query *"find_one"* με argument το username που έδωσε ο χρηστης, με σκοπό να ελεχθεί εάν υπάρχει στη βάση χρήστης με το username που δώθηκε και το αποτέλεσμα εκχωρείται στη μεταβλητή user. Άν η μεταβλητή user είναι άδεια, δηλαδή δεν βρέθηκε χρήστης με αυτό το username, τότε εμφανίζεται το μήνυμα *"No user found with that username"*. Αν ο χρήστης υπάρχει στο σύστημα, τότε ελέγχεται εάν ο κωδικός που αντιστοιχεί σε αυτόν τον χρήστη είναι ο ίδιος με αυτόν που εδωσε ο χρηστης ως input. Άν δεν ταυτίζονται εμφανιζεται το μήνυμα *"Wrong username or password."*, ενώ αν ταυτίζονται καλείται η συνάρτηση create_session με argument το username και μας επιστρέφεται πίσω το uuid. Στη συνεχεια δημιουργείται η μεταβλητή **res** στη οποία εκχωρείται το uuid που πήραμε, καθώς και το username του χρήστη και μετά εκτυπώνοται σε μορφή:
````json
{
    "uuid": "c6c65dea-b3ed-11eb-8545-0800273bc3c2",
    "username": "nomikipar"
} 
````

**Κώδικας**
````python
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
  ````
  
  ## ΕΡΩΤΗΜΑ 3: Επιστροφή φοιτητή βάσει email
  
  > Το συγκεκριμένο endpoint δέχεται ως input ένα email και επιστρέφει τον χρήστη στον οποίο αντιστοιχεί, εφόσον υπάρχει. Εκτελείται με μια εντολή curl της μορφής:
  
````bash
curl -X GET localhost:5000/getStudent -d '{"email":"mcgowanrobinson@ontagene.com"}'  -H "Authorization: c6c65dea-b3ed-11eb-8545-0800273bc3c2"  -H Content-Type:application/json
````
> Μετά τον έλεγχο των δεδομένων του input, παίρνουμε τo uuid του χρήστη που έχει κάνει login εκείνη τη στιγμή με το **request.headers.get('authorization')** και στη συνέχεια καλείται η συνάρτηση **is_session_valid** για την αυθεντικοποιήση του. Αν η αυθεντικοποιήση αποτύχει εμφανίζεται το μήνυμα **'User was not authorized'**. Αν ο χρήστης αυθεντικοποιηθεί με επιτυχία, τότε εκτελείται το query **find_one** πάνω στο collection students για να βρεθεί ο χρήστης στον οποίο αντιστοιχεί το email και επιστρεφεται το αποτέλεσμα στην μεταβλητη **student**. Αν η μεταβλητή student δεν είναι κενή, δηλαδή βρέθηκε χρήστης, τότε το **_id** στη συγκεκριμένη μεταβλητή θέτεται σε *"Νοne", καθώς είναι πεδίο που δεν πρέπει να εμφανιστεί και τέλος εκτυπώνεται ένα json ως αποτέλσμα με τα στοιχεία του χρήστη. Αλλιώς εμφανίζεται το μήνυμα *'No user with that email found'*. 
```` json
{
    "_id": null,
    "name": "Mcgowan Robinson",
    "email": "mcgowanrobinson@ontagene.com",
    "yearOfBirth": 1988,
    "address": [
        {
            "street": "Frank Court",
            "city": "Bannock",
            "postcode": 18295
        }
    ]
} 
````
**Κώδικας**

```` python
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
  ````
## ΕΡΩΤΗΜΑ 4: Επιστροφή όλων των φοιτητών που είναι 30 ετών

> Σε αυτο το endpoint επιστρέφονται όλοι οι students είναι ακριβώς 30 ετών και εκτελείται με εντολή curl της μορφής:
```` bash
 curl -X GET localhost:5000/getStudents/thirties -H "Authorization: ebfcbb78-b3f1-11eb-b0d6-0800273bc3c2"  -H Content-Type:application/json
````
> Αρχικά αυθεντικοποιεί τον χρήστη με τον ίδιο τρόπο όπως και στο προηγούμενο ερώτημα και μετά την επιτυχής αυθεντικοποιήση του εκτελεί το **find** query στο student collection με argument το *"yearOfBirth"* να ισουται με 1991 (αφού όσοι είναι τώρα 30 έχουν γεννηθεί το 1991). Το αποτέλεσμα του query εκχωρείται στη μεταβλητή studentThirty και στη περίπτωση που δεν είναι κενή, ο κάθε φοιτητής μέσα σε αυτή γίνεται append στη λίστα thirty. Επιπλέον, η τιμή του *_id* του κάθε φοιτητή θέτεται σε **None** και μόλις έχουν περαστεί όλοι οι φοιτητλες στη λίστα thirty, τότε εμφανίζεται στον χρήστη σε μορφή json. Αν τελικά η μεταβλητή students ήταν κενή και δεν βρέθηκαν φοιτηττες της ηλικίας των 30 εμφανίζεται το μήνυμα *"No students at the age of 30"*.
````json
[
    {
        "_id": null,
        "name": "Browning Rasmussen",
        "email": "browningrasmussen@ontagene.com",
        "yearOfBirth": 1991,
        "address": [
            {
                "street": "Doone Court",
                "city": "Cuylerville",
                "postcode": 17331
            }
        ]
    },
    {
        "_id": null,
        "name": "Bennett Baker",
        "email": "bennettbaker@ontagene.com",
        "yearOfBirth": 1991,
        "gender": "male"
    }
] 
````

**Κώδικας**
````python
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
 ````
## ΕΡΩΤΗΜΑ 5: Επιστροφή όλων των φοιτητών που είναι τουλάχιστον 30 ετών

> Σε αυτο το endpoint εμφανιζονται ολοι οι φοιτητές που είναι απο 30 ετών και άνω και εκτελέιται με μια εντολή curl της μορφής:
````bash
curl -X GET localhost:5000/getStudents/oldies -H "Authorization: ebfcbb78-b3f1-11eb-b0d6-0800273bc3c2"  -H Content-Type:application/json
````
> Στην αρχή αυθεντικοποιείται ο χρηστης ομοίως με τα προηγούμενα ερωτήματα και με την επιτυχή αυθεντικοποιήση του εκτελείται το query **find** στο collection students για όσους μαθητές έχουν *"yearOfBirth*" μικρότερο ή ίσο του 1991. Το αποτέλεσμα επιστρέφεται στη μεταβλητή studentOldies και αν δεν είναι κενή, τότε κάθε μαθητής που βρίσκεται σε αυτό το dictionary γίνεται append στη λίστα **oldies**. Τέλος, εμφανίζεται στον χρήστη το json με τους μαθητές που είναι απο 30 και άνω. Στη περίπτωση που το studentOdlies είναι κενό, δηλαδη δεν βρέθηκα μαθητες των 30 και άνω, τότε εμφανίζεται το μήνυμα *"No students at and over the age of 30"*.

````json
[
{
        "_id": null,
        "name": "Elba Farley",
        "email": "elbafarley@ontagene.com",
        "yearOfBirth": 1981,
        "gender": "female"
    },
    {
        "_id": null,
        "name": "Stein Blanchard",
        "email": "steinblanchard@ontagene.com",
        "yearOfBirth": 1978,
        "gender": "male"
    },
    {
        "_id": null,
        "name": "Gracie Rosales",
        "email": "gracierosales@ontagene.com",
        "yearOfBirth": 1982,
        "gender": "female"
    },

]
````
**Κώδικας**
````python
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
````

## ΕΡΩΤΗΜΑ 6: Επιστροφή φοιτητή που έχει δηλώσει κατοικία βάσει email 

> Το συγκεκριμένο endpoint δέχεται ως input το email ενός μαθητή και εμφανίζει τα στοιχεία της κατοικίας του, εφόσον τα έχει δηλώσει. Εκτελείται με μια εντολή curl της μορφής:
````bash
curl -X GET localhost:5000/getStudentAddress -d '{"email":"hebertvazquez@ontagene.com"}'  -H "Authorization: 5163b7ec-b400-11eb-9257-0800273bc3c2"  -H Content-Type:application/json
````
> Στην αρχή ελέγχεται το input που έχει δωθεί και αυθεντικοποιείται ο χρήστης. Στη συνέχεια εκτελείται το query **find_one** με το email που δωθηκε απο τον χρηστη και ταυτοχρονα το πεδίο address να μην ισούται με **"None"**. To αποτέλεσμα περνάει στη μεταβλητή student και ελέχεται μετά αν δεν είναι κενή. Αν είναι τοτε εμφανίζεται το μήνυμα *"No student with that email and a declared address"*, ενω στη περίπτωση που δεν είναι, τότε κρατάμε στο student μόνο το πεδίο με το όνομα του και απο το dictionary με το *address* κρατάμε το *street* και το *postcode*. Τέλος εμφανίζεται το αποτέλσμα στον χρήστη σε μορφή json. 
````json
{
    "name": "Hebert Vazquez",
    "street": "Woodside Avenue",
    "postcode": 14943
}  
````
**Κώδικας**
````python
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
````
## ΕΡΩΤΗΜΑ 7: Διαγραφή φοιτητή βάσει email

> Αυτό το endpoint δέχεται το email ενός μαθητή και τον διαγράφει απο το σύστημα. Εκτελείται απο μια εντολή curl της μορφής:
````bash
curl -X DELETE localhost:5000/deleteStudent -d '{"email":"dixiecombs@ontagene.com"}'  -H "Authorization: 5163b7ec-b400-11eb-9257-0800273bc3c2"  -H Content-Type:application/json
````
> Αφού ελεγχθεί το input του χρήστη και αυθεντικοποιηθεί και ο ίδιος, αναζητείται στο σύστημα με το query **find_one** σε ποιον χρήστη αντιστοιχεί το email που δώθηκε και το αποτέλεσμα εκχωρείται στη μεταβλητή student. Αν η student είναι κενη, δηλαδή δεν βρέθηκε χρήστης, τότε στη μεταβλητή msg εκχωρειται το ανάλογο μήνυμα αποτυχίας εύρεσης του μαθητή. Αν όμως έχει περιεχόμενα, τότε πριν τη διαγραφή του, κρατάμε το όνομα του στη μεταβλητή name για να τη προσθέσουμε στο msg για το μήνυμα επιτυχίας και στη συνέχεια τον διαγράφουμε με το query **delete_one**. Τέλος, εμφανίζεται στον χρήστη το ανάλογο μήνυμα. 

````python
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
````

## ΕΡΩΤΗΜΑ 8: Εισαγωγή μαθημάτων σε φοιτητή βάσει email 

> Αυτο το endpoint δέχεται ως input ένα email μαθητή και ενα μια λίστα απο courses καθώς και τον βαθμό τους. Εκτελείται με εντολή curl της μορφής:
````bash
curl -X PATCH localhost:5000/addCourses -d '{"email":"moongriffin@ontagene.com","courses":[{"Information Systems":5, "XML":7, "DataBases":9, "Probabilities":3, "Multimedia Communications":4}]}' -H "Authorization: 5163b7ec-b400-11eb-9257-0800273bc3c2" -H Content-Type:application/json
````
> Αφού ελεχθεί το input του χρήστη και αυθεντικοποιηθεί και ο ίδιος, αναζητείται με το query **find_one** ο χρήστης στον οποίο αντιστοιχεί το email που δώθηκε και επιστρέφεται στην μεταβλητή student. Αν αυτή η μεταβλητή είναι κενή, τότε εμφανίζεται μήνυμα αποτυχίας, ενώ αν δεν είναι κενή, τότε εκτελεί το query **update_one** στον μαθητη αυτον προσθέτοντας του το πεδίο *"courses"* και μέσα σε αύτο τη λίστα με τα μαθήματα που έδωσε ο χρήστης. Τέλος εμφανίζει μήνυμα επιτυχίας της μορφής *"The given courses and their scores were added to database for Moon Griffin "*.

````python
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
````

## ΕΡΩΤΗΜΑ 9: Επιστροφή περασμένων μαθημάτων φοιτητή βάσει email

> Αυτο το endpoint δέχεται ως input το email ενός μαθητή και επιστρέφει τα περασμένα μαθήματα του, εφόσον υπάρχουν. Εκτελείται με μια εντολή curl της μορφής:
````bash
curl -X GET localhost:5000/getPassedCourses -d '{"email":"moongriffin@ontagene.com"}'  -H "Authorization: 5163b7ec-b400-11eb-9257-0800273bc3c2"  -H Content-Type:application/json
````
> Μετά τον ελέγχο του input και την επιτυχής αυθεντικοποίηση του χρήστη, εκτελείται το query **find_one** για την αναζήτη του φοιτητή στον οποίο αντιστοιχεί το email που δώθηκε και εκχωρείται το αποτέλεσμα στην μεταβλητή *student*. Γίνεται έλεγχος για το περιεχόμενο της μεταβλητής και άν είναι κενή, τότε επιστρέφεται το μήνυμα *"No student with the given email"*. Αλλιώς, ελέγχει εάν το πεδίο **courses** συμπεριλαμβάνεται μέσα στη μεταβλητη με τις πληροφορίες του φοιτητή και αν δεν υπάρχει τότε εμφανίζει το μήνυμα *"Student has no courses"*. Αν όμως υπάρχει η πληροφορία για τα μαθήματα του, τότε περνάει στη μεταβλητή *courseList* το dictionary με τα courses του. Στη συνέχεια προσπελάυνει όλα τα στοιχεία αυτού του dictionary και τα values τους και ελέγχει άν το value του κάθε course, δηλαδή ο βαθμός του, είναι απο 5 και πάνω. Όποιο μάθημα πληρεί αυτή τη προϋπόθεση μπαίνει στη λίστα **passed**. Τέλος, μετα απο αυτή τη διαδικασία, ελέγχεται εάν η λίστα passed έχει καθόλου περιεχόμενα. Αν είναι άδεια τότε εμφανίζει το μήνυμα *"Sudent (name) has not passed any courses"*, ενω στην άλλη περίτπωση εμφανίζει τα μαθήματα που έχει περάσει ο μαθητής. 
````json
{
    "Information Systems": 5,
    "XML": 7,
    "DataBases": 9
}  
````

**Κώδικας**
````python
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
  ````
