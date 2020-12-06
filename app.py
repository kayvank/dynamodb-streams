""" AWS lambda function for dynamodb streams

Archive dynamodb streams to kinesis -> s3
"""
import logging
from common import processor


log_format = (
    "%(asctime)s::%(levelname)s::%(name)s::" "%(filename)s::%(lineno)d::%(message)s"
)
logging.basicConfig(level="INFO", format=log_format)
# Lazy-eval the dynamodb attribute (boto3 is dynamic!)


def main(event, ctx):
    """ main entrace to the lambda function
    """
    try:
        f = processor()
        f(event)
    except Exception as error:
        logging.error(f"Error. Exception <<{error}>> was thrown")
        return "Error"
    return f"records processed: {len(event)}"
