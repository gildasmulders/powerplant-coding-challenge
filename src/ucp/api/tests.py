import json
from os import path
from django.test import TestCase, Client
from pprint import pformat


class TestProductionPlan(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_get_fails(self):
        response = self.client.get("/productionplan/")
        self.assertEqual(response.status_code, 405)

    def test_post_payload1(self):
        payload = get_payload(1)

        res = self._make_request(payload)

        self._check_output(payload, res)

    def test_post_payload2(self):
        payload = get_payload(2)

        res = self._make_request(payload)

        self._check_output(payload, res)

    def test_post_payload3(self):
        payload = get_payload(3)

        res = self._make_request(payload)

        self._check_output(payload, res)

    def test_post_payload4(self):
        payload = get_payload(3)
        payload["powerplants"][-1]["type"] = "solar"

        res = self._make_request(payload)
        output = json.loads(res.content)
        print(header_str("output: "), pformat(output, compact=True, width=160))
        self.assertEqual(res.status_code, 400)

    def _make_request(self, payload):
        response = self.client.post("/productionplan/", payload, content_type="application/json")
        return response

    def _check_output(self, payload, response):
        output = json.loads(response.content)
        print(header_str("output: "), pformat(output, compact=True, width=160))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(all(set(plant.keys()) == {"name", "p"} for plant in output))
        self.assertEqual(sum(plant["p"] for plant in output), payload["load"])


def get_payload(example_number):
    assert example_number in [1, 2, 3]
    example_path = path.join(path.dirname(__file__),
                             "..", "..", "..",
                             "data", "example_payloads",
                             f"payload{example_number}.json")
    with open(example_path, "r") as f:
        payload = json.load(f)
        print(header_str("payload: "), pformat(payload, compact=True, width=160))
        return payload


def header_str(content):
    color = "\033[96m" if content == "output: " else "\033[92m"
    return f"\n {color}" + content + "\033[0m \n"
