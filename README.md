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
