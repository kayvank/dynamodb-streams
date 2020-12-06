"""Dynamodb stream processor

Process dynamodb streams filtering for inserts and modify payloads
"""

import json
import math
import time
import boto3

try:
    import unzip_requirements
except ImportError:
    pass
from dynamodb_json import json_util as ddbjson

delivery_stream_name = "core-dynamodb-v1"
firehose_client = boto3.client("firehose", region_name="us-west-2")


def compose(f, g):
    return lambda x: f(g(x))


def newImage(record, event_name):
    """Return paylods of interest

function does:
    1- strips dynamodb `json-typed-tags`
    2- return `NewImage`, a dynamdb term for the actual user-data
    """
    record_data = record["dynamodb"]["NewImage"]
    record_data.update({"timestamp": math.floor(time.time() * 1000)})
    record_data.update({"dynamodbEvent": event_name})
    return json.dumps(record_data)


def generate(event):
    """ record generator

    generator strips the dyamodb `type-tags`
    """
    for record in event["Records"]:
        yield ddbjson.loads(record)


def inserted(record):
    """ process dynamo insert events
    """
    return f"{newImage(record, 'INSERT')}\n"


def modified(record):
    """ process dynamo modify events
    """
    return f"{newImage(record, 'MODIFY')}\n"


def removed(record):
    """ process dynamo remove events
    """
    return f"{newImage(record, 'REMOVE')}\n"


def event_router(dynamo_event):
    """ event router returns to the appropirate function
    """
    routes = {"INSERT": inserted, "MODIFY": modified, "REMOVE": removed}
    return routes[dynamo_event]


def as_kcl_record(payload):
    """ string to kinesis record
    """
    return {"Data": payload, "PartitionKey": str(hash(payload))}


def as_firehose_record(payload):
    """ string to kinesis record
    """
    return {"Data": payload.encode()}


def ddb_to_firehose(record):
    """process dynamodb stream record to kinesis record
    """
    f = event_router(dynamo_event=record["eventName"])
    process_function = compose(as_firehose_record, f)
    return process_function(record)


def dispatcher(event):
    """ dispatches the dynamodb events to the corresponding processor
    """

    def batch_events(kcls):
        for record in generate(event):
            kcl_record = ddb_to_firehose(record)
            kcls.append(kcl_record)
            return kcls

    return batch_events([])


def firehose_writer(records):
    """ writes to aws firehose
    """
    firehose_client.put_record_batch(
        DeliveryStreamName=delivery_stream_name, Records=records
    )


def processor():
    """Process a batch of dynamodb records

    returns a function that transforms and writes dynamodb records to firehose
    """

    f = compose(firehose_writer, dispatcher)
    return f
