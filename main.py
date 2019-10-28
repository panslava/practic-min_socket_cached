#!/usr/bin/env python

import socket
import logging
import redis
import json

sock = socket.socket()
sock.bind(('', 65432))
sock.listen()
conn, addr = sock.accept()

cache = redis.Redis(host='redis_cache', port=6379)

# logging.basicConfig(filename="/var/log/server.log", level=logging.INFO)

while True:
    data = conn.recv(1024)

    if not data:
        break

    response = {}
    request = {}

    try:
        request = json.loads(data)
    except ValueError as e:
        response["Status"] = "Bad Request"

    if request["action"] == "get":
        ans = cache.get(request["key"])

        if ans is None:
            response["Status"] = "Not found"
        else:
            if type(ans) is bytes:
                response["message"] = ans.decode('utf-8')
            else:
                response["message"] = ans
            response["Status"] = "OK"

    if request["action"] == "put":
        if cache.exists(request["key"]):
            response["Status"] = "Key already exists"
        else:
            response["Status"] = "Created"
            cache.set(request["key"], request["message"])

    if request["action"] == "delete":
        if cache.exists(request["key"]):
            cache.delete(request["key"])
            response["Status"] = "OK"
        else:
            response["Status"] = "Not found"

    response_string = json.dumps(response)
    conn.send(response_string.encode('utf-8'))

conn.close()
