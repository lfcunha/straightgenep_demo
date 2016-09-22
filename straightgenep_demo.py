from flask import Flask, render_template, request
from wsgiref import simple_server
import requests
import json
import time

app = Flask(__name__)


@app.template_filter('ctime')
def timectime(s):
    return time.ctime(int(s)) # datetime.datetime.fromtimestamp(s)

@app.route('/demo/<username>')
def user(username=None):
    token, comp_req, around_me = None, None, []
    try:
        token_req = requests.get("http://localhost:8871/authorization_token/" + username)
        if token_req.status_code < 400:
            token = token_req.text
    except Exception:
        pass
    if token:
        headers = {'Authorization': 'Bearer ' + token}
        try:
            comp_reqs_req = requests.get("http://localhost:8871/compatibility_requests", headers=headers)
            if comp_reqs_req.status_code < 400:
                comp_req = comp_reqs_req.text
        except Exception:
            pass
        try:
            headers = {"Content-Type": "application/json"}
            url = "http://localhost:8871/match/geo/" + username
            data = {"lat": None, "lon": None, "radius": 10, "offset": 0, "limit": 50}
            around_me_req = requests.post(url, data=json.dumps(data), headers=headers)
        except Exception:
            pass
        else:
            if around_me_req.status_code < 400:
                around_me = around_me_req.text
                print("#records: ", len(json.loads(around_me)))
    return render_template('index.html', username=username, token=token, comp_req=comp_req,
                           requester=json.loads(comp_req)["requester"],
                           requestee=json.loads(comp_req)["requestee"],
                           around_me=json.loads(around_me))

if __name__ == "__main__":
    httpd = simple_server.make_server('0.0.0.0', 8000, app)
    httpd.serve_forever()
    # app.run(host='0.0.0.0')
