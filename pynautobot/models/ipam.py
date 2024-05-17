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

from pynautobot.core.response import Record
from pynautobot.core.endpoint import DetailEndpoint


class IpAddresses(Record):
    def __str__(self):
        parent_record_string = super().__str__()
        return parent_record_string or str(self.address)


class Prefixes(Record):
    def __str__(self):
        parent_record_string = super().__str__()
        return parent_record_string or str(self.prefix)

    @property
    def available_ips(self):
        """
        Represents the ``available-ips`` detail endpoint.

        Returns a DetailEndpoint object that is the interface for
        viewing and creating IP addresses inside a prefix.

        Returns:
            DetailEndpoint: The detail endpoint interface for available IPs.

        Examples:
            List available IPs:

            >>> prefix = nb.ipam.prefixes.get(prefix="10.0.192.0/18")
            >>> prefix.available_ips.list()
            [<pynautobot.models.ipam.IpAddresses ('10.0.192.1/18') at 0x103cb59d0>, <pynautobot.models.ipam.IpAddresses ('10.0.192.2/18') at 0x103cefb90>,...]

            To create a single IP:

            >>> prefix = nb.ipam.prefixes.get(prefix="10.0.192.0/18")
            >>> prefix.available_ips.create()
            {u'status': 1, u'description': u'', u'nat_inside': None...}

            To create multiple IPs:

            >>> prefix = nb.ipam.prefixes.get(prefix="10.0.192.0/18")
            >>> create = prefix.available_ips.create([{} for i in range(2)])
            >>> len(create)
            2
        """

        return DetailEndpoint(self, "available-ips", custom_return=IpAddresses)

    @property
    def available_prefixes(self):
        """
        Represents the ``available-prefixes`` detail endpoint.

        Returns a DetailEndpoint object that is the interface for
        viewing and creating prefixes inside a parent prefix.

        Very similar to :py:meth:`~pynautobot.ipam.Prefixes.available_ips`,
        except that the dict (or list of dicts) passed to ``.create()`` 
        needs to have a ``prefix_length`` key/value specified.

        Returns:
            DetailEndpoint: The detail endpoint interface for available prefixes.

        Examples:
            List available prefixes:

            >>> prefix.available_prefixes.list()
            [{u'prefix': u'10.1.1.44/30', u'vrf': None, u'family': 4}]

            Creating a single child prefix:

            >>> prefix = nb.ipam.prefixes.get(prefix="10.0.192.0/18")
            >>> new_prefix = prefix.available_prefixes.create({'prefix_length': 29, 'status': 'Active'})
            >>> new_prefix.prefix
            '10.0.192.40/29'
        """
        return DetailEndpoint(self, "available-prefixes", custom_return=Prefixes)
