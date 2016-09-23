from flask import Flask, render_template, request
from wsgiref import simple_server
import requests
import json
import time
import os
import ConfigParser

app = Flask(__name__)

config_file = "config.ini"
config = ConfigParser.ConfigParser()
config.readfp(open(config_file))
api_host = "localhost"  # config.get('api', "host")
api_port = config.get('api', "port")
demo_host = "localhost"  # config.get('demo', "host")
demo_port = config.get('demo', "port")

API_URI = "http://" + api_host + ":" + api_port  # OR INTRANET IP

@app.template_filter('ctime')
def timectime(s):
    return time.ctime(int(s))  # datetime.datetime.fromtimestamp(s)


@app.route('/demo/<username>')
def user(username=None):
    token, comp_req, around_me = None, None, []
    try:
        url = API_URI + os.sep + "authorization_token" + os.sep + username
        print url
        token_req = requests.get(url)
        if token_req.status_code < 400:
            token = token_req.text
    except Exception:
        pass
    if token:
        headers = {'Authorization': 'Bearer ' + token}
        try:
            comp_reqs_req = requests.get(API_URI + os.sep + "compatibility_requests", headers=headers)
            print comp_reqs_req.status_code
            if comp_reqs_req.status_code < 400:
                comp_req = comp_reqs_req.text
        except Exception as e:
            print e
            pass
        try:
            headers = {"Content-Type": "application/json"}
            url = API_URI + os.sep + "match" + os.sep + "geo" + os.sep + username
            data = {"lat": None, "lon": None, "radius": 10, "offset": 0, "limit": 50}
            around_me_req = requests.post(url, data=json.dumps(data), headers=headers)
        except Exception as e:
            print e
            pass
        else:
            if around_me_req.status_code < 400:
                around_me = around_me_req.text
        print username, token, comp_req
    return render_template('index.html', username=username, token=token, comp_req=comp_req,
                           requester=json.loads(comp_req)["requester"],
                           requestee=json.loads(comp_req)["requestee"],
                           around_me=json.loads(around_me))


if __name__ == "__main__":
    httpd = simple_server.make_server('0.0.0.0', int(demo_port), app)
    httpd.serve_forever()
    # app.run(host='0.0.0.0')
