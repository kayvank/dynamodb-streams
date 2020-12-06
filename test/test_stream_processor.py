"""unit test
"""
import unittest
import json
import logging
from dynamodb_json import json_util as ddbjson
import common as sp
import app as m


class TestStramProcessor(unittest.TestCase):
    """ test class
    """

    def setUp(self):
        with open("./test/test-data.txt") as fp:
            self.lines = fp.readlines()

    def test_inserted(self):
        """insert spec:
        given insert record
        display transformed record to be archived
        verify lastname
        """
        dynamo_record = json.loads(self.lines[1])["Records"][0]
        result = sp.inserted(ddbjson.loads(dynamo_record))
        logging.info(result)
        self.assertEqual(json.loads(result)["lastName"], "Ice")

    def test_dispatcher(self):
        """dispatch spec:
        given insert record
        route to correct handerl
        verify  string is returned

        """
        dynamo_record = json.loads(self.lines[1])
        result = sp.dispatcher(dynamo_record)
        logging.info(result)
        self.assertTrue(len(result) == 1)

    # def test_handler_function(self):
    #     """ poor man integration test
    #     given complete dynamodb record
    #     verify firehose insert occured
    #     """
    #     event = json.loads(self.lines[1])
    #     result = m.main(event, "test-context")
    #     logging.info(result)
    #     self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
