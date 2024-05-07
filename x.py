import re, sqlite3, os
from bottle import request

COOKIE_SECRET = "41ebeca46f3b-4d77-a8e2-554659075C6319a2fbfb-9a2D-4fb6-Afcad32abb26a5e0"


##############################
def dict_factory(cursor, row):
    col_names = [col[0] for col in cursor.description]
    return {key: value for key, value in zip(col_names, row)}
    
##############################
def db():
    db = sqlite3.connect(os.getcwd()+"/db.db")  
    db.row_factory = dict_factory
    return db

##############################
#Validate
##############################
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PASSWORD_REGEX = ".{4,}"

def validate_email():
    error = "Invalid email"
    user_email = request.forms.get("user_email", "").strip()
    if not re.match(EMAIL_REGEX, user_email): 
        raise Exception(error, 400)
    return user_email
    
def validate_password():
   error = "Password too short"
   user_password = request.forms.get("user_password", "").strip()
   if not re.match(PASSWORD_REGEX, user_password):
      raise Exception(error, 400)
   return user_password