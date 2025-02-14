from bottle import default_app, get, post, run, template, static_file, response, request, put, delete
from json import dumps
from arango import ArangoClient
import git, x, bcrypt, time, uuid, os
import pymysql


#@post('/1fa5b451-8928-40e8-9324-f707ebfcb485')
#def git_update():
#    repo = git.Repo('./wd_exam')
#    origin = repo.remotes.origin
#    repo.create_head('main', origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
#    origin.pull()
#    return ""

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
    cookie = get_cookie()
    if cookie == "No cookies found":
        response.status = 303
        response.set_header('Location', '/login')
    return template("profile", title="Profile", is_index_page=False)

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
@get("/admin")
def _():
    return template("admin", title="Admin", is_index_page=False)

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
        cursor, connection = x.db()  # Get cursor and connection
        cursor.execute("SELECT 1")  # Test query
        return {"success": True, "message": "Database connection successful"}
    except Exception as e:
        response.status = 500
        return {"success": False, "error": str(e)}
    finally:
        cursor.close()  # Close cursor
        connection.close()  # Close connection

##############################
@get("/initialize_database")
def _():
    x.initialize_db()
    return "Database initialized"

##############################
@get("/user")
def _():
    try:
        cursor, connection = x.db()
        #Since the hashed password is stored as bytes, and for security reasons,
        #i am excluding it from this fetch so the dict_factory method still works
        cursor.execute("SELECT user_pk, user_username, user_email, user_role, user_created_at, user_updated_at, user_deleted_at, user_is_verified, user_is_blocked, user_verification_key FROM users")
        users = cursor.fetchall()
        return dumps(users)
    except Exception as ex:
        print(ex)
    finally:
        cursor.close()
        connection.close()

##############################
@get("/house")
def _():
    try:
        user_pk = request.query.get('user_pk')

        cursor, connection = x.db()
        if user_pk:
            cursor.execute("SELECT * FROM houses WHERE user_pk = %s", (user_pk,))
        else:
            cursor.execute("SELECT * FROM houses")
        houses = cursor.fetchall()
        houses_with_Images = []
        column_names = [desc[0] for desc in cursor.description]
        for house in houses:
            house_dict = dict(zip(column_names, house))
            cursor.execute("SELECT image_url FROM house_images WHERE house_pk = %s", (house_dict['house_pk'],))
            images = cursor.fetchall()
            house_images = [image[1] for image in images]
            house_dict["images"] = house_images
            houses_with_Images.append(house_dict)

        return dumps(houses_with_Images)
    except Exception as ex:
        print(ex)
        if len(ex.args) > 1 and ex.args[1]:
            response.status=ex.args[1]
        else:
            response.status = 500
        return ex.args[0]
    finally:
        cursor.close()
        connection.close()

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
        cursor, connection = x.db()  # Get cursor and connection
        cursor.execute("SELECT * FROM password_reset")  # Execute the query
        password_reset = cursor.fetchall()  # Fetch all results
        return dumps(password_reset)  # Return results as JSON
    except Exception as ex:
        print(ex)  # Log the exception
        response.status = 500  # Set response status to 500 for errors
        return {"success": False, "error": str(ex)}  # Return error message
    finally:
        cursor.close()  # Close cursor
        connection.close()  # Close connection

