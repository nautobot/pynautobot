Modifying the HTTP Session
==========================

Pynautobot uses a `requests.Session <https://requests.readthedocs.io/en/stable/user/advanced/#session-objects>`_
object to make HTTP requests to Nautobot.
This is stored as :py:attr:`~pynautobot.core.api.Api.http_response`, and can be updated as supported by ``requests``.
A few examples are provided below:

* :ref:`Headers`
* :ref:`SSL Verification`
* :ref:`Timeouts`

Headers
-------

HTTP headers can be modified using the ``headers`` argument, which is a dictionary of all key/value pairs. The example below shows how to set a custom user agent.

.. code-block:: python

    from pynautobot import api

    headers = {
        "User-Agent": "my-user-agent"
    }

    nautobot = api(
        url='http://localhost:8000',
        token=os.environ["NAUTOBOT_TOKEN"],
        headers=headers
    )

SSL Verification
----------------

The below example shows how to disable SSL verification.

.. code-block:: python

    import os
    from pynautobot import api
    nautobot = api(
        url='https://localhost:8000',
        token=os.environ["NAUTOBOT_TOKEN"],
        verify=False
    )

Timeouts
--------

Changing the timeout behavior is done with `Transport Adapters <https://requests.readthedocs.io/en/stable/user/advanced/#transport-adapters>`_.

.. code-block:: python

    import os
    from requests.adapters import HTTPAdapter
    from pynautobot import api

    class TimeoutHTTPAdapter(HTTPAdapter):
        def __init__(self, *args, **kwargs):
            self.timeout = kwargs.get("timeout", 5)
            super().__init__(*args, **kwargs)

        def send(self, request, **kwargs):
            kwargs['timeout'] = self.timeout
            return super().send(request, **kwargs)

    nautobot = api(
        url='http://localhost:8000',
        token='d6f4e314a5b5fefd164995169f28ae32d987704f'
    )
    nautobot.http_session.mount(nautobot.base_url, TimeoutHTTPAdapter())
