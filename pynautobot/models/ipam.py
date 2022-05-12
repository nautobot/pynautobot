"""
(c) 2017 DigitalOcean

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

This file has been modified by NetworktoCode, LLC.
"""
from pynautobot.core.response import Record
from pynautobot.core.endpoint import DetailEndpoint


class Prefixes(Record):
    @property
    def available_ips(self):
        """ Represents the ``available-ips`` detail endpoint.

        Returns a DetailEndpoint object that is the interface for
        viewing and creating IP addresses inside a prefix.

        :returns: :py:class:`.DetailEndpoint`

        :Examples:

        >>> prefix = nb.ipam.prefixes.get(24)
        >>> prefix.available_ips.list()
        [{u'vrf': None, u'family': 4, u'address': u'10.1.1.49/30'}...]

        To create a single IP:

        >>> prefix = nb.ipam.prefixes.get(24)
        >>> prefix.available_ips.create()
        {u'status': 1, u'description': u'', u'nat_inside': None...}


        To create multiple IPs:

        >>> prefix = nb.ipam.prefixes.get(24)
        >>> create = prefix.available_ips.create([{} for i in range(2)])
        >>> len(create)
        2
        """
        # Setting to Record even though it isn't custom due to the function just returning a dictionary
        # if no custom_return is passed in
        return DetailEndpoint(self, "available-ips", custom_return=Record)

    @property
    def available_prefixes(self):
        """ Represents the ``available-prefixes`` detail endpoint.

        Returns a DetailEndpoint object that is the interface for
        viewing and creating prefixes inside a parent prefix.

        Very similar to :py:meth:`~pynautobot.ipam.Prefixes.available_ips`
        , except that dict (or list of dicts) passed to ``.create()``
        needs to have a ``prefix_length`` key/value specifed.

        :returns: :py:class:`.DetailEndpoint`

        :Examples:

        >>> prefix.available_prefixes.list()
        [{u'prefix': u'10.1.1.44/30', u'vrf': None, u'family': 4}]


        Creating a single child prefix:

        >>> prefix = nb.ipam.prefixes.get(1)
        >>> new_prefix = prefix.available_prefixes.create(
        ...    {'prefix_length': 29}
        ...)
        >>> new_prefix['prefix']
        u'10.1.1.56/29'

        """
        return DetailEndpoint(self, "available-prefixes", custom_return=Prefixes)
