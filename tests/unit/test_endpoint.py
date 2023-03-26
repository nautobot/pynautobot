import unittest
from unittest.mock import Mock, patch

from pynautobot.core.endpoint import Endpoint, JobsEndpoint


class EndPointTestCase(unittest.TestCase):
    def test_filter(self):
        with patch("pynautobot.core.query.Request.get", return_value=Mock()) as mock:
            api = Mock(base_url="http://localhost:8000/api")
            app = Mock(name="test")
            mock.return_value = [{"id": 123}, {"id": 321}]
            test_obj = Endpoint(api, app, "test")
            test = test_obj.filter(test="test")
            self.assertEqual(len(test), 2)

    def test_filter_empty_kwargs(self):
        api = Mock(base_url="http://localhost:8000/api")
        app = Mock(name="test")
        test_obj = Endpoint(api, app, "test")
        with self.assertRaises(ValueError) as _:
            test_obj.filter()

    def test_filter_reserved_kwargs(self):
        api = Mock(base_url="http://localhost:8000/api")
        app = Mock(name="test")
        test_obj = Endpoint(api, app, "test")
        with self.assertRaises(ValueError) as _:
            test_obj.filter(pk=1)
        with self.assertRaises(ValueError) as _:
            test_obj.filter(limit=1)
        with self.assertRaises(ValueError) as _:
            test_obj.filter(offset=1)

    def test_choices(self):
        with patch("pynautobot.core.query.Request.options", return_value=Mock()) as mock:
            api = Mock(base_url="http://localhost:8000/api")
            app = Mock(name="test")
            mock.return_value = {
                "actions": {
                    "POST": {
                        "letter": {
                            "choices": [
                                {"display_name": "A", "value": 1},
                                {"display_name": "B", "value": 2},
                                {"display_name": "C", "value": 3},
                            ]
                        }
                    }
                }
            }
            test_obj = Endpoint(api, app, "test")
            choices = test_obj.choices()
            self.assertEqual(choices["letter"][1]["display_name"], "B")
            self.assertEqual(choices["letter"][1]["value"], 2)


class JobEndPointTestCase(unittest.TestCase):
    def test_invalid_arg_less_v1_3(self):
        with self.assertRaises(
            ValueError, msg='Keyword Argument "class_path" is required to run a job in Nautobot APIv1.2 and older.'
        ):
            api = Mock(base_url="http://localhost:8000/api", api_version="1.2")
            app = Mock(name="test")
            test_obj = JobsEndpoint(api, app, "test")
            test_obj.run(job_id="test")

    def test_run_less_v1_3(self):
        with patch("pynautobot.core.query.Request.post", return_value=Mock()) as mock:
            api = Mock(base_url="http://localhost:8000/api", api_version="1.2")
            app = Mock(name="test")
            mock.return_value = [{"schedule": {"id": 123}, "job_result": {"id": 123, "status": {"value": "foo"}}}]
            test_obj = JobsEndpoint(api, app, "test")
            test = test_obj.run(class_path="test")
            self.assertEqual(len(test), 1)

    def test_invalid_arg_greater_v1_3(self):
        with self.assertRaises(
            ValueError, msg='Keyword Argument "job_id" is required to run a job in Nautobot APIv1.3 and newer.'
        ):
            api = Mock(base_url="http://localhost:8000/api", api_version="1.3")
            app = Mock(name="test")
            test_obj = JobsEndpoint(api, app, "test")
            test_obj.run(class_path="test")

    def test_run_greater_v1_3(self):
        with patch("pynautobot.core.query.Request.post", return_value=Mock()) as mock:
            api = Mock(base_url="http://localhost:8000/api", api_version="1.3")
            app = Mock(name="test")
            mock.return_value = [{"schedule": {"id": 123}, "job_result": {"id": 123, "status": {"value": "foo"}}}]
            test_obj = JobsEndpoint(api, app, "test")
            test = test_obj.run(job_id="test")
            self.assertEqual(len(test), 1)
