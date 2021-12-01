const { initializeApp } = require('firebase-admin/app');
const {getFirestore, collection, setDoc, getDocs, doc, addDoc} = require('firebase/firestore/lite');
require("firebase-admin/firestore");
const fs = require('fs');
const {resolve} = require('path');

const firebaseConfig = {
    apiKey: "AIzaSyAmBHC0o_DLr6KcOvsjt15dXVZe5idDQB0",
    authDomain: "project-group18.firebaseapp.com",
   // databaseURL: "https://project-group18-default-rtdb.firebaseio.com",
    projectId: "project-group18",
    // storageBucket: "project-group18.appspot.com",
    // messagingSenderId: "944914465522",
    // appId: "1:944914465522:web:8ba83369a55d24eae3066b",
    // measurementId: "G-L9ZZVWGDKG"
  };
var admin = require("firebase-admin");

var serviceAccount = require("/Users/kshaunishsoni/461project2/project-2-18-1/firestore/project-group18-firebase-adminsdk-2llpi-72a9d84369.json");

admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: "https://project-group18-default-rtdb.firebaseio.com"
  });


const db = admin.firestore();

class addJsonFirestore {
    constructor() {
        
        this.db = db; //admin database access
        const [, , type, filepath] = process.argv;
        if(filepath != null){
            if(filepath.endsWith(".json")){ //checks if arg[2] is a .json file
                this.absolutePath = resolve(process.cwd(), filepath);
            }else{
                if(type == 'get' || type == 'delete'){ //if not and type == get, then input str.
                    this.str = filepath;
                    this.absolutePath = filepath;
                }
            }
            
        }
        this.type = type; //types are add, update, list
        //only add items from JSON file
        //check if inputs are correct
        if((this.absolutePath == null || this.absolutePath.length < 1) && (this.type != 'list' || this.type != 'get')){
            console.error('File path error, ', this.absolutePath);
            this.exit(1);
        }
        if(this.type == null){
            console.error('type error:', this.type);
            this.exit(1);
        }
        console.log("db:", this.db);
        console.log("absolute path:", this.absolutePath);
        console.log("type: ", this.type);
        console.log("str: ", this.str);
    }

    async populate(){
        let data = [];

        try{ //parse data in json file
            data = (JSON.parse(fs.readFileSync(this.absolutePath, {}), 'utf8'));
        } catch(e){
            console.error(e.message);
        }

        //console.log(data);
        if(data.length < 1){
            console.error('make sure JSON file has data');
            this.exit(1);
        }
        var i = 0;
        data.forEach(item => { //for each item in data, do command on item (add, update ,etc)
            try{
                if(this.type == 'add'){
                    this.add(item);
                }
                else if(this.type == 'update'){
                    //check if item exists first
                    if(this.get(item.repo) != 0){
                        this.update(item);
                    }
                }
            }catch(e){
                console.error(e.message);
            }
            if(i == data.length - 1){
                console.log('UPLOAD SUCCESS');
            }  
            i++;        
        });
    }

    add(item){
        var name = item.repo
        var str = name.toString();
        db.collection("repositories").doc(str).collection(type).doc(str).set(item)
        .then((docRef) => {
            console.log("Document written with ID: ", docRef.id);
        })
        .catch((error) => {
            console.error("Error adding document: ", error);
        });
    }

    delete(str){ //input repo name, delete repo from firestore.
        db.collection("repositories").delete(str)
        .then((docRef) => {
            console.log("Document deleted with ID: ", docRef.id);
        })
        .catch((error) => {
            console.error("Error deleting document: ", error);
        });
    }

    get(str){ //input repo name, will return repo information in the form of a JSON tree
        var docRef = db.collection("repositories").doc(str);
        docRef.get().then((doc) => {
            if (doc.exists) {
                console.log("Document data:", doc.data());
            } else {
                // doc.data() will be undefined in this case
                console.log("No such document!");
                return 0;
            }
        }).catch((error) => {
            console.log("Error getting document:", error);
        });
    }

    listall(){ //list all repositories in the database
        db.collection("repositories").get().then((querySnapshot) => {
            querySnapshot.forEach((doc) => {
                // doc.data() is never undefined for query doc snapshots
                console.log(doc.id, " => ", doc.data());
            });
        });
    }

    update(item){ //if item already exists in database, then rewrite database with new information.
        var name = item.repo
        var str = name.toString();
        db.collection("repositories").doc(str).update(item)
        .then((docRef) => {
            console.log("Document written with ID: ", docRef.id);
        })
        .catch((error) => {
            console.error("Error updating document: ", error);
        });
    }

    exit(code){
        return process.exit(code);
    }

    
}
//commands:
//node ./firestore/jsonFirestore.js (type: add, update, list) (json file, usually module.json)
const populateFirestore = new addJsonFirestore();
//populateFirestore.get("cloudinary_npm"); check for get
if(populateFirestore.type == 'add' || populateFirestore.type == 'update'){
    populateFirestore.populate(); //reads json file, adds each data entry into firestore as a document
}else if(populateFirestore.type == 'list'){
    populateFirestore.listall(); //lists all documents in database
}else if(populateFirestore.type == 'get'){
    populateFirestore.get(populateFirestore.str); //gets the information for the selected repository
}else if(populateFirestore.type == 'delete'){
    populateFirestore.delete(populateFirestore.str); //deletes repository and info from firestore
}


