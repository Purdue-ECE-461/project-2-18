const firebase = require("firebase");
require("firebase/firestore");
const fs = require('fs');
const {resolve} = require('path');

firebase.initializeApp({
    apiKey: "AIzaSyAmBHC0o_DLr6KcOvsjt15dXVZe5idDQB0",
    authDomain: "project-group18.firebaseapp.com",
    projectId: "project-group18",
});


class addJsonFirestore {
    constructor() {
        this.db = firebase.firestore();
        const [, , filepath, collectionName] = process.argv;
        this.absolutePath = resolve(process.cwd(), filepath);
        this.collection = collectionName;
        //only add items from JSON file
        //check if inputs are correct
        if(this.absolutePath == NULL || this.absolutePath.length < 1){
            console.error('File path error, ${this.absolutePath}');
            this.exit(1);
        }
        if(this.collection == NULL || this.collection.length < 1){
            console.error('collection namee error, ${this.collection}');
            this.exit(1);
        }

    }

    async populate(){
        let data = [];
        try{
            data = JSON.parse(fs.readFileSync(this.absolutePath, {}), 'utf8');
        } catch(e){
            console.error(e.message);
        }

        if(data.length < 1){
            console.error('make sure JSON file has data');
        }
        var i = 0;
        for(var item in data){
            console.log(item)
            try{
                this.add(item);
            }catch(e){
                console.error(e.message);
            }
            if(i == data.length - 1){
                console.log('UPLOAD SUCCESS');
                this.exit(0);
            }  
            i++;          
        }

    }

    add(item){
        console.log('adding item${item.id}');
        return this.db.collection(this.collection).add(Object.assign({}, item))
        .then(() => true)
        .catch((e) => console.error(e.message));

    }

    exit(code){
        return process.exit(code);
    }
}