# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import json
import uuid
import time
from click import echo
import gevent

from websocket import create_connection, WebSocket
import six
import ssl
from locust import HttpUser, TaskSet, task
# from locust.events import event.Events().request_success
# from locust.events import request_success
from locust import events

# from websocket import create_connection

import locust.event as event 

class EchoTaskSet(TaskSet):
    ws = None
    def on_start(self):
        self.user_id = six.text_type(uuid.uuid4())
        ws = WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
        ws = create_connection("wss://localhost:443",sslopt={"cert_reqs": ssl.CERT_NONE})
        
        self.ws = ws
        
        def _receive():
            while True:
                res = ws.recv()
                data = json.loads(res)
                end_at = time.time()
                response_time = int((end_at - data['start_at']) * 1000000)
                events.request_success.fire(
                    request_type='WebSocket Recv',
                    name='ws/getRoomRtpCapabilities',
                    response_time=response_time,
                    response_length=len(res),
                )

        gevent.spawn(_receive)

    def on_quit(self):
        self.ws.close()

    @task
    def get_room_rtp_capabilities(self):
        start_at = time.time()
        body = json.dumps({
                        "ms_token": 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI4IiwiaWF0IjoxNjUyOTgzMzI2LCJleHAiOjE2NTMwNjk3MjZ9.dL_SbBQjrTV0Xsf8G9AEOCS1f7txd2wvrkidnrNpBCsl4UuLIbC3lAwiihZITmkOHMv3rbaqXUs2FO6sXU-XwecRNF4UDcG92VG1-nLpTdwhWFh04Dhtbfpp0Aj9VUyXo8VIIt53JiuiOzM_pt0lxdJwOR4HYgwGi8wC6p4Rmz4XcipGyMiftc7V1GDb4NIm0GIRamkQb2y52JZtvYAmULDJQM2ctPhK6gs-q0U2eqnQcmgkDs73lOTOC4EHBH_7_mJRh4il77Oae0XRPSHIiCPGb36oWBB5C9448ygLIaYJ6D4JcWhuOo67A0kX6W0VdG4qNcqSUBpV8Z2TpQstDg',
                        "action": "getRoomRtpCapabilities",
                        'start_at': start_at
                        })
        self.ws.send(body)
        events.request_success.fire(
            request_type='WebSocket Sent',
            name='ws/getRoomRtpCapabilities',
            response_time=int((time.time() - start_at) * 1000000),
            response_length=len(body),
        )

class EchoLocust(HttpUser):
    tasks = [EchoTaskSet]
    min_wait = 0
    max_wait = 100
