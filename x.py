import re, sqlite3, os
from bottle import request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()
email = os.getenv("EMAIL_USERNAME")
COOKIE_SECRET = os.getenv("COOKIE_SECRET")
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
script_dir = os.path.dirname(os.path.abspath(__file__))

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
def initialize_db():
    try:
        sql_file_path = os.path.join(script_dir, "db.sql")
        with open(sql_file_path, 'r') as file:
            sql_script = file.read()

        connection = db()
        cursor = connection.cursor()
        cursor.executescript(sql_script)
        connection.commit()
    except Exception as ex:
        print(ex)
    finally:
        connection.close()

##############################
def send_password_reset_email(recipient_email, reset_password_key):
    try:
        message = MIMEMultipart()
        message["To"] = recipient_email
        message["From"] = 'michaelthodeschultz@gmail.com'
        message["Subject"] = 'Reset Password'

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reset Password</title>
        </head>
        <body>
            <h1>Reset Password</h1>
            <p>Click the button below to reset you're password:</p>
            <a href="http://127.0.0.1/reset-password?token={reset_password_key}">
                <button style="padding: 10px 20px; background-color: #007bff; color: #fff; border: none; cursor: pointer;">Reset Password</button>
            </a>
        </body>
        </html>
        """
        message.attach(MIMEText(html_content, 'html'))

        email = os.getenv("EMAIL_USERNAME")
        password = os.getenv("EMAIL_PASSWORD")

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(email, password)
        server.sendmail(email, recipient_email, message.as_string())
        server.quit()
    except Exception as ex:
        print(ex)
        return "error"    

##############################
def send_verification_email(recipient_email, user_verification_key):
    try:
        message = MIMEMultipart()
        message["To"] = recipient_email
        message["From"] = 'michaelthodeschultz@gmail.com'
        message["Subject"] = 'Account verification'

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Account Verification</title>
        </head>
        <body>
            <h1>Account Verification</h1>
            <p>Click the button below to verify your account:</p>
            <a href="http://127.0.0.1/verify-account?token={user_verification_key}">
                <button style="padding: 10px 20px; background-color: #007bff; color: #fff; border: none; cursor: pointer;">Verify Account</button>
            </a>
        </body>
        </html>
        """
        message.attach(MIMEText(html_content, "html"))

        email = os.getenv("EMAIL_USERNAME")
        password = os.getenv("EMAIL_PASSWORD")

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(email, password)
        server.sendmail(email, recipient_email, message.as_string())
        server.quit()
    except Exception as ex:
        print(ex)
        return "error"

##############################
def send_deletion_email(recipient_email):
    try:
        message = MIMEMultipart()
        message["To"] = recipient_email
        message["From"] = 'michaelthodeschultz@gmail.com'
        message["Subject"] = 'Account deleted'

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Account Deleted</title>
        </head>
        <body>
            <h1>Account Deleted</h1>
            <p>We write to confirm with you that you're account has been deleted, if this was not you, please write back and we will open you're account.</p>
        </body>
        </html>
        """
        message.attach(MIMEText(html_content, "html"))

        email = os.getenv("EMAIL_USERNAME")
        password = os.getenv("EMAIL_PASSWORD")
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(email, password)
        server.sendmail(email, recipient_email, message.as_string())
        server.quit()
    except Exception as ex:
        print(ex)
        return "error"
    
##############################
def send_blocked_status_email(recipient_email, blocked_status):
    try:
        subject = 'Account blocked' if blocked_status == 1 else 'Account unblocked'
        message = MIMEMultipart()
        message["To"] = recipient_email
        message["From"] = 'michaelthodeschultz@gmail.com'
        message["Subject"] = subject

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{subject}</title>
        </head>
        <body>
            <h1>{subject}</h1>
            <p>We write to inform you that you're account has been {"blocked" if blocked_status == 1 else "unblocked"}</p>
        </body>
        </html>
        """
        message.attach(MIMEText(html_content, "html"))

        email = os.getenv("EMAIL_USERNAME")
        password = os.getenv("EMAIL_PASSWORD")
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(email, password)
        server.sendmail(email, recipient_email, message.as_string())
        server.quit()
    except Exception as ex:
        print(ex)
        return "error"  
    
