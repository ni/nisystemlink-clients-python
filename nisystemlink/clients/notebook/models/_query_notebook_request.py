from typing import Optional

from nisystemlink.clients.core._uplink._with_paging import WithPaging


class QueryNotebookRequest(WithPaging):
    """Model for a query notebooks request."""

    filter: Optional[str] = None
    """
    The filter criteria for notebook, consisting of a string of queries composed using AND/OR operators.
    String values need to be enclosed in double quotes. Parenthesis can be used within the filter
    to better define the order of operations.
    Filter syntax: '[property name][operator][operand] and [property name][operator][operand]' Operators:

      Equals operator '='. Example: 'x = y'
      Not equal operator '!='. Example: 'x != y'
      Greater than operator '>'. Example: 'x > y'
      Greater than or equal operator '>='. Example: 'x >= y'
      Less than operator '<'. Example: 'x < y'
      Less than or equal operator '<='. Example: 'x <= y'
      Logical AND operator 'and'. Example: 'x and y'
      Logical OR operator 'or'. Example: 'x or y'
      Starts with operator '.StartsWith()', used to check whether a string starts with another string.
      Example: 'x.StartsWith(y)'
      Does not start with operator '!.StartsWith()', used to check whether a string does not start with another string.
      Example: '!x.StartsWith(y)'
      String null or empty 'string.IsNullOrEmpty()', used to check whether a string is null or empty.
      Example: 'string.IsNullOrEmpty(x)'
      String is not null or empty '!string.IsNullOrEmpty()', used to check whether a string is not null or empty.
      Example: '!string.IsNullOrEmpty(x)'
        Valid notebook properties that can be used in the filter:
      id
      name
      properties.interface
      workspace
    """

    take: Optional[int] = None
    """The maximum number of notebooks to return."""
