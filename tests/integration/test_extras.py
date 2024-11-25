import pytest


class TestCustomField:
    """Verify we can create, custom field, and custom field choices."""

    @pytest.fixture(scope="session")
    def create_custom_field(self, nb_client):
        data = {
            "label": "test_cf",
            "key": "test_cf",
            "content_types": ["dcim.device"],
            "type": "select",
            "weight": 100,
            "filter_logic": "loose",
        }
        return nb_client.extras.custom_fields.create(**data)

    @pytest.fixture(scope="session")
    def create_custom_field_choices(self, nb_client, create_custom_field):
        data = {
            "value": "A",
            "custom_field": create_custom_field["id"],
            "weight": 100,
        }
        return nb_client.extras.custom_field_choices.create(**data)

    def test_custom_field(self, create_custom_field):
        assert create_custom_field["label"] == "test_cf"

    def test_custom_field_choice(self, create_custom_field_choices):
        assert create_custom_field_choices["value"] == "A"

    def test_custom_field_choice_to_cf(self, create_custom_field_choices, create_custom_field):
        assert create_custom_field_choices["custom_field"]["id"] == create_custom_field["id"]


class TestNotes:
    """Verify we can list and create notes as detailed endpoints."""

    @pytest.fixture(scope="session")
    def create_test_object(self, nb_client):
        return nb_client.dcim.manufacturers.create(name="test_manufacturer")

    def test_create_object_note(self, create_test_object):
        test_obj = create_test_object
        assert len(test_obj.notes.list()) == 0
        test_obj.notes.create({"note": "foo bar"})
        assert len(test_obj.notes.list()) == 1

    def test_get_object_note(self, create_test_object):
        test_obj = create_test_object
        assert test_obj.notes.list()[0].note == "foo bar"

    def test_get_note_on_invalid_object(self, nb_client):
        test_obj = nb_client.extras.content_types.get(model="manufacturer")
        with pytest.raises(Exception, match="The requested url: .* could not be found."):
            test_obj.notes.list()


class TestGraphqlQueries:
    """Verify we can create and run a saved graphql query"""

    @pytest.fixture(scope="session")
    def create_graphql_query(self, nb_client):
        query = """
            query Example($devicename: [String] = "server.networktocode.com"){
                devices(name: $devicename) {
                    name
                    serial
                }
            }
        """
        data = {"name": "foobar", "query": query}
        return nb_client.extras.graphql_queries.create(**data)

    def test_graphql_query_run(self, create_graphql_query):
        query = create_graphql_query
        data = query.run()
        assert len(data.get("data", {}).get("devices")) == 1
        assert data.get("data", {}).get("devices")[0].get("name") == "server.networktocode.com"

    def test_graphql_query_run_with_variable(self, create_graphql_query):
        query = create_graphql_query
        data = query.run(variables={"devicename": "dev-1"})
        assert len(data.get("data", {}).get("devices")) == 1
        assert data.get("data", {}).get("devices")[0].get("name") == "dev-1"


class TestDynamicGroup:
    """Dynamic group tests."""

    def test_dynamic_group_filter_field(self, nb_client):
        """Verify we can create a dynamic group and return the filter field."""

        # Define filter field
        obj_filter = {"q": "foobar"}

        # Create dynamic group
        nb_client.extras.dynamic_groups.create(
            [
                {
                    "name": "TestDynamicGroup",
                    "content_type": "dcim.device",
                    "group_type": "dynamic-filter",
                    "filter": obj_filter,
                }
            ]
        )

        # Get dynamic group
        dynamic_group = nb_client.extras.dynamic_groups.get(name="TestDynamicGroup")

        # Assert filter field is returned
        assert dynamic_group.filter == obj_filter
