from bottle import default_app, get, post, run, template, static_file, response, request
import git
import x, bcrypt

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

@get("/favicon.ico")
def _():
    return static_file("favicon.ico", ".")

##############################
@get("/")
def _():
    return "X"

##############################
@get("/login")
def _():
    return template("login", title="Login")

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

@get("/users")
def _():
    try:
        db = x.db()
        q = db.execute("SELECT * FROM users")
        users = q.fetchall()
        print(users)
        return "users"
    except Exception as ex:
        print(ex)
    finally:
        db.close()

##############################
#POST
##############################
@post("/login")
def _():
    try:
        user_email = x.validate_email()
        user_password = x.validate_password()

        db = x.db()
        q = db.execute("SELECT * FROM users WHERE user_email = (?) LIMIT 1", (user_email,))
        user = q.fetchone()

        if user:
            stored_hashed_password = user['user_password'].encode('utf-8')
            if bcrypt.checkpw(user_password.encode('utf-8'), stored_hashed_password):
                user.pop("user_password")
                try:
                    import production
                    is_cookie_https = True
                except:
                    is_cookie_https = False        
                response.set_cookie("user", user, secret=x.COOKIE_SECRET, httponly=True, secure=is_cookie_https)
                return user
            else: 
                response.status = 401
                #This is incorrect password, but the user should not know which one is incorrect
                return "Incorrect email or password"
        else:
            response.status = 404
            return "User not found"
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