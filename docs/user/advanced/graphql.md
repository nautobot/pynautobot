# Gathering Data from GraphQL Endpoint

Using pynautobot to make GraphQL queries against Nautobot has the same
initial setup as detailed in
[Creating a pynautobot Instance](../basic/api.md).

```python
import os

from pynautobot import api

url = "https://demo.nautobot.com"

# Retrieve token from system environment variable
# token = os.environ["NAUTOBOT_TOKEN"]
token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
nautobot = api(url=url, token=token)
```

An instance of [`GraphQLQuery`][pynautobot.core.graphql.GraphQLQuery] is assigned to the above `nautobot` object upon
initialization. The
[`query()`][pynautobot.core.graphql.GraphQLQuery.query] method is used to perform queries against Nautobot's
GraphQL endpoint.

## Making a GraphQL Query

The [`query()`][pynautobot.core.graphql.GraphQLQuery.query] method requires that a query string is passed into it.
The method retuns a
[`GraphQLRecord`][pynautobot.core.graphql.GraphQLRecord] object as discussed in
[The GraphQLRecord Object](#the-graphqlrecord-object) section.

This example demonstrates how to fetch the `id`,
`name`, and `parent name` for all *Locations*.

```python
>>> # Build a query string
>>> query = """
... query {
...   locations {
...     id
...     name
...     parent {
...       name
...     }
...   }
... }
... """
>>>
>>> # Make a graphql query
>>> graphql_response = nautobot.graphql.query(query=query)
>>>
>>> # Show that a GraphQLRecord is returned
>>> graphql_response
GraphQLRecord(json={'data': {'locations': [{'id': ..., status_code=200)
```

The next example performs the same query, but restricts it to only the
`HQ` location.

```python
>>> # Build a query string restricting only to HQ location
>>> query = """
... query {
...   locations (name: "HQ") {
...     id
...     name
...     parent {
...       name
...     }
...   }
... }
... """
>>> graphql_response = nautobot.graphql.query(query=query)
>>> graphql_response
GraphQLRecord(json={'data': {'locations': [{'id': ..., 'name': 'HQ', 'parent': {'name': 'US'}}]}}, status_code=200)
```

!!! Tip

  Nautobot's [GraphQL documentation](https://docs.nautobot.com/projects/core/en/stable/user-guide/platform-functionality/graphql/) provides a summary of making queries.
  Nautobot's browsable API also provides a `graphiql` interface to aid in developing query strings at `/graphql/`


## Making a GraphQL Query with Variables

The [`query()`][pynautobot.core.graphql.GraphQLQuery.query] method supports using variables in the query string by
passing in an optional `variables` argument. This argument is a
dictionary, with the `key` being the variable name, and the
`value` being the value to use for the variable in the query
string. This example is the same as the previous one, except the
location name is now derived using variables.

```python
>>> # Create a variables dictionary
>>> variables = {"location_name": "HQ"}
>>>
>>> # Create a query string that takes variables
>>> query = """
... query ($location_name:String!) {
...   locations (name: [$location_name]) {
...     id
...     name
...     parent {
...       name
...     }
...   }
... }
... """
>>>
>>> # Use the query method with variables
>>> graphql_response = nautobot.graphql.query(query=query, variables=variables)
>>> graphql_response
GraphQLRecord(json={'data': {'locations': [{'id': ..., 'name': 'HQ', 'parent': {'name': 'US'}}]}}, status_code=200)
```

## Making a GraphQL Query with a Saved Query

Nautobot supports saving your graphql queries and executing them later.
Here is an example of saving a query using pynautobot.

```python
>>> query = """
... query ($location_name:String!) {
...   locations (name: [$location_name]) {
...     id
...     name
...     parent {
...       name
...     }
...   }
... }
... """
>>> data = {"name": "Foobar", "query": query}
>>> nautobot.extras.graphql_queries.create(**data)
```

Now that we have a query saved with the name `Foobar`, we can execute it using pynautobot.

```python
>>> # Create a variables dictionary
>>> variables = {"location_name": "HQ"}
>>>
>>> # Get the query object that was created
>>> query_object = nautobot.extras.graphql_queries.get("Foobar")
>>>
>>> # Call the run method to execute query
>>> query_object.run()
>>>
>>> # To execute a query with variables
>>> query_object.run(variables=variables)
>>>
>>> # To execute a query with custom payload
>>> query_object.run({"variables": variables, "foo": "bar"})
```

## The GraphQLRecord Object

The [`GraphQLRecord`][pynautobot.core.graphql.GraphQLRecord] object that is returned from making a query provides a
`json` attribute with the response from the API. The `json` attribute is
a dictionary of the results from making the query. This example shows
accessing data from the previous query.

```python
>>> variables = {"location_name": "HQ"}
>>> query = """
... query ($location_name:String!) {
...   locations (name: [$location_name]) {
...     id
...     name
...     parent {
...       name
...     }
...   }
... }
... """
>>> graphql_response = nautobot.graphql.query(query=query, variables=variables)
>>> graphql_response.json
{
  'data': {
    'locations': [
      {
        'id': ...,
        'name': 'HQ',
        'parent': {
          'name': 'US'
        }
      }
    ]
  }
}
>>> # Get the name of the first location
>>> graphql_response.json["data"]["locations"][0]["name"]
'HQ'
```

## Saving Changes

The Nautobot GraphQL API is currently read-only. To make updates to
objects, see:

-   [Updating objects without loading data](update.md#updating-objects-without-loading-data)
-   [`update()`][pynautobot.core.endpoint.Endpoint.update]
