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

var serviceAccount = require("/Users/kshaunishsoni/461project2/project-2-18-1/p18_website/p18website/static/p18_website/project-group18-firebase-adminsdk-2llpi-72a9d84369.json");

admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: "https://project-group18-default-rtdb.firebaseio.com"
  });


const db = admin.firestore();

class addJsonFirestore {
    constructor() {
        
        this.db = db; //admin database access
        // if(filepath != null){
        //     if(filepath.endsWith(".json")){ //checks if arg[2] is a .json file
        //         this.absolutePath = resolve(process.cwd(), filepath);
        //     }else{
        //         if(type == 'get' || type == 'delete'){ //if not and type == get, then input str.
        //             this.str = filepath;
        //             this.absolutePath = filepath;
        //         }
        //     }
            
        // }
        // this.filetype = filetype
        // this.type = type; //types are add, update, list
        //only add items from JSON file
        //check if inputs are correct
        // if((this.absolutePath == null || this.absolutePath.length < 1) && (this.type != 'list' || this.type != 'get')){
        //     console.error('File path error, ', this.absolutePath);
        //     this.exit(1);
        // }
        // if(this.type == null){
        //     console.error('type error:', this.type);
        //     this.exit(1);
        // }
        console.log("db:", this.db);
        // console.log("absolute path:", this.absolutePath);
        // console.log("type: ", this.type);
        // console.log("str: ", this.str);
    }
    check_filetype(data, filetype){
        if(filetype == null){
            return false;
        }
        if(filetype == 'PackageRetrieve' || filetype == 'PackageCreate'){
            if(data.metadata == null){
                return false;
            }
            if(data.data == null){
                return false;
            }
        }else if(filetype == 'PackageRate'){
            if(data.netscore == null){
                return false;
            }
            if(data.RampUp == null){
                return false;
            }
            if(data.Correctness == null){
                return false;
            }
            if(data.BusFactor == null){
                return false;
            }
            if(data.LicenseScore == null){
                return false;
            }
            if(data.ResponsiveMaintainer == null){
                return false;
            }
            if(data.GoodPinningPractice == null){
                return false;
            }
        }else if(filetype == 'CreateAuthToken'){
            if(data.User == null){
                return false;
            }
            if(data.Secret == null){
                return false;
            }
        }
        return true;
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
                this.check_filetype();
                if(this.type == 'POST'){
                    if(this.filetype == 'PackageCreate'){
                        var str = item[0].name;
                        var version = item[0].version;
                        this.add_data(item, str, version);
                    }
                    
                }
                else if(this.type == 'PUSH'){
                    //check if item exists first
                    if(this.get(item.repo) != false){
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

    add_data(item, str, version, filetype){
        
        db.collection("repositories").doc(str).collection(version).doc(filetype).set(item)
        .then((docRef) => {
            console.log("Document written with ID: ", docRef.id);
        })
        .catch((error) => {
            console.error("Error adding document: ", error);
        });
    }

    add_metadata(item,str){
        db.collection("repositories").doc(str).set(item)
        .then((docRef) => {
            console.log("Document written with ID: ", docRef.id);
        })
        .catch((error) => {
            console.error("Error adding document: ", error);
        });
    }

    delete(str, version){ //input repo name, delete repo from firestore.
        db.collection("repositories").doc(str).collection(version).delete(this.filetype)
        .then((docRef) => {
            console.log("Document deleted with ID: ", docRef.id);
        })
        .catch((error) => {
            console.error("Error deleting document: ", error);
        });
    }

    get(str, version){ //input repo name, will return repo information in the form of a JSON tree
        var docRef = db.collection("repositories").doc(str).collection(version).doc(this.filetype);
        docRef.get().then((doc) => {
            if (doc.exists) {
                console.log("Document data:", doc.data());
                return doc.data();
            } else {
                // doc.data() will be undefined in this case
                console.log("No such document!");
                return null; //TODO: ERROR 400: No such package
            }
        }).catch((error) => {
            console.log("Error getting document:", error);
        });
        return null;
    }

    get_name(name){
        var docRef = db.collection("repositories").doc(name);
        docRef.get().then((doc) => {
            if (doc.exists) {
                console.log("Document data:", doc.data());
                return doc.data();
            } else {
                // doc.data() will be undefined in this case
                console.log("No such document!");
                return null; //TODO: ERROR 400: No such package
            }
        }).catch((error) => {
            console.log("Error getting document:", error);
        });
        return null;
    }

    listall(page_number){ //list all repositories in the database
        const repos = new Array();
        db.collection("repositories").get().then((querySnapshot) => {
            querySnapshot.forEach((doc) => {
                //console.log(doc.data());
                // doc.data() is never undefined for query doc snapshots
                repos.push(doc.data());
               // console.log(repos);
            });
            //console.log(repos);
            repos.slice((page_number-1)*10, page_number*10);
            var e = "<br/>"; 
            for(var i =0; i < repos.length; i++){
                console.log(repos[i].repo);
                document.getElementById("Result").innerHTML = repos[i].repo;
            }
            // repos.forEach(item => {
            //     e += item + "<br/>";
            //     console.log(item);
            //     document.getElementsByClassName("repo").innerHTML = item;;
            // })
        });
    }

    update(item, version){ //if item already exists in database, then rewrite database with new information.
        var name = item.repo
        var str = name.toString();
        db.collection("repositories").doc(str).collection(version).doc(this.filetype).update(item)
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
function initFirestore(){
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
}

function getListpaginated(page_number){
    //initFirestore();
    const populateFirestore = new addJsonFirestore();
    const repos = populateFirestore.listall(page_number); 
    console.log(repos);
    
   // var e = "<br/>"; 
    // repos.forEach(item => {
    //     e += item + "<br/>";
    //     console.log(item);
    //     document.getElementsByClassName("repo").innerHTML = item;;
    // })
    
    //document.getElementById("Result").innerHTML = e;
   
}


//commands:
//node ./firestore/jsonFirestore.js (type: POST, PUSH, list, GET, DELETE) (filetype) (json file, usually module.json)
const populateFirestore = new addJsonFirestore();
getListpaginated(1);
//populateFirestore.get("cloudinary_npm"); check for get
// if(populateFirestore.type == 'POST' || populateFirestore.type == 'PUSH'){
//     populateFirestore.populate(); //reads json file, adds each data entry into firestore as a document
// }else if(populateFirestore.type == 'list'){
//     populateFirestore.listall(); //lists all documents in database
// }else if(populateFirestore.type == 'GET'){
//     populateFirestore.get(populateFirestore.str); //gets the information for the selected repository
// }else if(populateFirestore.type == 'DELETE'){
//     populateFirestore.delete(populateFirestore.str); //deletes repository and info from firestore
// }


