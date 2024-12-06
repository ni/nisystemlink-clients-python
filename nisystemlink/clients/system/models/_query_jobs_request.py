from typing import Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class QueryJobsRequest(JsonModel):
    """Model for query job request."""

    skip: int
    """The number of jobs to skip."""

    take: Optional[int] = None
    """The number of jobs to return. The maximum value is 1000."""

    filter: Optional[str] = None
    """
    Gets or sets the filter criteria for jobs or systems. Consists of a string of queries composed using
    AND/OR operators.String values and date strings need to be enclosed in double quotes. Parenthesis
    can be used around filters to better define the order of operations.
    Filter syntax: '[property name][operator][operand] and [property name][operator][operand]'

    Operators:
        Equals operator '='. Example: 'x = y'
        Not equal operator '!='. Example: 'x != y'
        Greater than operator '>'. Example: 'x > y'
        Greater than or equal operator '>='. Example: 'x >= y'
        Less than operator '<'. Example: 'x < y'
        Less than or equal operator '<='. Example: 'x <= y'
        Logical AND operator 'and' or '&&'. Example: 'x and y'
        Logical OR operator 'or' or '||'. Example: 'x or y'
        Contains operator '.Contains()', used to check if a list contains an element.
        Example: 'x.Contains(y)'
        Not Contains operator '!.Contains()', used to check if a list does not contain an element.
        Example: '!x.Contains(y)'

    Valid job properties that can be used in the filter:
        jid : String representing the ID of the job.
        id : String representing the ID of the system.
        createdTimestamp: ISO-8601 formatted timestamp string specifying the date when the job
          was created.
        lastUpdatedTimestamp: ISO-8601 formatted timestamp string specifying the last date the
          job was updated.
        dispatchedTimestamp: ISO-8601 formatted timestamp string specifying the date when the
          job was actually sent to the system.
        state: String representing the state of the job.
        metadata: Object containg the the metadata of job. Example: metadata.queued
        config.user: String representing the user who created the job.
        config.tgt: List of strings representing the targeted systems. Example: config.tgt.Contains("id")
        config.fun: List of strings representing the functions to be executed within the job.
          Example: config.fun.Contains("nisysmgmt.set_blackout")
        config.arg: An array of arrays of variable type elements that are arguments to the function specified
          by the "fun" property. Example: config.arg[0].Contains("test")
        result.return: An array of objects representing return values for each executed function.
          Example: result.return[0].Contains("Success")
        result.retcode: An array of integers representing code values for each executed function.
          Example: result.retcode
        result.success: An array of booleans representing success values for each executed function.
          Example: result.success.Contains(false)
    """

    projection: Optional[str] = None
    """
    Gets or sets specifies the projection for resources. Use this field to receive specific properties of the model.

    Examples: - 'new(id,jid,state)' - 'new(id,jid,config.user as user)' -
    'new(id,jid,state,lastUpdatedTimestamp,metadata.queued as queued)'
    """

    order_by: Optional[str] = None
    """
    The order in which the jobs return.

    Example: createdTimestamp descending
    """
