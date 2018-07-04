# -*- coding: utf-8 -*-

# MIT License

# Copyright (c) 2018, Marco Marzetti <marco@lamehost.it>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
REST client library for Beagle BGP looking glass
"""

import logging
import fnmatch

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client

import requests
import urllib3


class RESTClient(object):
    def __init__(self, base_url, username=None, password=None, verify_ssl=False, debug=False):
        if debug:
            http_client.HTTPConnection.debuglevel = 1
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True
        else:
            # Hide library warnings (on by default)
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.base_url = base_url
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl

    def _get_url(self, path, params=None):
        params = params or []
        url = urljoin(self.base_url, path)
        try:
            request = requests.get(
                url,
                auth=(self.username, self.password),
                verify=self.verify_ssl,
                params=params,
                headers={
                    'Content-type': 'application/json',
                    'Accept': 'application/json'
                }
            )
        except requests.exceptions.ConnectionError:
            raise RuntimeError(u'(╯°□°）╯︵ ┻━┻ Unable to connect to the server.')

        if request.status_code not in [200, 201]:
            raise RuntimeError(u'(╯°□°）╯︵ ┻━┻ Server returned error state %d' % request.status_code)

        result = request.json()

        return result

    @staticmethod
    def _to_cli_output(data):
        try:
            output = data['data']['output']
        except KeyError:
            raise RuntimeError('Unable to parse query result.')

        # Transform most common HTML tags
        # TODO, find a library for that
        output = output.replace('<b>', '\033[1m')
        output = output.replace('</b>', '\033[0m')

        # data['data']['output'] = output

        return output

    def get_routers(self, wildcard="*"):
        data = self._get_url('routers/')
        try:
            routers = [_ for _ in data['data']['routers'] if fnmatch.fnmatch(_['name'], wildcard)]
        except StopIteration:
            raise RuntimeError('Unable to find a router whose name matches with "%s"' % wildcard)

        return routers

    def ping(self, address, router_id=1, afi=1, vrf='global'):
        output = self._get_url(
            'ping/%s' % address,
            {
                'afi': afi,
                'safi': 1,
                'format': 'text/plain',
                'vrf': vrf,
                'id': router_id
            }
        )
        output = self._to_cli_output(output)

        return output

    def show_bgp_unicast(self, prefix, router_id=1, afi=1, vrf='global'):
        output = self._get_url(
            'show/bgp/%s' % prefix,
            {
                'afi': afi,
                'safi': 1,
                'format': 'text/plain',
                'vrf': vrf,
                'id': router_id
            }
        )
        output = self._to_cli_output(output)

        return output

    def show_routers(self, wildcard="*"):
        routers = self.get_routers(wildcard)

        try:
            return '\n'.join(sorted([_['name'] for _ in routers]))
        except KeyError:
            raise RuntimeError('Unable to parse query result.')

    def traceroute(self, address, router_id=1, afi=1, vrf='global'):
        output = self._get_url(
            'traceroute/%s' % address,
            {
                'afi': afi,
                'safi': 1,
                'format': 'text/plain',
                'vrf': vrf,
                'id': router_id
            }
        )
        output = self._to_cli_output(output)

        return output
