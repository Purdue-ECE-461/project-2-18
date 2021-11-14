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
        
        this.db = db;
        const [, , filepath, type, collectionName] = process.argv;
        this.absolutePath = resolve(process.cwd(), filepath);
        this.collection = collectionName;
        this.type = type;
        //only add items from JSON file
        //check if inputs are correct
        if(this.absolutePath == null || this.absolutePath.length < 1){
            console.error('File path error, ${this.absolutePath}');
            this.exit(1);
        }
        if(this.collection == null || this.collection.length < 1){
            console.error('collection namee error, ${this.collection}');
            this.exit(1);
        }
        if(this.type == null){
            console.error('type error:', this.type);
            this.exit(1);
        }
        console.log("db:", this.db);
        console.log("absolute path:", this.absolutePath);
        console.log("collection name:", this.collection);
        console.log("type: ", this.type);
    }

    async populate(){
        let data = [];
        try{
            data = (JSON.parse(fs.readFileSync(this.absolutePath, {}), 'utf8'));
        } catch(e){
            console.error(e.message);
        }

        if(data.length < 1){
            console.error('make sure JSON file has data');
        }
        var i = 0;
        data.forEach(item => {
            
            try{
                if(this.type == 'add'){
                    this.add(item);
                }else if(this.type == 'update'){
                    this.update(item);
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
        console.log(item)
        db.collection("repositories").add(item)
        .then((docRef) => {
            console.log("Document written with ID: ", docRef.id);
        })
        .catch((error) => {
            console.error("Error adding document: ", error);
        });
    }

    delete(item){
        db.collection("repositories").delete(item)
        .then((docRef) => {
            console.log("Document written with ID: ", docRef.id);
        })
        .catch((error) => {
            console.error("Error adding document: ", error);
        });
    }

    get(item){
        var docRef = db.collection("repositories").doc(item);
        docRef.get().then((doc) => {
            if (doc.exists) {
                console.log("Document data:", doc.data());
            } else {
                // doc.data() will be undefined in this case
                console.log("No such document!");
            }
        }).catch((error) => {
            console.log("Error getting document:", error);
        });
    }

    listall(){
        db.collection("repositories").get().then((querySnapshot) => {
            querySnapshot.forEach((doc) => {
                // doc.data() is never undefined for query doc snapshots
                console.log(doc.id, " => ", doc.data());
            });
        });
    }

    update(item){
        console.log('updating item ${item.id}');
        return this.db.collection(this.collection).update(Object.assign({}, item))
        .then(() => true)
        .catch((e) => console.error(e.message));
    }

    exit(code){
        return process.exit(code);
    }
}

const populateFirestore = new addJsonFirestore();
populateFirestore.populate();
//populateFirestore.listall();
