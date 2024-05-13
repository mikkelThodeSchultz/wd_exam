from bottle import default_app, get, post, run, template, static_file, response, request
from json import dumps
import git, x, bcrypt, time, uuid


@post('/1fa5b451-8928-40e8-9324-f707ebfcb485')
def git_update():
    repo = git.Repo('./wd_exam')
    origin = repo.remotes.origin
    repo.create_head('main', origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
    origin.pull()
    return ""

##############################
#GET
##############################
@get("/css/<filename:path>")
def _(filename):
    return static_file(filename, root="./css")

@get("/js/<filename:path>")
def _(filename):
    return static_file(filename, root="./js")

@get("/images/<filename:path>")
def _(filename):
    return static_file(filename, root="./images")

@get("/app.js")
def _():
    return static_file("app.js", ".")

@get("/favicon.ico")
def _():
    return static_file("favicon.ico", ".")

##############################
@get("/")
def _():
    return template("index", title="Company", is_index_page=True)

##############################
@get("/profile")
def _():
    return template("profile", title="Profile", is_index_page=False)

##############################
@get("/house")
def _():
    try:
        db = x.db()
        q = db.execute("SELECT * FROM houses")
        houses = q.fetchall()
        houses_with_Images = []
        for house in houses:
            house_dict = dict(house)
            q = db.execute("SELECT image_url FROM house_images WHERE house_pk = ?", (house['house_pk'],))
            images = q.fetchall()
            house_images = [image["image_url"] for image in images]
            house_dict["images"] = house_images
            houses_with_Images.append(house_dict)
        db.close()
        return dumps(houses_with_Images)
    except Exception as ex:
        print(ex)
        if len(ex.args) > 1 and ex.args[1]:
            response.status=ex.args[1]
        else:
            response.status = 500
        return ex.args[0]
    finally:
        if "db" in locals(): db.close()

##############################
@get("/mapbox_token")
def _():
    return x.MAPBOX_TOKEN
##############################
@get("/login")
def _():
    return template("login", title="Login" , is_index_page=False)

##############################
@get("/signup")
def _():
    return template("signup", title="Signup" , is_index_page=False)

##############################
@get("/verify-account")
def _():
    return template("verify-account", title="Verify account" , is_index_page=False)

##############################
@get("/reset-password")
def _():
    return template("reset-password", title="Reset password" , is_index_page=False)

##############################
@get("/reset-password-form")
def _():
    return template("reset-password-form", title="Reset password" , is_index_page=False)

##############################
@get("/logout")
def _():
    response.delete_cookie("user")
    response.status = 303
    response.set_header('Location', '/login')
    return

##############################
@get("/test_db_connection")
def _():
    try:
        db = x.db()
        db.execute("SELECT 1")
        return {"success": True, "message": "Database connection successful"}
    except Exception as e:
        response.status = 500
        return {"success": False, "error": str(e)}
    finally:
        db.close()

##############################
@get("/initialize_database")
def _():
    x.initialize_db()
    return "Database initialized"

##############################
@get("/user")
def _():
    try:
        db = x.db()
        #Since the hashed password is stored as bytes, and for security reasons, 
        #i am excluding it from this fetch so the dict_factory method still works
        q = db.execute("SELECT user_pk, user_username, user_email, user_role, user_created_at, user_updated_at, user_deleted_at, user_is_verified, user_verification_key FROM users")
        users = q.fetchall()
        return dumps(users)
    except Exception as ex:
        print(ex)
    finally:
        if "db" in locals(): db.close()

##############################
@get("/cookie")
def get_cookie():
    user_cookie = request.get_cookie('user', secret=x.COOKIE_SECRET)
    if user_cookie:
        response.status = 200
        return user_cookie 
    else: 
        response.status = 404
        return "No cookies found"
    
            
##############################
@get("/password_reset")
def _():
    try:
        db = x.db()
        q = db.execute("SELECT * FROM password_reset")
        password_reset = q.fetchall()
        return dumps(password_reset)
    except Exception as ex:
        print(ex)
    finally:
        if "db" in locals(): db.close()

##############################
#POST
##############################
@post("/login")
def _():
    try:
        user_email = x.validate_email()
        user_password = x.validate_password()
        db = x.db()
        q = db.execute("SELECT * FROM users WHERE user_email = ? AND user_deleted_at = 0 AND user_is_verified = 1 LIMIT 1", (user_email,))
        user = q.fetchone()

        if user:
            stored_hashed_password = user['user_password']
            if bcrypt.checkpw(user_password.encode('utf-8'), stored_hashed_password):
                user.pop("user_password")
                try:
                    import production
                    is_cookie_https = True
                except:
                    is_cookie_https = False        
                response.set_cookie("user", user, secret=x.COOKIE_SECRET, httponly=True, secure=is_cookie_https)
                return user
        response.status = 404
        return "User not found or incorrect email/password"
    except Exception as ex:
        print(ex)
        if len(ex.args) > 1 and ex.args[1]:
            response.status=ex.args[1]
        else:
            response.status = 500
        return ex.args[0]
    finally:
        if "db" in locals(): db.close()

##############################
@post("/signup")
def _():
    try:
        user_email = x.validate_email()
        db = x.db()
        email_exists = db.execute("SELECT 1 FROM users WHERE user_email = ?", (user_email,)).fetchone()
        if email_exists:
            response.status = 409
            return "Email address is already in use"
        
        user_password = x.validate_password()
        user_username = x.validate_username()
        user_role = x.validate_user_role()
        hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())
        user_pk = str(uuid.uuid4())
        current_unix_time = int(time.time())
        user_verification_key = str(uuid.uuid4())
    
        db.execute("INSERT INTO users (user_pk, user_username, user_email, user_password, user_role, user_created_at, user_updated_at, user_deleted_at, user_is_verified, user_verification_key) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (user_pk, user_username, user_email, hashed_password, user_role, current_unix_time, 0, 0, 0, user_verification_key))
        db.commit()

        x.send_verification_email(user_email, user_verification_key)
    
        response.status = 201
        return "User created"
    except Exception as ex:
        print(ex)
        if len(ex.args) > 1 and ex.args[1]:
            response.status=ex.args[1]
        else:
            response.status = 500
        return ex.args[0]
    finally:
        if "db" in locals(): db.close()

##############################
@post("/verify-account")
def _():
    try:
        token = request.query.token
        db = x.db()
        q = db.execute("UPDATE users SET user_is_verified = 1 WHERE user_verification_key = ?", (token,))
        db.commit()
        if q.rowcount == 0:
            response.status = 404
            return "No user with that verification key"
        response.status = 200
        return "User has been verified"
    except Exception as ex:
        print(ex)
        if len(ex.args) > 1 and ex.args[1]:
            response.status=ex.args[1]
        else:
            response.status = 500
        return ex.args[0]
    finally:
        if "db" in locals(): db.close()

##############################
@post("/reset-password")
def _():
    try:
        user_email = x.validate_email()
        db = x.db()
        q = db.execute("SELECT user_pk FROM users WHERE user_email = (?)", (user_email,))
        result = q.fetchone()
        if result:
            user_pk = result["user_pk"]
            reset_token = str(uuid.uuid4())
            db.execute("INSERT INTO password_reset (user_pk, reset_token) VALUES (?, ?)", (user_pk, reset_token))
            db.commit()
            x.send_password_reset_email(user_email, reset_token)
            response.status = 200
            return "Password reset token has been created"
        else:
            response.status = 404
            return "No user with the given email"
    except Exception as ex:
        print(ex)
        if len(ex.args) > 1 and ex.args[1]:
            response.status=ex.args[1]
        else:
            response.status = 500
        return ex.args[0]
    finally:
        if "db" in locals(): db.close()

##############################
@post("/verify-reset-password")
def _():
    try:
        reset_token = request.query.token
        user_password = x.validate_password()
        hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())
        db = x.db()
        q = db.execute("SELECT user_pk FROM password_reset WHERE reset_token = ?", (reset_token,))
        user_pk = q.fetchone()
        if user_pk:
            db.execute("UPDATE users SET user_password = ? WHERE user_pk = ?", (hashed_password, user_pk["user_pk"]))
            db.commit()
            db.execute("DELETE FROM password_reset WHERE reset_token = ?", (reset_token,))
            db.commit()
            response.status = 200
            return "User have been updated"
        else:
            response.status = 404
            return "No user matching the given code"
    except Exception as ex:
        print(ex)
        if len(ex.args) > 1 and ex.args[1]:
            response.status=ex.args[1]
        else:
            response.status = 500
        return ex.args[0]
    finally:
        if "db" in locals(): db.close()

##############################
try:
    import production
    application = default_app()
except Exception as ex:
    print("Running local server")
    run(host="127.0.0.1", port=80, debug=True, reloader=True)