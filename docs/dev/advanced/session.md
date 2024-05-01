# Modifying the HTTP Session

Pynautobot uses a
[requests.Session](https://requests.readthedocs.io/en/stable/user/advanced/#session-objects)
object to make HTTP requests to Nautobot. This is stored as
`~pynautobot.core.api.Api.http_response`{.interpreted-text
role="py:attr"}, and can be updated as supported by `requests`. A few
examples are provided below:

-   `Headers`{.interpreted-text role="ref"}
-   `SSL Verification`{.interpreted-text role="ref"}
-   `Timeouts`{.interpreted-text role="ref"}

## Headers

Adding or updating headers is done by updating the `headers` dictionary
on the `http_response` object. The example below shows how to update a
Token if it has been cycled.

```python
import os
from pynautobot import api

nautobot = api(
    url='http://localhost:8000',
    token=os.environ["NAUTOBOT_TOKEN"]
)
new_token = f"Token {os.environ['NEW_NAUTOBOT_TOKEN']}"

# Update Session object with new header
nautobot.http_session.headers["Authorization"] = new_token
```

## SSL Verification

The below example shows how to disable SSL verification.

```python
import os
from pynautobot import api
nautobot = api(
    url='https://localhost:8000',
    token=os.environ["NAUTOBOT_TOKEN"],
    verify=False
)
```

## Timeouts

Changing the timeout behavior is done with [Transport
Adapters](https://requests.readthedocs.io/en/stable/user/advanced/#transport-adapters).

```python
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
```
