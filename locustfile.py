
from locust import HttpUser, between, task
import json

class WebsiteUser(HttpUser):
    wait_time = between(5, 15)
    access_token = ''
    def on_start(self):
        r = self.client.post("/users/login", {
            "username": "goku3",
            "password": "1234"
        })
        accessToken = r.json()['accessToken']
        self.access_token = accessToken
        
    # @task
    # def creatroom(self):
    #     self.client.post(
    #         url="/rooms",
    #         data= 'title=roomA&inviteUser=8%2C24',
    #         auth=None,
    #         headers={"Authorization": "Bearer " + self.access_token , 'Content-Type': 'application/x-www-form-urlencoded'},
    #     )
    
    @task
    def following(self):
        self.client.get(
            url="/users/following",
            auth=None,
            headers={"Authorization": "Bearer " + self.access_token , 'Content-Type': 'application/x-www-form-urlencoded'},
        )
        
