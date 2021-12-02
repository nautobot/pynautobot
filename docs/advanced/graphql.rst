Gathering Data from GraphQL Endpoint
====================================

Using pynautobot to make GraphQL queries against Nautobot has the same
initial setup as detailed in :ref:`Creating a pynautobot Instance`. 

.. code-block:: python

    import os

    from pynautobot import api

    url = "https://demo.nautobot.com"

    # Retrieve token from system environment variable
    # token = os.environ["NAUTOBOT_TOKEN"]
    token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    nautobot = api(url=url, token=token)

An instance of :py:class:`~pynautobot.core.graphql.GraphQLQuery` is assigned
to the above ``nautobot`` object upon initialization.
The :py:meth:`~pynautobot.core.graphql.GraphQLQuery.query` method is used to
perform queries against Nautobot's GraphQL endpoint.


Making a GraphQL Query
----------------------

The :py:meth:`~pynautobot.core.graphql.GraphQLQuery.query` method requires
that a query string is passed into it.
The method retuns a :py:class:`~pynautobot.core.graphql.GraphQLRecord` object
as discussed in :ref:`The GraphQLRecord Object` section.

This example demonstrates how to fetch the `id`, `name`, and `region name` for all *Sites*.

.. code-block:: python

    >>> # Build a query string
    >>> query = """
    ... query {
    ...   sites {
    ...     id
    ...     name
    ...     region {
    ...       name
    ...     }
    ...   }
    ... }
    ... """

    >>> # Make a graphql query
    >>> graphql_response = nautobot.graphql.query(query=query)

    >>> # Show that a GraphQLRecord is returned
    GraphQLRecord(json={'data': {'sites': [{'id': '2cfbc91e-361f-4129-9db6-bc21a6f88d38', 'name': 'ams', ..., status_code=200)

The next example performs the same query, but restricts it to only the ``den`` site.

.. code-block:: python

    >>> # Build a query string restricting only to den site
    >>> query = """
    ... query {
    ...   sites (name: "den") {
    ...     id
    ...     name
    ...     region {
    ...       name
    ...     }
    ...   }
    ... }
    ... """
    >>> graphql_response = nautobot.graphql.query(query=query)
    >>> graphql_response
    GraphQLRecord(json={'data': {'sites': [{'id': '45399b54-47f9-4eec-86e3-47352e103b1b', 'name': 'den', 'region': {'name': 'United States'}}]}}, status_code=200)

.. tip::

   Nautobot's `GraphQL documentation <https://nautobot.readthedocs.io/en/latest/additional-features/graphql/>`_ 
   provides a summary of making queries.

   Nautobot's browsable API also provides a `graphiql` interface to aid in developing query strings at `/graphql/` 


Making a GraphQL Query with Variables
-------------------------------------

The :py:meth:`~pynautobot.core.graphql.GraphQLQuery.query` method supports using variables in the query string by passing in an optional ``variables`` argument.
This argument is a dictionary, with the `key` being the variable name, and the `value` being the value to use for the variable in the query string.
This example is the same as the previous one, except the site name is now derived using variables.

.. code-block:: python

    >>> # Create a variables dictionary
    >>> variables = {"site_name": "den"}

    >>> # Create a query string that takes variables
    >>> query = """
    ... query ($site_name:String!) {
    ...   sites (name: $site_name) {
    ...     id
    ...     name
    ...     region {
    ...       name
    ...     }
    ...   }
    ... }
    ... """

    >>> # Use the query method with variables
    >>> graphql_response = nautobot.graphql.query(query=query, variables=variables)
    >>> graphql_response
    GraphQLRecord(json={'data': {'sites': [{'id': '45399b54-47f9-4eec-86e3-47352e103b1b', 'name': 'den', 'region': {'name': 'United States'}}]}}, status_code=200)


The GraphQLRecord Object
------------------------

The :py:class:`~pynautobot.core.graphql.GraphQLRecord` object that is returned from making a query provides a ``json`` attribute with the response from the API.
The ``json`` attribute is a dictionary of the results from making the query.
This example shows accessing data from the previous query.

.. code-block:: python

    >>> variables = {"site_name": "den"}
    >>> query = """
    ... query ($site_name:String!) {
    ...   sites (name: $site_name) {
    ...     id
    ...     name
    ...     region {
    ...       name
    ...     }
    ...   }
    ... }
    ... """
    >>> graphql_response = nautobot.graphql.query(query=query, variables=variables)
    >>> graphql_response.json
    {
      'data': {
        'sites': [
          {
            'id': '45399b54-47f9-4eec-86e3-47352e103b1b',
            'name': 'den',
            'region': {
              'name': 'United States'
            }
          }
        ]
      }
    }
    >>> # Get the name of the first site
    >>> graphql_response.json["data"]["sites"][0]["name"]
    'den'
