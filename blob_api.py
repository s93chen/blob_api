import json
import flask 
import requests
from hashlib import sha256 
from urllib.parse import parse_qs

# flask has a class called Request for handling requests, 
# and a class called Response for representing responses:
# http://flask.pocoo.org/docs/1.0/api/#flask.Request

# obj storage
objects = dict()

class ObjectInfo:
    """
     Stores the object's information.
     An ObjectInfo instance is only created
     if the corresponding object id (oid)
     does not exist.

      - repos: set of repos this obj is in
      - content: request body, bytes type
      - size: size of content in bytes
    """
   
    def __init__(self, first_repo, content): 
        self.repos = set()
        self.repos.add(first_repo)
        self.content = content
        self.size = len(content)


# Create flask app
app = flask.Flask(__name__)

# Home
@app.route("/")
def home_page():
    if not objects:
        return "You currently do not have any objects."
    
    out = ""
    for k, v in objects.items():
        out += "* Object: {}, Repos: {} <br />".format(k, str(v.repos))

    return out

# Handle object creation
@app.route("/<repo>", methods=["PUT"])
def add_object(repo):
    req_body = flask.request.get_data()
    oid = sha256(req_body).hexdigest()

    if oid not in objects:
        objects[oid] = ObjectInfo(repo, req_body)
    else:
        objects[oid].repos.add(repo)

    """ Manual way of returning response

    resp_body = {"oid": oid, "size": len(req_body)}
    json_body = json.dumps(resp_body).encode("utf-8")

    headers = {"Content-Length": len(json_body),
               "Content-Type": "application/json"}

    return (json_body, 201, headers)
    """

    resp_body = {"oid": oid, "size": len(req_body)}
    return flask.jsonify(resp_body), 201

# Handle object query
@app.route("/<repo>/<oid>")
def get_object(repo, oid):
    if (oid in objects) and (repo in objects[oid].repos):
        resp_body = objects[oid].content
        return resp_body, 200
    
    return flask.abort(404)

# Handle object deletion
@app.route("/<repo>/<oid>", methods=["DELETE"])
def delete_object(repo, oid):
    if (oid in objects) and (repo in objects[oid].repos):
        # if object in multiple repos
        if len(objects[oid].repos) > 1:
            objects[oid].repos.remove(repo)
        else:
            del objects[oid]
        return "Object {} deleted from {}".format(oid, repo), 200

    return flask.abort(404)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
