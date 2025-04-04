"""Extras Object"""

# (c) 2017 DigitalOcean
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This file has been modified by NetworktoCode, LLC.

from pynautobot.core.endpoint import JobsEndpoint, DetailEndpoint, GraphqlEndpoint
from pynautobot.core.response import JsonField, Record


class ConfigContexts(Record):
    """ConfigContext object."""

    data = JsonField


class ObjectChanges(Record):
    """ObjectChanges."""

    object_data = JsonField

    def __str__(self):
        return self.request_id


class CustomFieldChoices(Record):
    """CustomFieldChoices."""

    def __str__(self):
        return self.value


class JobResults(Record):
    """JobResults."""

    data = JsonField


class Jobs(Record):
    """Jobs."""

    def run(self, **kwargs):
        """Run a job from within a job instance."""
        return JobsEndpoint(self.api, self.api.extras, "jobs").run(class_path=self.id, **kwargs)


class GraphqlQueries(Record):
    """GraphqlQueries."""

    def run(self, *args, **kwargs):
        """Run a graphql query from a saved graphql instance."""
        return GraphqlEndpoint(self.api, self.api.extras, "graphql_queries").run(self.id, *args, **kwargs)


class DynamicGroups(Record):
    """DynamicGroups."""

    filter = JsonField

    def __str__(self):
        parent_record_string = super().__str__()
        return parent_record_string or str(self.id)

    @property
    def members(self):
        """Represents the ``members`` detail endpoint.

        Returns a list of DetailEndpoint objects that are
        related to the dynamic group

        :returns: :py:class:`.DetailEndpoint`

        :Examples:

        Dynamic group of devices:

        >>> group = nb.extras.dynamic_groups.get("device-group")
        >>> group.members.list()
        [<pynautobot.models.extras.DynamicGroups ('testswitch') at 0x7efee4037e80>...]

        Dynamic group of IPs:

        >>> group = nb.extras.dynamic_groups.get("ip-group")
        >>> group.members.list()
        [<pynautobot.models.extras.DynamicGroups ('192.168.10.200/32') at 0x7f3e6a980040>...]
        """
        return DetailEndpoint(self, "members", custom_return=DynamicGroups)


class Secrets(Record):
    """Secrets."""

    parameters = JsonField
