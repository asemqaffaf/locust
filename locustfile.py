
from locust import HttpUser, between, task
import json

import json
import time

import ssl
from websocket import create_connection, WebSocket
import locust.event as event 

class WebsiteUser(HttpUser):
    wait_time = between(5, 15)
    access_token = ''
    ms_token = ''
    def on_start(self):
        r = self.client.post("/users/login", {
            "username": "goku3",
            "password": "1234"
        })
        accessToken = r.json()['accessToken']
        self.access_token = accessToken
        
    @task
    def creatroom(self):
        r = self.client.post(
            url="/rooms",
            data= 'title=roomA&inviteUser=8%2C24',
            auth=None,
            headers={"Authorization": "Bearer " + self.access_token , 'Content-Type': 'application/x-www-form-urlencoded'},
        )
        self.ms_token  =r.json()['ms_token']
        print(self.ms_token)
        self.get_room_rtp_capabilities(ms_token = self.ms_token)
        
    # @task
    def get_room_rtp_capabilities(self, ms_token):
        ws = WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
        ws.connect("wss://localhost:443")
        self.ws = ws
        body = json.dumps({
                        "ms_token": ms_token,
                        "action": "getRoomRtpCapabilities"})
        self.ws.send(body)
        event.Events().request_success.fire(
            request_type='WebSocket Sent',
            name='test/ws/getRoomRtpCapabilities',
            response_length=len(body),
        )
        
    @task
    def following(self):
        self.client.get(
            url="/users/following",
            auth=None,
            headers={"Authorization": "Bearer " + self.access_token , 'Content-Type': 'application/x-www-form-urlencoded'},
        )