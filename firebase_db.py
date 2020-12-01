import pyrebase
from datetime import datetime
from secrets import Secrets

c_t = datetime.now()
c_t_short = str(c_t.strftime("%c"))
c_m = str(c_t.strftime("%B"))
c_y = str(c_t.year)
c_d = str(c_t.strftime('%d'))

firebaseConfig = {
    'apiKey': Secrets.apiKey,
    'authDomain': Secrets.authDomain,
    'databaseURL': Secrets.databaseURL,
    'projectId': Secrets.projectId,
    'storageBucket': Secrets.storageBucket,
    'messagingSenderId': Secrets.messagingSenderId,
    'appId': Secrets.appId,
    'admin': Secrets.admin
}


def login():
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    user = auth.sign_in_with_email_and_password(Secrets.firebase_email, Secrets.firebase_password)
    user = auth.refresh(user['refreshToken'])
    return user['idToken']


def database_write(data):
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()
    result = db.child(str(f'{c_y} - {c_m}')).child(f'Day - {c_d}').child('articles').push(data, login())
    return result


def database_read():
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()
    titles = db.child(str(f'{c_y} - {c_m}')).child(f'Day - {c_d}').child('articles').get(login())
    return titles
