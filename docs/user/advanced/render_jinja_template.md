# Rendering a Jinja Template

Nautobot can render a Jinja template server-side and return the result.
pynautobot exposes this through the `core` app, which is available on the
`~pynautobot.core.api.Api`{.interpreted-text role="py:class"} object upon
initialization. The setup is the same as detailed in
`Creating a pynautobot Instance`{.interpreted-text role="ref"}.

```python
import os

from pynautobot import api

url = "https://demo.nautobot.com"

# Retrieve token from system environment variable
# token = os.environ["NAUTOBOT_TOKEN"]
token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
nautobot = api(url=url, token=token)
```

## Rendering a Template

The `~pynautobot.core.app.CoreApp.render_jinja_template`{.interpreted-text
role="py:meth"} method accepts the template to render as `template_code`
and an optional `context` dictionary of variables. It returns the raw
response from Nautobot as a dictionary.

```python
>>> result = nautobot.core.render_jinja_template(
...     template_code="Hello {{ name }}",
...     context={"name": "world"},
... )
>>> result["rendered_template"]
'Hello world'
```

The returned dictionary contains the following keys:

- `rendered_template`: The rendered output as a single string.
- `rendered_template_lines`: The rendered output split into a list of lines.
- `template_code`: The template that was submitted.
- `context`: The context that was submitted.

```python
>>> result
{
    'rendered_template': 'Hello world',
    'rendered_template_lines': ['Hello world'],
    'template_code': 'Hello {{ name }}',
    'context': {'name': 'world'}
}
```

## Rendering Without Context

The `context` argument is optional and defaults to an empty dictionary,
which is useful for templates that do not require any variables.

```python
>>> result = nautobot.core.render_jinja_template(
...     template_code="{{ 2 + 2 }}",
... )
>>> result["rendered_template"]
'4'
```

!!! Tip

    Nautobot's [Jinja2 template rendering](https://docs.nautobot.com/projects/core/en/stable/user-guide/platform-functionality/template-filters/) documentation lists the filters and functions available within templates.
