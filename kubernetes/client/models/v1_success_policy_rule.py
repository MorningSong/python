# coding: utf-8

"""
    Kubernetes

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: release-1.33
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from kubernetes.client.configuration import Configuration


class V1SuccessPolicyRule(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'succeeded_count': 'int',
        'succeeded_indexes': 'str'
    }

    attribute_map = {
        'succeeded_count': 'succeededCount',
        'succeeded_indexes': 'succeededIndexes'
    }

    def __init__(self, succeeded_count=None, succeeded_indexes=None, local_vars_configuration=None):  # noqa: E501
        """V1SuccessPolicyRule - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._succeeded_count = None
        self._succeeded_indexes = None
        self.discriminator = None

        if succeeded_count is not None:
            self.succeeded_count = succeeded_count
        if succeeded_indexes is not None:
            self.succeeded_indexes = succeeded_indexes

    @property
    def succeeded_count(self):
        """Gets the succeeded_count of this V1SuccessPolicyRule.  # noqa: E501

        succeededCount specifies the minimal required size of the actual set of the succeeded indexes for the Job. When succeededCount is used along with succeededIndexes, the check is constrained only to the set of indexes specified by succeededIndexes. For example, given that succeededIndexes is \"1-4\", succeededCount is \"3\", and completed indexes are \"1\", \"3\", and \"5\", the Job isn't declared as succeeded because only \"1\" and \"3\" indexes are considered in that rules. When this field is null, this doesn't default to any value and is never evaluated at any time. When specified it needs to be a positive integer.  # noqa: E501

        :return: The succeeded_count of this V1SuccessPolicyRule.  # noqa: E501
        :rtype: int
        """
        return self._succeeded_count

    @succeeded_count.setter
    def succeeded_count(self, succeeded_count):
        """Sets the succeeded_count of this V1SuccessPolicyRule.

        succeededCount specifies the minimal required size of the actual set of the succeeded indexes for the Job. When succeededCount is used along with succeededIndexes, the check is constrained only to the set of indexes specified by succeededIndexes. For example, given that succeededIndexes is \"1-4\", succeededCount is \"3\", and completed indexes are \"1\", \"3\", and \"5\", the Job isn't declared as succeeded because only \"1\" and \"3\" indexes are considered in that rules. When this field is null, this doesn't default to any value and is never evaluated at any time. When specified it needs to be a positive integer.  # noqa: E501

        :param succeeded_count: The succeeded_count of this V1SuccessPolicyRule.  # noqa: E501
        :type: int
        """

        self._succeeded_count = succeeded_count

    @property
    def succeeded_indexes(self):
        """Gets the succeeded_indexes of this V1SuccessPolicyRule.  # noqa: E501

        succeededIndexes specifies the set of indexes which need to be contained in the actual set of the succeeded indexes for the Job. The list of indexes must be within 0 to \".spec.completions-1\" and must not contain duplicates. At least one element is required. The indexes are represented as intervals separated by commas. The intervals can be a decimal integer or a pair of decimal integers separated by a hyphen. The number are listed in represented by the first and last element of the series, separated by a hyphen. For example, if the completed indexes are 1, 3, 4, 5 and 7, they are represented as \"1,3-5,7\". When this field is null, this field doesn't default to any value and is never evaluated at any time.  # noqa: E501

        :return: The succeeded_indexes of this V1SuccessPolicyRule.  # noqa: E501
        :rtype: str
        """
        return self._succeeded_indexes

    @succeeded_indexes.setter
    def succeeded_indexes(self, succeeded_indexes):
        """Sets the succeeded_indexes of this V1SuccessPolicyRule.

        succeededIndexes specifies the set of indexes which need to be contained in the actual set of the succeeded indexes for the Job. The list of indexes must be within 0 to \".spec.completions-1\" and must not contain duplicates. At least one element is required. The indexes are represented as intervals separated by commas. The intervals can be a decimal integer or a pair of decimal integers separated by a hyphen. The number are listed in represented by the first and last element of the series, separated by a hyphen. For example, if the completed indexes are 1, 3, 4, 5 and 7, they are represented as \"1,3-5,7\". When this field is null, this field doesn't default to any value and is never evaluated at any time.  # noqa: E501

        :param succeeded_indexes: The succeeded_indexes of this V1SuccessPolicyRule.  # noqa: E501
        :type: str
        """

        self._succeeded_indexes = succeeded_indexes

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, V1SuccessPolicyRule):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1SuccessPolicyRule):
            return True

        return self.to_dict() != other.to_dict()
