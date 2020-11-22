import pyrebase
from datetime import datetime

c_t = datetime.now()
c_t_short = str(c_t.strftime("%c"))
c_m = str(c_t.strftime("%B"))
c_y = str(c_t.year)
c_d = str(c_t.strftime('%d'))

firebaseConfig = {
    'apiKey': "AIzaSyDsRPt73z0Or6cnOkk9rQ6c9QvXXnOZHdg",
    'authDomain': "guyaneseupdates.firebaseapp.com",
    'databaseURL': "https://guyaneseupdates.firebaseio.com",
    'projectId': "guyaneseupdates",
    'storageBucket': "guyaneseupdates.appspot.com",
    'messagingSenderId': "641260725294",
    'appId': "1:641260725294:web:41ae9723b7313771f32bbf",
    'admin': "true"
}


def login():
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    email = 'admin@mail.com'
    password = 'password1'
    user = auth.sign_in_with_email_and_password(email, password)
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