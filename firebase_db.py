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
    db.child().child(str(f'{c_y} - {c_m}')).child(f'Date - {c_t_short}').child('articles').push(data, login())


def database_read():
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()
    titles = db.child().child(str(f'{c_y} - {c_m}')).child(f'Date - {c_t_short}').child('articles').get(login())
    return titles


data = {'date': c_t_short, 'sd': short_d, 'title': title, 'agency': agency_name}
# data2 = {'title': title2, 'sd': short_d, 'date': c_t_short, 'agency': 'Village Voice'}

# for i in range(1, 240):
# db.child().child(str(f'{c_y} - {c_m}')).child(f'date - {c_d}').child('articles').set(data2)
# db.child().child(str(f'{c_y} - {c_m}')).child(f'Date - {c_t_short}').child('articles').push(data, login())
# print(result)
# db.child().child(str(f'{c_y} - {c_m}')).child(f'date - {c_d}').child('articles').push(data2)
# db.child().child(str(f'{c_y} - {c_m}')).child('articles').push(data) #good
# db.child().child(str(f'{c_y} - {c_m}')).child('articles').push(data2)
# db.child("users").push(data, user['idToken'])



# titles = db.child().child(str(f'{c_y} - {c_m}')).child(f'Date - {c_t_short}').child('articles').get(user['idToken'])
# for i in titles.each():
#     print(i.val()['title'])
