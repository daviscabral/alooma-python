import os
import unittest

from nose.tools import assert_equals, assert_true
from alooma import Client


class TestAlooma(unittest.TestCase):

    def setUp(self):
        """
         **** **** **** ******** **** **** ****
         **** Getting an Alooma API Object ****
         **** **** **** ******** **** **** ****
        """
        ## Using Environment Variables ##
        ALOOMA_USERNAME = os.environ['ALOOMA_EMAIL']
        ALOOMA_PASSWORD = os.environ['ALOOMA_PASSWORD']
        ACCOUNT_NAME = os.environ['ALOOMA_DEPLOYMENT']

        ## We will use this api object throughout the documentation ##
        self.api = Client(ALOOMA_USERNAME, ALOOMA_PASSWORD,
                                 account_name=ACCOUNT_NAME)
        assert_equals(self.api.account_name, ACCOUNT_NAME)

    # region Deployment

    def test_get_deployment_info(self):
        deployment = self.api.get_deployment_info()['deploymentName']
        test = deployment.startswith(self.api.account_name)

        assert_true(test)

    # endregion

    # region Inputs

    def test_get_inputs(self):
        inputs = self.api.get_inputs()
        assert_true(isinstance(inputs, list))

    def test_get_input(self):
        inputs = self.api.get_inputs()
        input_name = inputs[0]['name']

        input_data = self.api.get_input(input_name)
        assert_equals(input_data.keys(), ["job", "tasks"])

    # endregion

    # region Consolidation

    def test_get_scheduled_queries(self):
        cons = self.api.get_scheduled_queries()
        assert_true(isinstance(cons, dict))

    # endregion
