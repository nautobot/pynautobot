"""Overrides for models in the Virtualization app.

Classes, attributes and methods only need to be defined here if they need to
override the default behavior.
"""

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

from pynautobot.core.response import JsonField, Record


class VirtualMachines(Record):
    """Virtual Machines."""

    config_context = JsonField
