# coding: utf-8

"""
    Kubernetes

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: v1.7.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import os
import sys
import unittest

import kubernetes.client
from kubernetes.client.rest import ApiException
from kubernetes.client.models.v1_network_policy_port import V1NetworkPolicyPort


class TestV1NetworkPolicyPort(unittest.TestCase):
    """ V1NetworkPolicyPort unit test stubs """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testV1NetworkPolicyPort(self):
        """
        Test V1NetworkPolicyPort
        """
        model = kubernetes.client.models.v1_network_policy_port.V1NetworkPolicyPort()


if __name__ == '__main__':
    unittest.main()