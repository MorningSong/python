# coding: utf-8


import unittest

import kubernetes
from kubernetes.client.configuration import Configuration
import urllib3


class TestApiClient(unittest.TestCase):
    def test_rest_proxycare(self):

        pool = { 'proxy': urllib3.ProxyManager, 'direct': urllib3.PoolManager }

        for dst, proxy, no_proxy, expected_pool in [
             ( 'http://kube.local/',           None,                       None,                           pool['direct']),
             ( 'http://kube.local/',          'http://proxy.local:8080/',  None,                           pool['proxy']),
             ( 'http://127.0.0.1:8080/',      'http://proxy.local:8080/',  'localhost,127.0.0.0/8,.local', pool['direct']),
             ( 'http://kube.local/',          'http://proxy.local:8080/',  'localhost,127.0.0.0/8,.local', pool['direct']),
             ( 'http://kube.others.com:1234/','http://proxy.local:8080/',  'localhost,127.0.0.0/8,.local', pool['proxy']),
             ( 'http://kube.others.com:1234/','http://proxy.local:8080/',  '*',                            pool['direct']),
        ]:
            # setup input
            config = Configuration(proxy='', no_proxy='')
            setattr(config, 'host', dst)
            if proxy is not None:
                setattr(config, 'proxy', proxy)
            if no_proxy is not None:
                setattr(config, 'no_proxy', no_proxy)
            # setup done

            # test
            client = kubernetes.client.ApiClient(configuration=config)
            self.assertEqual( expected_pool, type(client.rest_client.pool_manager) )


class TestConfigurationAuthSettings(unittest.TestCase):
    """Regression tests for Configuration.auth_settings() bearer-token lookup.

    Prior to v36.0.0 the generated client stored the bearer token under
    ``api_key['authorization']`` (e.g. set by ``load_kube_config`` or by
    user code directly). v36.0.0 switched the lookup to
    ``api_key['BearerToken']`` without a fallback, which silently dropped
    the Authorization header from every outgoing request and caused 401
    Unauthorized against any cluster relying on bearer tokens.
    See: https://github.com/kubernetes-client/python/issues/2595
    """

    def _bearer_value(self, config):
        settings = config.auth_settings()
        self.assertIn('BearerToken', settings)
        return settings['BearerToken']['value']

    def test_auth_settings_with_bearer_token_key(self):
        """The new key 'BearerToken' continues to work."""
        config = Configuration()
        config.api_key['BearerToken'] = 'Bearer abc123'
        self.assertEqual(self._bearer_value(config), 'Bearer abc123')

    def test_auth_settings_with_authorization_key(self):
        """Legacy key 'authorization' is honored as a fallback."""
        config = Configuration()
        config.api_key['authorization'] = 'Bearer abc123'
        self.assertEqual(self._bearer_value(config), 'Bearer abc123')

    def test_auth_settings_bearer_token_takes_precedence(self):
        """When both keys are set, 'BearerToken' wins."""
        config = Configuration()
        config.api_key['BearerToken'] = 'Bearer new'
        config.api_key['authorization'] = 'Bearer old'
        self.assertEqual(self._bearer_value(config), 'Bearer new')

    def test_auth_settings_with_no_token(self):
        """No api_key entry yields an empty auth dict."""
        config = Configuration()
        self.assertEqual(config.auth_settings(), {})

    def test_auth_settings_with_authorization_key_and_prefix(self):
        """Legacy callers that split the token and prefix across
        api_key['authorization'] and api_key_prefix['authorization'] (rather
        than embedding "Bearer " in the token itself) must still get the
        prefix applied. https://github.com/kubernetes-client/python/issues/2592
        """
        config = Configuration()
        config.api_key['authorization'] = 'abc123'
        config.api_key_prefix['authorization'] = 'Bearer'
        self.assertEqual(self._bearer_value(config), 'Bearer abc123')
