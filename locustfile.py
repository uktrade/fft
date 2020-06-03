import os

from locust import (
    HttpLocust,
    TaskSet,
    task,
    between,
)

sso_headers = {
    "Cookie": f"csrftoken={os.environ['CRSF_TOKEN']}; sessionid={os.environ['SESSION_ID']}"
}

paste_content = ""


class UserBehaviour(TaskSet):
    @task(1)
    def index(self):
        self.client.get("", headers=sso_headers)

    @task(2)
    def post_to_edit_forecast(self):
        self.client.post(
            f"/forecast/edit/{os.environ['TEST_COST_CENTRE_CODE']}/",
            data={
                "all_selected": True,
                "paste_content": paste_content,
                "csrfmiddlewaretoken": os.environ['CRSF_TOKEN'],
                "headers": sso_headers,
            },
        )


class FFTUser(HttpLocust):
    task_set = UserBehaviour
    wait_time = between(5, 9)
