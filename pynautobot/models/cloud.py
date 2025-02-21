"""Cloud Object"""

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

from pynautobot.core.response import Record, JsonField


class CloudResourceTypes(Record):
    """
    CloudResourceType object
    """

    config_schema = JsonField


class CloudServices(Record):
    """
    CloudService object
    """

    extra_config = JsonField
    cloud_resource_type = CloudResourceTypes


class CloudNetworks(Record):
    """
    CloudNetwork object
    """

    extra_config = JsonField
    cloud_resource_type = CloudResourceTypes
