from bottle import default_app, get, post, run, template, static_file
import git

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
try:
    import production
    application = default_app()
except Exception as ex:
    print("Running local server")
    run(host="127.0.0.1", port=80, debug=True, reloader=True)