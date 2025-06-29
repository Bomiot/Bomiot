from locust import HttpUser, task, between

class DjangoVueAdminUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.login()

    def login(self):
        response = self.client.post(
            "/login/",
            json={"username": "admin", "password": "admin"}
        )
        result = response.json()
        self.token = result.get("token", "")
        self.headers = {"token": f"{self.token}"} if self.token else {}

    @task(1)
    def get_django_test(self):
        self.client.get("/test/", headers=self.headers, name="Get django test")

    @task(1)
    def get_fastapi_test(self):
        self.client.get("/fastapi/test/", headers=self.headers, name="Get fastapi test")
    
    @task(1)
    def get_flask_test(self):
        self.client.get("/flask/test/", headers=self.headers, name="Get flask test")