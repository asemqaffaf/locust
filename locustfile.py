
from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    def on_start(self):
        r = self.client.post("/users/login", {
            "username": "goku3",
            "password": "1234"
        })
        print(r.json())

    @task
    def login(self):
        # self.client.post("/users/login")
        self.client.post("/users/login", {
            "username": "goku3-----",
            "password": "1234"
        })
        

#     # @task
#     # def index(self):
#     #     self.client.get("/")
#     #     self.client.get("/static/assets.js")

#     # @task
#     # def about(self):
#     #     self.client.get("/about/")
