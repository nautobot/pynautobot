import unittest
from unittest.mock import Mock, patch

from pynautobot.core.endpoint import Endpoint, JobsEndpoint
from pynautobot.core.response import Record


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

    def test_choices(self):
        with patch("pynautobot.core.query.Request.options", return_value=Mock()) as mock:
            api = Mock(base_url="http://localhost:8000/api")
            app = Mock(name="test")
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
            test_obj = Endpoint(api, app, "test")
            choices = test_obj.choices()
            self.assertEqual(choices["letter"][1]["display"], "B")
            self.assertEqual(choices["letter"][1]["value"], 2)

    def test_update_with_id_and_data(self):
        with patch("pynautobot.core.query.Request._make_call", return_value=Mock()) as mock:
            api = Mock(base_url="http://localhost:8000/api")
            app = Mock(name="test")
            test_obj = Endpoint(api, app, "test")
            mock.return_value = [{"name": "test"}]
            test = test_obj.update(id="db8770c4-61e5-4999-8372-e7fa576a4f65", data={"name": "test"})
            mock.assert_called_with(verb="patch", data={"name": "test"})
            self.assertTrue(test)

    def test_update_with_id_and_data_args(self):
        with patch("pynautobot.core.query.Request._make_call", return_value=Mock()) as mock:
            api = Mock(base_url="http://localhost:8000/api")
            app = Mock(name="test")
            test_obj = Endpoint(api, app, "test")
            mock.return_value = [{"name": "test"}]
            test = test_obj.update("db8770c4-61e5-4999-8372-e7fa576a4f65", {"name": "test"})
            mock.assert_called_with(verb="patch", data={"name": "test"})
            self.assertTrue(test)

    def test_update_with_id_and_data_args_kwargs(self):
        with patch("pynautobot.core.query.Request._make_call", return_value=Mock()) as mock:
            api = Mock(base_url="http://localhost:8000/api")
            app = Mock(name="test")
            test_obj = Endpoint(api, app, "test")
            mock.return_value = [{"name": "test"}]
            test = test_obj.update("db8770c4-61e5-4999-8372-e7fa576a4f65", data={"name": "test"})
            mock.assert_called_with(verb="patch", data={"name": "test"})
            self.assertTrue(test)

    def test_update_with_dict(self):
        with patch("pynautobot.core.query.Request._make_call", return_value=Mock()) as mock:
            api = Mock(base_url="http://localhost:8000/api")
            app = Mock(name="test")
            test_obj = Endpoint(api, app, "test")
            mock.return_value = [{"id": "db8770c4-61e5-4999-8372-e7fa576a4f65", "name": "test"}]
            test = test_obj.update([{"id": "db8770c4-61e5-4999-8372-e7fa576a4f65", "name": "test"}])
            mock.assert_called_with(verb="patch", data=[{"id": "db8770c4-61e5-4999-8372-e7fa576a4f65", "name": "test"}])
            self.assertTrue(test)

    def test_update_with_objects(self):
        with patch("pynautobot.core.query.Request._make_call", return_value=Mock()) as mock:
            ids = ["db8770c4-61e5-4999-8372-e7fa576a4f65", "e9b5f2e0-4f20-41ad-9179-90a4987f743e"]
            api = Mock(base_url="http://localhost:8000/api")
            app = Mock(name="test")
            test_obj = Endpoint(api, app, "test")
            objects = [Record({"id": i, "name": "test_" + str(i)}, api, test_obj) for i in ids]
            for o in objects:
                o.name = "new_" + str(o.id)
            mock.return_value = [o.serialize() for o in objects]
            test = test_obj.update(objects)
            mock.assert_called_with(verb="patch", data=[{"id": i, "name": "new_" + str(i)} for i in ids])
            self.assertTrue(test)

    def test_update_with_invalid_input(self):
        api = Mock(base_url="http://localhost:8000/api")
        app = Mock(name="test")
        test_obj = Endpoint(api, app, "test")
        with self.assertRaises(ValueError) as exc:
            test_obj.update()
        self.assertEqual(
            str(exc.exception), "You must provide either a UUID and data dict or a list of objects to update"
        )

    def test_update_with_invalid_objects_type(self):
        objects = {"id": "db8770c4-61e5-4999-8372-e7fa576a4f65", "name": "test"}
        api = Mock(base_url="http://localhost:8000/api")
        app = Mock(name="test")
        test_obj = Endpoint(api, app, "test")
        with self.assertRaises(ValueError) as exc:
            test_obj.update(objects)
        self.assertEqual(str(exc.exception), "objects must be a list[dict()|Record] not <class 'dict'>")

    def test_update_with_invalid_type_in_objects(self):
        objects = [[{"id": "db8770c4-61e5-4999-8372-e7fa576a4f65", "name": "test"}]]
        api = Mock(base_url="http://localhost:8000/api")
        app = Mock(name="test")
        test_obj = Endpoint(api, app, "test")
        with self.assertRaises(ValueError) as exc:
            test_obj.update(objects)
        self.assertEqual(str(exc.exception.__cause__), "Invalid object type: <class 'list'>")

    def test_update_with_missing_id_attribute(self):
        api = Mock(base_url="http://localhost:8000/api")
        app = Mock(name="test")
        test_obj = Endpoint(api, app, "test")
        objects = [
            Record({"no_id": "db8770c4-61e5-4999-8372-e7fa576a4f65", "name": "test"}, api, test_obj),
        ]
        with self.assertRaises(ValueError) as exc:
            test_obj.update(objects)
        self.assertEqual(str(exc.exception.__cause__), "'Record' object has no attribute 'id'")

    def test_delete_with_ids(self):
        with patch("pynautobot.core.query.Request._make_call", return_value=Mock()) as mock:
            ids = ["db8770c4-61e5-4999-8372-e7fa576a4f65", "e9b5f2e0-4f20-41ad-9179-90a4987f743e"]
            mock.return_value = True
            api = Mock(base_url="http://localhost:8000/api")
            app = Mock(name="test")
            test_obj = Endpoint(api, app, "test")
            test = test_obj.delete(ids)
            mock.assert_called_with(verb="delete", data=[{"id": i} for i in ids])
            self.assertTrue(test)

    def test_delete_with_objects(self):
        with patch("pynautobot.core.query.Request._make_call", return_value=Mock()) as mock:
            ids = ["db8770c4-61e5-4999-8372-e7fa576a4f65", "e9b5f2e0-4f20-41ad-9179-90a4987f743e"]
            mock.return_value = True
            api = Mock(base_url="http://localhost:8000/api")
            app = Mock(name="test")
            test_obj = Endpoint(api, app, "test")
            objects = [Record({"id": i, "name": "test_" + str(i)}, api, test_obj) for i in ids]
            test = test_obj.delete(objects)
            mock.assert_called_with(verb="delete", data=[{"id": i} for i in ids])
            self.assertTrue(test)

    def test_delete_with_invalid_uuid(self):
        ids = ["123", "456"]
        api = Mock(base_url="http://localhost:8000/api")
        app = Mock(name="test")
        test_obj = Endpoint(api, app, "test")
        with self.assertRaises(ValueError) as exc:
            test_obj.delete(ids)
        self.assertEqual(str(exc.exception.__cause__), "badly formed hexadecimal UUID string")

    def test_delete_with_invalid_id_type(self):
        ids = [123, 456]
        api = Mock(base_url="http://localhost:8000/api")
        app = Mock(name="test")
        test_obj = Endpoint(api, app, "test")
        with self.assertRaises(ValueError) as exc:
            test_obj.delete(ids)
        self.assertEqual(str(exc.exception.__cause__), "Invalid object type: <class 'int'>")

    def test_delete_with_invalid_object(self):
        api = Mock(base_url="http://localhost:8000/api")
        app = Mock(name="test")
        test_obj = Endpoint(api, app, "test")
        objects = [
            Record({"no_id": "db8770c4-61e5-4999-8372-e7fa576a4f65", "name": "test"}, api, test_obj),
        ]
        with self.assertRaises(ValueError) as exc:
            test_obj.delete(objects)
        self.assertEqual(str(exc.exception.__cause__), "'Record' object has no attribute 'id'")


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
