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