##############################
def send_blocked_house_status_email(recipient_email, blocked_status):
    try:
        subject = 'House unblocked' if blocked_status == 1 else 'House blocked'
        message = MIMEMultipart()
        message["To"] = recipient_email
        message["From"] = 'michaelthodeschultz@gmail.com'
        message["Subject"] = subject

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{subject}</title>
        </head>
        <body>
            <h1>{subject}</h1>
            <p>We write to inform you that your house has been {"blocked" if blocked_status == 1 else "unblocked"}</p>
        </body>
        </html>
        """
        message.attach(MIMEText(html_content, "html"))

        email = os.getenv("EMAIL_USERNAME")
        password = os.getenv("EMAIL_PASSWORD")
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(email, password)
        server.sendmail(email, recipient_email, message.as_string())
        server.quit()
    except Exception as ex:
        print(ex)
        return "error"  
    
##############################
#Validate
##############################
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PASSWORD_REGEX = ".{4,}"
USERNAME_REGEX = ".{4,}"
HOUSE_NAME_REGEX = r'^.{1,20}$'
HOUSE_DESCRIPTION_REGEX = r'^.{1,500}$'
PRICE_PER_NIGHT_REGEX = r'^\d+$'
STARS_REGEX = r'^[0-5](\.[0-9])?$'
LONGITUDE_REGEX = r'^-?((180(\.0{1,6})?)|((1[0-7]\d)|(\d{1,2}))(\.\d{1,6})?)$'
LATITUDE_REGEX = r'^-?((90(\.0{1,6})?)|(([1-8]?\d)|(\d{1,2}))(\.\d{1,6})?)$'

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

def validate_username():
    error = "Username too short"
    user_username = request.forms.get("user_username", "").strip()
    if not re.match(USERNAME_REGEX, user_username):
      raise Exception(error, 400)
    return user_username

def validate_user_role():
    error = "Invalid user role"
    user_role = request.forms.get("user_role", "").strip()
    if user_role not in ["customer", "partner", "admin"]:
        return error
    else:
        return user_role

def validate_house_name():
    error = "House name must be 20 characters or less"
    house_name = request.forms.get("house_name", "").strip()
    if not re.match(HOUSE_NAME_REGEX, house_name):
        raise Exception(error, 400)
    return house_name

def validate_house_description():
    error = "House description must be 300 characters or less"
    house_description = request.forms.get("house_description", "").strip()
    if not re.match(HOUSE_DESCRIPTION_REGEX, house_description):
        raise Exception(error, 400)
    return house_description

def validate_house_price_per_night():
    error = "Price per night must be a number"
    house_price_per_night = request.forms.get("house_price_per_night", "").strip()
    if not re.match(PRICE_PER_NIGHT_REGEX, house_price_per_night):
        raise Exception(error, 400)
    return house_price_per_night

def validate_house_stars():
    error = "Stars must be between 0 and 5"
    house_stars = request.forms.get("house_stars", "").strip()
    if not re.match(STARS_REGEX, house_stars):
        raise Exception(error, 400)
    return house_stars

def validate_house_images():
    error = "File is not an image or is too big"
    house_images = request.files.getall("image")
    valid_house_images = []

    for image in house_images:
        if image.file is not None and image.file and image.content_type.startswith('image/'):
            max_size_in_bytes = 5 * 1024 * 1024
            if image.content_length > max_size_in_bytes:
                raise Exception(error, 400)
            valid_house_images.append(image)
            
    return valid_house_images

def validate_longitude():
    error = "Longitude is out of range"
    house_longitude = request.forms.get("house_longitude", "").strip()
    if not re.match(LONGITUDE_REGEX, house_longitude):
        raise Exception(error, 400)
    return house_longitude

def validate_latitude():
    error = "Latitude is out of range"
    house_latidude = request.forms.get("house_latitude", "").strip()
    if not re.match(LATITUDE_REGEX, house_latidude):
        raise Exception(error, 400)    
    return house_latidude