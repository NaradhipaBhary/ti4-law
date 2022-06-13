import random

from locust import FastHttpUser, task


class StressTestingUser(FastHttpUser):

    def on_start(self):
        self.transaction_id = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        self.npm = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        self.client.post(f"/update", json={
            "name": "Test user",
            "NPM": self.npm
        })

    @task
    def retrieve_data(self):
        self.client.get(f"/read/{self.npm}", name="/read/{NPM}")
        self.client.get(f"/read/{self.npm}/{self.transaction_id}", name="/read/{NPM}/{TXID}")
