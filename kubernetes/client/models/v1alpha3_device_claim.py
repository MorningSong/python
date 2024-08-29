# coding: utf-8

"""
    Kubernetes

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: release-1.31
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from kubernetes.client.configuration import Configuration


class V1alpha3DeviceClaim(object):
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
        'config': 'list[V1alpha3DeviceClaimConfiguration]',
        'constraints': 'list[V1alpha3DeviceConstraint]',
        'requests': 'list[V1alpha3DeviceRequest]'
    }

    attribute_map = {
        'config': 'config',
        'constraints': 'constraints',
        'requests': 'requests'
    }

    def __init__(self, config=None, constraints=None, requests=None, local_vars_configuration=None):  # noqa: E501
        """V1alpha3DeviceClaim - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._config = None
        self._constraints = None
        self._requests = None
        self.discriminator = None

        if config is not None:
            self.config = config
        if constraints is not None:
            self.constraints = constraints
        if requests is not None:
            self.requests = requests

    @property
    def config(self):
        """Gets the config of this V1alpha3DeviceClaim.  # noqa: E501

        This field holds configuration for multiple potential drivers which could satisfy requests in this claim. It is ignored while allocating the claim.  # noqa: E501

        :return: The config of this V1alpha3DeviceClaim.  # noqa: E501
        :rtype: list[V1alpha3DeviceClaimConfiguration]
        """
        return self._config

    @config.setter
    def config(self, config):
        """Sets the config of this V1alpha3DeviceClaim.

        This field holds configuration for multiple potential drivers which could satisfy requests in this claim. It is ignored while allocating the claim.  # noqa: E501

        :param config: The config of this V1alpha3DeviceClaim.  # noqa: E501
        :type: list[V1alpha3DeviceClaimConfiguration]
        """

        self._config = config

    @property
    def constraints(self):
        """Gets the constraints of this V1alpha3DeviceClaim.  # noqa: E501

        These constraints must be satisfied by the set of devices that get allocated for the claim.  # noqa: E501

        :return: The constraints of this V1alpha3DeviceClaim.  # noqa: E501
        :rtype: list[V1alpha3DeviceConstraint]
        """
        return self._constraints

    @constraints.setter
    def constraints(self, constraints):
        """Sets the constraints of this V1alpha3DeviceClaim.

        These constraints must be satisfied by the set of devices that get allocated for the claim.  # noqa: E501

        :param constraints: The constraints of this V1alpha3DeviceClaim.  # noqa: E501
        :type: list[V1alpha3DeviceConstraint]
        """

        self._constraints = constraints

    @property
    def requests(self):
        """Gets the requests of this V1alpha3DeviceClaim.  # noqa: E501

        Requests represent individual requests for distinct devices which must all be satisfied. If empty, nothing needs to be allocated.  # noqa: E501

        :return: The requests of this V1alpha3DeviceClaim.  # noqa: E501
        :rtype: list[V1alpha3DeviceRequest]
        """
        return self._requests

    @requests.setter
    def requests(self, requests):
        """Sets the requests of this V1alpha3DeviceClaim.

        Requests represent individual requests for distinct devices which must all be satisfied. If empty, nothing needs to be allocated.  # noqa: E501

        :param requests: The requests of this V1alpha3DeviceClaim.  # noqa: E501
        :type: list[V1alpha3DeviceRequest]
        """

        self._requests = requests

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
        if not isinstance(other, V1alpha3DeviceClaim):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1alpha3DeviceClaim):
            return True

        return self.to_dict() != other.to_dict()