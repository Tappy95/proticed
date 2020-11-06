import random
from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(5, 9)

    @task
    def index_page(self):
        # self.client.get(
        #     "/ebay",
        #     headers={
        #         "Authorization": "123456"
        #     }
        # )/userInfo/loginByPassword?mobile=13244444444&password=e10adc3949ba59abbe56e057f20f883e&imei=e7f159ef35bfa4a4&equipmentType=1&registrationId=
        self.client.get(
            "/api/userInfo/loginByPassword?mobile=13244444444&password=e10adc3949ba59abbe56e057f20f883e&imei=e7f159ef35bfa4a4&equipmentType=1",
            headers={
                "Authorization": "123456"
            }
        )

    # @task(3)
    # def view_item(self):
    #     item_id = random.randint(1, 10000)
    #     self.client.get(f"/item?id={item_id}", name="/item")
    #
    # def on_start(self):
    #     self.client.post("/login", {"username": "foo", "password": "bar"})
