from bottle import default_app, get, post, run
import git

#https://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@github.com/mikkelThodeSchultz/wd_exam.git

@post('/1fa5b451-8928-40e8-9324-f707ebfcb485')
def git_update():
    repo = git.Repo('./wd_exam')
    origin = repo.remotes.origin
    repo.create_head('main', origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
    origin.pull()
    return ""

 
##############################
@get("/")
def _():
    return "Five"
 
##############################
try:
    import production
    application = default_app()
except Exception as ex:
    print("Running local server")
    run(host="127.0.0.1", port=80, debug=True, reloader=True)