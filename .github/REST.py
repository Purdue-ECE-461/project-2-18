import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import url

def read(db):
    users_ref = db.collection(u'users')
    docs = users_ref.stream()

    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')

def post(Url: url, db):
    doc_ref = db.collection(u'URLS').document(Url.url)
    doc_ref.set({
        u'first': u'Ada',
        u'last': u'Lovelace',
        u'born': 1815
    })
#store in documents, search through documents

def main():
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': "project-group18",
    })

    db = firestore.client()
    


if __name__ == "__main__":
    main()