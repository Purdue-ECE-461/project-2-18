from google.cloud import firestore
import url.py

#store in documents, search through documents
def add_to_dict(url):
    db = firestore.Client(url);

    db.Collection(u'repositories').document(u'URLS').set(url)


def get_from_dict():
    #get info from dictionary