##############################
#POST
##############################
@post("/login")
def _():
    try:
        user_email = x.validate_email()  # Validate and get user email
        user_password = x.validate_password()  # Validate and get user password
        cursor, connection = x.db()  # Get cursor and connection

        # Use %s as the placeholder for MySQL parameters
        query = """
            SELECT * FROM users
            WHERE user_email = %s
              AND user_deleted_at = 0
              AND user_is_verified = 1
              AND user_is_blocked = 0
            LIMIT 1
        """
        cursor.execute(query, (user_email,))  # Execute the query with parameters
        user = cursor.fetchone()  # Fetch the user

        if user:
            stored_hashed_password = user['user_password']  # Get stored password
            # Verify the password
            if bcrypt.checkpw(user_password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                user.pop("user_password")  # Remove the password from user data
                try:
                    import production
                    is_cookie_https = True
                except ImportError:
                    is_cookie_https = False

                # Set the cookie
                response.set_cookie("user", user, secret=x.COOKIE_SECRET, httponly=True, secure=is_cookie_https)
                response.status = 200  # Successful login
                return user

        response.status = 404  # User not found
        return "User not found or incorrect email/password"

    except Exception as ex:
        print(ex)  # Log the exception
        if len(ex.args) > 1 and ex.args[1]:
            response.status = ex.args[1]  # Set status from exception if available
        else:
            response.status = 500  # Internal server error
        return ex.args[0]  # Return error message

    finally:
        cursor.close()  # Close cursor
        connection.close()  # Close connection


##############################

@post("/signup")
def _():
    cursor, connection = None, None
    try:
        user_email = x.validate_email()  # Validate and get user email
        cursor, connection = x.db()  # Get cursor and connection

        # Check if the email already exists
        email_exists_query = "SELECT 1 FROM users WHERE user_email = %s"
        cursor.execute(email_exists_query, (user_email,))
        email_exists = cursor.fetchone()  # Fetch result

        if email_exists:
            response.status = 409  # Conflict status
            return "Email address is already in use"

        user_password = x.validate_password()  # Validate and get password
        user_username = x.validate_username()  # Validate and get username
        user_role = x.validate_user_role()  # Validate and get user role

        hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())  # Hash password
        user_pk = str(uuid.uuid4())  # Generate user primary key
        current_unix_time = int(time.time())  # Get current time
        user_verification_key = str(uuid.uuid4())  # Generate verification key

        # Insert new user into the database
        insert_query = """
            INSERT INTO users (user_pk, user_username, user_email, user_password, user_role, user_created_at,
                               user_updated_at, user_deleted_at, user_is_verified, user_is_blocked, user_verification_key)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (user_pk, user_username, user_email, hashed_password, user_role, current_unix_time, 0, 0, 0, 0, user_verification_key))
        connection.commit()  # Commit the transaction

        # Send verification email
        x.send_verification_email(user_email, user_verification_key)

        response.status = 201  # Created status
        return "User created"
    except Exception as ex:
        print("Error during signup:", ex)  # Log the exception
        if len(ex.args) > 1 and ex.args[1]:
            response.status = ex.args[1]  # Set status from exception if available
        else:
            response.status = 500  # Internal server error
        return str(ex)  # Return error message
    finally:
        if cursor:  # Check if cursor was created
            cursor.close()  # Close cursor
        if connection:  # Check if connection was created
            connection.close()  # Close connection


##############################
@post("/house")
def _():
    try:
        user_pk = request.query.get("user_pk")
        house_pk = str(uuid.uuid4())
        current_unix_time = int(time.time())

        house_name = x.validate_house_name()
        house_description = x.validate_house_description()
        house_price_per_night = x.validate_house_price_per_night()
        house_stars = x.validate_house_stars()
        house_longitude = x.validate_longitude()
        house_latitude = x.validate_latitude()
        house_images = x.validate_house_images()

        images_to_save = []
        relative_image_paths = []

        for upload in house_images:
            filename = upload.filename
            relative_path = os.path.join("images", filename)
            try:
                import production
                full_path = os.path.join("/home/mikkelThodeSchultz/wd_exam", relative_path)
            except Exception as ex:
                full_path = os.path.join(relative_path)

            upload.save(full_path)
            images_to_save.append(full_path)
            relative_image_paths.append(relative_path)

        db = x.db()
        db.execute("INSERT INTO houses (house_pk, house_name, house_description, house_price_per_night, house_latitude, house_longitude, house_stars, house_created_at, house_updated_at, house_is_blocked, user_pk) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (house_pk, house_name, house_description, house_price_per_night, house_latitude, house_longitude, house_stars, current_unix_time, 0, 0, user_pk))

        for url in relative_image_paths:
            db.execute("INSERT INTO house_images (house_pk, image_url) VALUES (?,?)", (house_pk,url))

        response.status = 200
        db.commit()
        return "House has been created"
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
#PUT
##############################
@put("/user")
def _():
    try:
        current_time = int(time.time())

        #if user_pk is in the query, this is a block/unblock call
        user_pk = request.query.get("user_pk")
        if user_pk:
            db = x.db()
            db.execute("UPDATE users SET user_is_blocked = CASE WHEN user_is_blocked = 0 THEN 1 ELSE 0 END, user_updated_at = ? WHERE user_pk = ?",
                       (current_time, user_pk))
            db.commit()
            updated_user = db.execute("SELECT user_is_blocked, user_email FROM users WHERE user_pk = ?", (user_pk,)).fetchone()
            x.send_blocked_status_email(updated_user["user_email"], updated_user["user_is_blocked"])

        #if user_pk is not in the query, this is an update user call
        else:
            user_username = x.validate_username()
            user_email = x.validate_email()
            user = get_cookie()
            if user == "No cookies found":
                response.status = 404
                return user
            db = x.db()
            db.execute("UPDATE users SET user_username = ?, user_email = ?, user_updated_at = ? WHERE user_email = ?",
                    (user_username, user_email, current_time, user["user_email"]))
            db.commit()
            updated_user = db.execute("SELECT * FROM users WHERE user_email = ?", (user_email,)).fetchone()
            updated_user.pop("user_password")
            try:
                import production
                is_cookie_https = True
            except:
                is_cookie_https = False

            response.set_cookie("user", updated_user, secret=x.COOKIE_SECRET, httponly=True, secure=is_cookie_https)

        response.status = 200
        return "User have been updated"
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
@put("/house")
def _():
    try:
        is_house_block_request = request.query.get("house_block")
        house_pk = request.query.get('house_pk')

        if is_house_block_request:
            current_unix_time = int(time.time())
            db = x.db()
            db.execute("UPDATE houses SET house_is_blocked = CASE WHEN house_is_blocked = 0 THEN 1 ELSE 0 END, house_updated_at = ? WHERE house_pk = ?",
                       (current_unix_time, house_pk))
            q = db.execute("SELECT house_is_blocked FROM houses WHERE house_pk = ?",
                           (house_pk,))
            house_blocked_status = q.fetchone()
            q = db.execute("SELECT user_pk FROM houses WHERE house_pk = ?",
                           (house_pk,))
            partner_pk = q.fetchone()
            q = db.execute("SELECT user_email FROM users WHERE user_pk = ?",
                           (partner_pk["user_pk"],))
            partner_email = q.fetchone()
            x.send_blocked_house_status_email(partner_email["user_email"], house_blocked_status["house_is_blocked"])
            db.commit()

        else:
            house_name = x.validate_house_name()
            house_description = x.validate_house_description()
            house_price_per_night = x.validate_house_price_per_night()
            house_stars = x.validate_house_stars()
            house_images = x.validate_house_images()

            images_to_save = []
            for upload in house_images:
                filename = upload.filename
                filepath = os.path.join("images", filename)
                upload.save(filepath)
                images_to_save.append(filepath)

            db = x.db()
            db.execute("UPDATE houses SET house_name = ?, house_description = ?, house_price_per_night = ?, house_stars = ? WHERE house_pk = ?",
                    (house_name, house_description, house_price_per_night, house_stars, house_pk))

            for url in images_to_save:
                db.execute("INSERT INTO house_images (house_pk, image_url) VALUES (?,?)", (house_pk,url))

            db.commit()

        response.status = 200
        return "House has been updated"
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
#DELETE
##############################
@delete("/user")
def _():
    try:
        user_password = x.validate_password()
        db = x.db()
        user = get_cookie()
        if user == "No cookies found":
            response.status = 404
            return user

        db_user = db.execute("SELECT * FROM users WHERE user_email = ?", (user["user_email"],)).fetchone()

        stored_hashed_password = db_user['user_password']
        if bcrypt.checkpw(user_password.encode('utf-8'), stored_hashed_password):
            current_time = int(time.time())
            db.execute("UPDATE users SET user_deleted_at = ? WHERE user_pk = ?", (current_time, user["user_pk"]))
            db.commit()
            x.send_deletion_email(user["user_email"])
            response.status = 200
            response.delete_cookie("user")
            return "User have been deleted"
        else:
            response.status = 404
            return "Wrong password"

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
@delete("/image")
def _():
    try:
        house_pk = request.query.get("house_pk")
        url = request.query.get("imageUrl")
        db = x.db()
        db.execute("DELETE FROM house_images WHERE house_pk = ? AND image_url = ?", (house_pk, url))
        db.commit()
        response.status = 200
        return "Image have been deleted"
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
@delete("/house")
def _():
    try:
        house_pk = request.query.get("house_pk")
        db = x.db()
        db.execute("DELETE FROM houses WHERE house_pk = ?", (house_pk,))
        db.execute("DELETE FROM house_images WHERE house_pk = ?", (house_pk,))
        db.commit()
        response.status = 200
        return "House has been deleted"
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
#Arango Setup
##############################
client = ArangoClient()
arangoDb = client.db('_system', username='root', password='')
#Husk docker
#http://127.0.0.1:8529/_db/_system/_admin/aardvark/index.html#collections
@post("/arango/create_collections")
def _():

    if not arangoDb.has_collection("users"):
        arangoDb.create_collection("users")
    if not arangoDb.has_collection("houses"):
        arangoDb.create_collection("houses")

    house_collection = arangoDb.collection("houses")
    users_collection = arangoDb.collection("users")

    sample_users = [
                {
                    "user_username": "john_doe",
                    "user_email": "john@example.com",
                    "user_password": "password123",
                    "user_role": "admin",
                    "user_created_at": int(time.time()),
                    "user_updated_at": 0,
                    "user_deleted_at": 0,
                    "user_is_verified": 1,
                    "user_is_blocked": 0,
                    "user_verification_key": "abc123"
                },
                {
                    "user_username": "jane_smith",
                    "user_email": "jane@example.com",
                    "user_password": "password456",
                    "user_role": "partner",
                    "user_created_at": int(time.time()),
                    "user_updated_at": 0,
                    "user_deleted_at": 0,
                    "user_is_verified": 1,
                    "user_is_blocked": 0,
                    "user_verification_key": "xyz789",
                    "houses": [
                        {
                        "house_name": "Beach House",
                        "house_description": "A beautiful beach house",
                        "house_price_per_night": 200,
                        "house_latitude": 34.0195,
                        "house_longitude": -118.4912,
                        "house_stars": 4.5,
                        "house_created_at": 1625068800,
                        "house_updated_at": 0,
                        "house_is_blocked": 0
                        },
                        {
                        "house_name": "Mountain Cabin",
                        "house_description": "A cozy cabin in the mountains",
                        "house_price_per_night": 150,
                        "house_latitude": 39.7392,
                        "house_longitude": -104.9903,
                        "house_stars": 4.8,
                        "house_created_at": 1625155200,
                        "house_updated_at": 0,
                        "house_is_blocked": 0
                        }
                    ]
                }
            ]

    users_collection.import_bulk(sample_users)

    sample_houses = [
            {
                "house_name": "Beach House",
                "house_description": "A beautiful beach house",
                "house_price_per_night": 200,
                "house_latitude": 34.0195,
                "house_longitude": -118.4912,
                "house_stars": 4.5,
                "house_created_at": 1625068800,
                "house_updated_at": 0,
                "house_is_blocked": 0,
                "user_pk": "user1"
            },
            {
                "house_name": "Mountain Cabin",
                "house_description": "A cozy cabin in the mountains",
                "house_price_per_night": 150,
                "house_latitude": 39.7392,
                "house_longitude": -104.9903,
                "house_stars": 4.8,
                "house_created_at": 1625155200,
                "house_updated_at": 0,
                "house_is_blocked": 0,
                "user_pk": "user1"
            }
    ]

    house_collection.import_bulk(sample_houses)

    return "Collection 'users' and 'houses' have been created and sampled"

##############################
@post("/arango/users")
def _():
    try:
        user_data = request.json
        user_data["created_at"] = int(time.time())
        user_data["updated_at"] = 0
        user_data["deleted_at"] = 0
        user_data["user_verification_key"] = str(uuid.uuid4())

        users_collection = arangoDb.collection("users")
        user = users_collection.insert(user_data)
        return {"User created successfully ", user["_key"]}
    except Exception as ex:
        print(ex)

@get("/arango/users")
def _():
    try:
        users_collection = arangoDb.collection("users")
        cursor = users_collection.all()
        all_users_json = [doc for doc in cursor]
        return dumps(all_users_json)
    except Exception as ex:
        print(ex)


@get("/arango/users/<_key>")
def _(_key):
    try:
        users_collection = arangoDb.collection("users")
        user = users_collection.get(_key)
        if user:
            return user
        response.status = 404
        return "User not found"
    except Exception as ex:
        print(ex)

@put("/arango/users/<_key>")
def _(_key):
    try:
        user_data = request.json
        users_collection = arangoDb.collection("users")
        user = users_collection.get(_key)
        if user:
            user_data["updated_at"] = int(time.time())
            users_collection.update_match({"_key": _key}, user_data)
            return "User updated successfully"
        response.status = 404
        return "User not found"
    except Exception as ex:
        print(ex)

@delete("/arango/users/<_key>")
def _(_key):
    try:
        users_collection = arangoDb.collection("users")
        user = users_collection.get(_key)
        if user:
            users_collection.delete_match({"_key": _key})
            return "User deleted successfully"
        response.status = 404
        return "User not found"
    except Exception as ex:
        print(ex)

##############################

try:
    import production
    application = default_app()
except Exception as ex:
    print("Running local server")
    run(host="0.0.0.0", port=5000, debug=True, reloader=True)
