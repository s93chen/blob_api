This exercise implements a flask API for below requirements.

## API Requirements
Create an HTTP API which stores objects owned by
repositories.

* A repository is identified by a string.
* An object is an arbitrary sequence of bytes.
* Each object has an ID string, the <a href="https://cryptii.com/pipes/hash-function">SHA-256</a> hash of the object in hex format.

API users should be able to add a new object to a repository, retrieve an
object from a repository and delete an object from a repository. These details
are specified below.

## Supported HTTP Methods
* GET
* PUT
* DELETE

If a request uses any other HTTP method, you should return 405 (bad method).

### 1.1 PUT
Requests use the path ```/REPOSITORY```, where ```REPOSITORY``` is a
string which identifies the repository that the object should be added to.
```
PUT /data/somerepo HTTP/1.1

Hello, world!
```

Responses should be in JSON-format. They should contain the object ID and size
in bytes. For example, ```oid``` below equals the hash of "Hello, world!". HTTP
code 201 should be returned.
```
HTTP/1.1 201 Created
Content-Length: 84
Content-Type: application/json

{"oid":"315f5bdb76d078c43b8ac0064e4a0164612b1fce77c869345bfc94c75894edd3","size":13}
```

### 1.2 GET
Requests specify a repository and object ID in the URL path.
```
GET /somerepo/315f5bdb76d078c43b8ac0064e4a0164612b1fce77c869345bfc94c75894edd3 HTTP/1.1
```

Responses should return the object bytes in the body. If the specified
repository or object ID do not exist, return HTTP code 404. Note: your response
headers will not be checked.
```
HTTP/1.1 200 OK
Content-Length: 13

Hello, world!
```

### 1.3 DELETE
Deletion should return HTTP code 200 always.
```
DELETE /somerepo/315f5bdb76d078c43b8ac0064e4a0164612b1fce77c869345bfc94c75894edd3 HTTP/1.1
