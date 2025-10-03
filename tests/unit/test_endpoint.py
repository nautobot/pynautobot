"""Endpoint tests"""

import unittest
from unittest.mock import Mock, patch

from pynautobot.core.endpoint import Endpoint, GraphqlEndpoint, JobsEndpoint
from pynautobot.core.response import Record


# pylint: disable=too-many-public-methods
class EndPointTestCase(unittest.TestCase):
    """Endpoint Test Case"""

    def setUp(self):
        self.api = Mock(base_url="http://localhost:8000/api", default_filters={})
        self.app = Mock(name="test")
        self.test_obj = Endpoint(self.api, self.app, "test")

    def test_filter(self):
        with patch("pynautobot.core.query.Request.get", return_value=Mock()) as mock:
            mock.return_value = [{"id": 123}, {"id": 321}]
            test = self.test_obj.filter(test="test")
            self.assertEqual(len(test), 2)

    def test_filter_reserved_kwargs(self):
        with self.assertRaises(ValueError) as _:
            self.test_obj.filter(pk=1)

    def test_all_none_limit_offset(self):
        with patch("pynautobot.core.query.Request.get", return_value=Mock()) as mock:
            mock.return_value = [{"id": 123}, {"id": 321}]
            with self.assertRaises(ValueError) as _:
                self.test_obj.all(limit=None, offset=1)

    def test_all_equals_filter_empty_kwargs(self):
        with patch("pynautobot.core.query.Request.get", return_value=Mock()) as mock:
            mock.return_value = [{"id": 123}, {"id": 321}]
            self.assertEqual(self.test_obj.all(), self.test_obj.filter())

    def test_all_accepts_kwargs(self):
        with patch("pynautobot.core.endpoint.Endpoint.filter", return_value=Mock()) as mock:
            self.test_obj.all(include=["config_context"])
            mock.assert_called_with(include=["config_context"])

    def test_filter_zero_limit_offset(self):
        with patch("pynautobot.core.query.Request.get", return_value=Mock()) as mock:
            mock.return_value = [{"id": 123}, {"id": 321}]
            with self.assertRaises(ValueError) as _:
                self.test_obj.filter(test="test", limit=0, offset=1)

    def test_choices(self):
        with patch("pynautobot.core.query.Request.options", return_value=Mock()) as mock:
            mock.return_value = {
                "schema": {
                    "properties": {
                        "letter": {
                            "enum": [1, 2, 3],
                            "enumNames": ["A", "B", "C"],
                        }
                    }
                }
            }
            choices = self.test_obj.choices()
            self.assertEqual(choices["letter"][1]["display"], "B")
            self.assertEqual(choices["letter"][1]["value"], 2)

    def test_update_with_id_and_data(self):
        with patch("pynautobot.core.query.Request._make_call", return_value=Mock()) as mock:
            mock.return_value = [{"name": "test"}]
            test = self.test_obj.update(id="db8770c4-61e5-4999-8372-e7fa576a4f65", data={"name": "test"})
            mock.assert_called_with(verb="patch", data={"name": "test"})
            self.assertTrue(test)

    def test_update_with_id_and_data_args(self):
        with patch("pynautobot.core.query.Request._make_call", return_value=Mock()) as mock:
            mock.return_value = [{"name": "test"}]
            test = self.test_obj.update("db8770c4-61e5-4999-8372-e7fa576a4f65", {"name": "test"})
            mock.assert_called_with(verb="patch", data={"name": "test"})
            self.assertTrue(test)

    def test_update_with_id_and_data_args_kwargs(self):
        with patch("pynautobot.core.query.Request._make_call", return_value=Mock()) as mock:
            mock.return_value = [{"name": "test"}]
            test = self.test_obj.update("db8770c4-61e5-4999-8372-e7fa576a4f65", data={"name": "test"})
            mock.assert_called_with(verb="patch", data={"name": "test"})
            self.assertTrue(test)

    def test_update_with_dict(self):
        with patch("pynautobot.core.query.Request._make_call", return_value=Mock()) as mock:
            mock.return_value = [{"id": "db8770c4-61e5-4999-8372-e7fa576a4f65", "name": "test"}]
            test = self.test_obj.update([{"id": "db8770c4-61e5-4999-8372-e7fa576a4f65", "name": "test"}])
            mock.assert_called_with(verb="patch", data=[{"id": "db8770c4-61e5-4999-8372-e7fa576a4f65", "name": "test"}])
            self.assertTrue(test)

    def test_update_with_objects(self):
        with patch("pynautobot.core.query.Request._make_call", return_value=Mock()) as mock:
            ids = ["db8770c4-61e5-4999-8372-e7fa576a4f65", "e9b5f2e0-4f20-41ad-9179-90a4987f743e"]
            objects = [Record({"id": i, "name": "test_" + str(i)}, self.api, self.test_obj) for i in ids]
            for o in objects:
                o.name = "new_" + str(o.id)
            mock.return_value = [o.serialize() for o in objects]
            test = self.test_obj.update(objects)
            mock.assert_called_with(verb="patch", data=[{"id": i, "name": "new_" + str(i)} for i in ids])
            self.assertTrue(test)

    def test_update_with_invalid_objects_type(self):
        objects = {"id": "db8770c4-61e5-4999-8372-e7fa576a4f65", "name": "test"}
        with self.assertRaises(ValueError) as exc:
            self.test_obj.update(objects)
        self.assertEqual(
            str(exc.exception), "You must provide either a UUID and data dict or a list of objects to update"
        )

    def test_update_with_invalid_type_in_objects(self):
        objects = [[{"id": "db8770c4-61e5-4999-8372-e7fa576a4f65", "name": "test"}]]
        with self.assertRaises(ValueError) as exc:
            self.test_obj.update(objects)
        self.assertEqual(str(exc.exception.__cause__), "Invalid object type: <class 'list'>")

    def test_update_with_missing_id_attribute(self):
        objects = [
            Record({"no_id": "db8770c4-61e5-4999-8372-e7fa576a4f65", "name": "test"}, self.api, self.test_obj),
        ]
        with self.assertRaises(ValueError) as exc:
            self.test_obj.update(objects)
        self.assertEqual(str(exc.exception.__cause__), "'Record' object has no attribute 'id'")

    def test_delete_with_ids(self):
        with patch("pynautobot.core.query.Request._make_call", return_value=Mock()) as mock:
            ids = ["db8770c4-61e5-4999-8372-e7fa576a4f65", "e9b5f2e0-4f20-41ad-9179-90a4987f743e"]
            mock.return_value = True
            test = self.test_obj.delete(ids)
            mock.assert_called_with(verb="delete", data=[{"id": i} for i in ids])
            self.assertTrue(test)

    def test_delete_with_objects(self):
        with patch("pynautobot.core.query.Request._make_call", return_value=Mock()) as mock:
            ids = ["db8770c4-61e5-4999-8372-e7fa576a4f65", "e9b5f2e0-4f20-41ad-9179-90a4987f743e"]
            mock.return_value = True
            objects = [Record({"id": i, "name": "test_" + str(i)}, self.api, self.test_obj) for i in ids]
            test = self.test_obj.delete(objects)
            mock.assert_called_with(verb="delete", data=[{"id": i} for i in ids])
            self.assertTrue(test)

    def test_delete_with_invalid_uuid(self):
        ids = ["123", "456"]
        with self.assertRaises(ValueError) as exc:
            self.test_obj.delete(ids)
        self.assertEqual(str(exc.exception.__cause__), "badly formed hexadecimal UUID string")

    def test_delete_with_invalid_id_type(self):
        ids = [123, 456]
        with self.assertRaises(ValueError) as exc:
            self.test_obj.delete(ids)
        self.assertEqual(str(exc.exception.__cause__), "Invalid object type: <class 'int'>")

    def test_delete_with_invalid_object(self):
        objects = [
            Record({"no_id": "db8770c4-61e5-4999-8372-e7fa576a4f65", "name": "test"}, self.api, self.test_obj),
        ]
        with self.assertRaises(ValueError) as exc:
            self.test_obj.delete(objects)
        self.assertEqual(str(exc.exception.__cause__), "'Record' object has no attribute 'id'")


