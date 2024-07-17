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


class TestJobRun:
    """Verify we can run a job."""

    @pytest.fixture(scope="session")
    def create_git_repo(self, nb_client):
        data = {
            "name": "demorepo",
            "remote_url": "https://github.com/nautobot/demo-git-datasource",
            "branch": "main",
        }
        return nb_client.extras.git_repositories.create(**data)

    def test_job_run(self, nb_client, create_git_repo):
        job_to_run = nb_client.extras.jobs.get("Git Repository: Dry-Run")
        assert nb_client.extras.jobs.run(job_id=job_to_run.id, data={"repository": create_git_repo.id})

    def test_job_ran_successfully(self, nb_client):
        assert nb_client.extras.job_results.all()[0].status.value in ["STARTED", "SUCCESS"]
