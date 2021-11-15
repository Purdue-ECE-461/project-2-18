import firebase_admin  # import firebase-admin
from firebase_admin import credentials
from firebase_admin import firestore


def read(db):
    users_ref = db.collection(u'URLS')
    docs = users_ref.stream()

    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')


def post(db):
    doc_ref = db.collection(u'URLS').document(u'test')
    doc_ref.set({
        u'first': u'Ada',
        u'last': u'Lovelace',
        u'born': 1815
    })
    print("new url added")
    # store in documents, search through documents


def main():
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': "project-group18",
    })

    db = firestore.client()
    post(db)
    read(db)


if __name__ == "__main__":
    main()