class JobEndPointTestCase(unittest.TestCase):
    """Job Endpoint Test Case"""

    def test_run_job_name(self):
        with patch("pynautobot.core.query.Request.post", return_value=Mock()) as mock:
            api = Mock(base_url="http://localhost:8000/api", api_version="2.4")
            app = Mock(name="test")
            mock.return_value = [{"schedule": {"id": 123}, "job_result": {"id": 123, "status": {"value": "foo"}}}]
            test_obj = JobsEndpoint(api, app, "test")
            test = test_obj.run(job_name="test")
            self.assertEqual(len(test), 1)

    # Run and Wait Tests
    # =================================================

    @patch("pynautobot.core.query.Request.get", return_value=Mock())
    @patch("pynautobot.core.query.Request.post", return_value=Mock())
    def test_run_and_wait_greater_v1_3(self, mock_post, mock_get):
        api = Mock(base_url="http://localhost:8000/api")
        app = Mock(name="test")
        test_obj = JobsEndpoint(api, app, "test")
        mock_post.return_value = {"schedule": {"id": 123}, "job_result": {"id": 123, "status": {"value": "PENDING"}}}
        mock_get.return_value = {"schedule": {"id": 123}, "job_result": {"id": 123, "status": {"value": "SUCCESS"}}}
        test = test_obj.run_and_wait(job_id="test", interval=1, max_rechecks=5)
        self.assertEqual(test.job_result.id, 123)

    @patch("pynautobot.core.query.Request.get", return_value=Mock())
    @patch("pynautobot.core.query.Request.post", return_value=Mock())
    def test_run_and_wait_invalid_input(self, mock_post, mock_get):
        api = Mock(base_url="http://localhost:8000/api", api_version="1.3")
        app = Mock(name="test")
        test_obj = JobsEndpoint(api, app, "test")
        mock_post.return_value = {"schedule": {"id": 123}, "job_result": {"id": 123, "status": {"value": "PENDING"}}}
        mock_get.return_value = {"schedule": {"id": 123}, "job_result": {"id": 123, "status": {"value": "PENDING"}}}
        with self.assertRaises(ValueError):
            test_obj.run_and_wait(job_id="test", interval=0, max_rechecks=0)


class GraphqlEndPointTestCase(unittest.TestCase):
    """Graphql Endpoint Test Case"""

    def test_invalid_arg(self):
        with self.assertRaises(
            TypeError, msg="GraphqlEndpoint.run() missing 1 required positional argument: 'query_id'"
        ):
            api = Mock(base_url="http://localhost:8000/api")
            app = Mock(name="test")
            test_obj = GraphqlEndpoint(api, app, "test")
            test_obj.run()  # pylint: disable=no-value-for-parameter
