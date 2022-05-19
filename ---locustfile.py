# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import json
import uuid
import time
import gevent

from websocket import create_connection, WebSocket
import ssl

import six
import locust.event as event 


from locust import HttpUser, TaskSet, task
# from locust.event import request_success


class EchoTaskSet(TaskSet):

    def on_start(self):
        self.user_id = six.text_type(uuid.uuid4())
        ws = WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
        ws.connect("wss://localhost:443")
        # ws = create_connection('wss://localhost:443')
        self.ws = ws

        def _receive():
            while True:
                res = ws.recv()
                data = json.loads(res)
                end_at = time.time()
                response_time = int((end_at - data['start_at']) * 1000000)
                event.Events().request_success.fire(
                    request_type='WebSocket Recv',
                    name='test/ws/getRoomRtpCapabilities',
                    response_time=response_time,
                    response_length=len(res),
                )
                # request_success.fire(
                #     request_type='WebSocket Recv',
                #     name='test/ws/echo',
                #     response_time=response_time,
                #     response_length=len(res),
                # )

        gevent.spawn(_receive)

    def on_quit(self):
        self.ws.close()

    @task
    def sent(self):
        start_at = time.time()
        # body = json.dumps({'message': 'hello, world',
        #                   'user_id': self.user_id, 'start_at': start_at})
        body = json.dumps({
                        "ms_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI4IiwiaWF0IjoxNjUyOTU2NzQyLCJleHAiOjE2NTMwNDMxNDJ9.Y3Ftu9EJyBBCb2eWLD9bpIuNYTKlCs8kADXAZGf1txGHdaYh8gh0jviZw9l49LTOQc1HM-3m8Z9Ce0LZMdcLo6i1BNFvubL-GBNm0IpkNx5ergHDQ73yXBzVZcshF-uAIXDAP8H8sWMaKXNFPWANpLFuZbYOE0hm-qFnlKYpSMx1Tum4jh5mNC7bCdZjxgC3-AgY9Q610U-iDsUoh3inySbpbrrVNuofwugezcRMgldYG1ePBnZANDZUC6u0Kwjk8CSZpKbSnwpjBpgUtfXc2pwEyaVa-vnTwJ_gJYusykH9SqEeZWKrtc0HGO1dYkWoKmnNpUp0MB50TXwWRScFAg",
                        "action": "getRoomRtpCapabilities",
                        'user_id': self.user_id, 'start_at': start_at})
        self.ws.send(body)
        event.Events().request_success.fire(
            request_type='WebSocket Sent',
            name='test/ws/getRoomRtpCapabilities',
            response_time=int((time.time() - start_at) * 1000000),
            response_length=len(body),
        )


# class ChatTaskSet(TaskSet):
#     def on_start(self):
#         self.user_id = six.text_type(uuid.uuid4())
#         # ws = create_connection('wss://127.0.0.1:443')
#         ws = WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
#         ws.connect("wss://localhost:443")
#         # ws = create_connection('ws://127.0.0.1:5000/chat')
#         self.ws = ws

#         def _receive():
#             while True:
#                 res = ws.recv()
#                 data = json.loads(res)
#                 end_at = time.time()
#                 response_time = int((end_at - data['start_at']) * 1000000)
#                 event.Events().request_success.fire(
#                     request_type='WebSocket Recv',
#                     name='test/ws/chat',
#                     response_time=response_time,
#                     response_length=len(res),
#                 )

#         gevent.spawn(_receive)

#     def on_quit(self):
#         self.ws.close()

#     @task
#     def sent(self):
#         start_at = time.time()
#         # body = json.dumps({'message': 'hello, world',
#         #                   'user_id': self.user_id, 'start_at': start_at})
#         body = json.dumps({
#                         "ms_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI4IiwiaWF0IjoxNjUyOTU2NzQyLCJleHAiOjE2NTMwNDMxNDJ9.Y3Ftu9EJyBBCb2eWLD9bpIuNYTKlCs8kADXAZGf1txGHdaYh8gh0jviZw9l49LTOQc1HM-3m8Z9Ce0LZMdcLo6i1BNFvubL-GBNm0IpkNx5ergHDQ73yXBzVZcshF-uAIXDAP8H8sWMaKXNFPWANpLFuZbYOE0hm-qFnlKYpSMx1Tum4jh5mNC7bCdZjxgC3-AgY9Q610U-iDsUoh3inySbpbrrVNuofwugezcRMgldYG1ePBnZANDZUC6u0Kwjk8CSZpKbSnwpjBpgUtfXc2pwEyaVa-vnTwJ_gJYusykH9SqEeZWKrtc0HGO1dYkWoKmnNpUp0MB50TXwWRScFAg",
#                         "action": "getRoomRtpCapabilities",
#                         'user_id': self.user_id, 'start_at': start_at})
#         self.ws.send(body)
#         event.Events().request_success.fire(
#             request_type='WebSocket Sent',
#             name='test/ws/getRoomRtpCapabilities',
#             response_time=int((time.time() - start_at) * 1000000),
#             response_length=len(body),
#         )


class EchoLocust(HttpUser):
    tasks = [EchoTaskSet]
    min_wait = 0
    max_wait = 100


# class ChatLocust(HttpUser):
#     tasks = [ChatTaskSet]
#     min_wait = 0
