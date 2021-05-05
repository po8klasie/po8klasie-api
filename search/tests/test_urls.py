from django.test import TestCase


class TestUrls(TestCase):
    def test_graphql_endpoint(self):
        data = {"query": "query {\n  __typename\n}", "variables": None}
        response = self.client.post(
            "/api/graphql/", data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
