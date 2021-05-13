# Πρώτη Υποχρωτική Εργασια 
## Πληροφορικά Συστήματα, Τμήμα Ψηφιακών Συστημάτων
### Όνομα : Νομική Παργινού
###  AM : E18130

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
