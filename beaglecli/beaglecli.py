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
TODO
"""

from __future__ import absolute_import
from __future__ import print_function

import sys

from beaglecli.rest_client import RESTClient


class Commands(object):
    def __init__(self, api_base, username, password, verify_ssl, debug):
        self.client = RESTClient(
            api_base,
            username,
            password,
            verify_ssl,
            debug
        )

    def print_result(self, result):
        # TODO: Find a library for this
        try:
            _  = result['body']['data']['output']
            _ = _.replace('<b>', '\033[1m')
            _ = _.replace('</b>', '\033[0m')
            result['body']['data']['output'] = _
        except KeyError:
            pass

        if result['status'] in [200, 202]:
            print('\033[1mStatus\033[0m: %(status)s' % result['body'])
            print('\033[1mTimestamp\033[0m: %(performed_at)s' % result['body']['data'])
            print('\n\033[1mOutput\033[0m:\n%(output)s' % result['body']['data'])
        elif result['status'] in [400, 404]:
            print('Server didn\'t like the argument. Please try with something meaningful.')
            sys.exit(1)
        elif result['status'] in [429]:
            print(u'(╯°□°）╯︵ ┻━┻ Hey, what are you up to? Slow down!')
            sys.exit(1)
        elif result['status'] in [502]:
            print('\033[1mStatus\033[0m: %(status)s' % result['body'])
            print('\n\033[1mOutput\033[0m:\n%(message)s\n' % result['body']['data'])
        elif result['status'] in [504]:
            print(u'(╯°□°）╯︵ ┻━┻ Command timed out on the router')
        else:
            print(u'(╯°□°）╯︵ ┻━┻ Something went wrong with the server')

        print('')


    def ping(self, router, address, vrf, max_routers, afi):
        try:
            routers = self.show_routers(router, max_routers, True)
        except RuntimeError as error:
            print(unicode(error))
            sys.exit(1)

        for _router in routers:
            print('\033[1mRouter\033[0m: %s' % _router['name'])
            try:
                result = self.client.ping(address, _router['id'], afi, vrf)
            except RuntimeError as error:
                print(unicode(error))
                sys.exit(1)

            self.print_result(result)

    def show_bgp_unicast(self, router, prefix, vrf, max_routers, afi):
        try:
            routers = self.show_routers(router, max_routers, True)
        except RuntimeError as error:
            print(unicode(error))
            sys.exit(1)

        for _router in routers:
            print('\033[1mRouter\033[0m: %s' % _router['name'])
            try:
                result = self.client.show_bgp_unicast(prefix, _router['id'], afi, vrf)
            except RuntimeError as error:
                print(unicode(error))
                sys.exit(1)

            self.print_result(result)

    def show_routers(self, router, max_routers, compact=False):
        try:
            routers = self.client.get_routers(router)
        except RuntimeError as error:
            print(unicode(error))
            sys.exit(1)

        if max_routers > 0:
            limit = len(routers) if len(routers) < max_routers else max_routers
            routers = sorted(routers[:limit], key=lambda _: _['name'])        

        if compact:
            router_names = ', '.join([_['name'] for _ in routers])
            print('\033[1mSelected routers\033[0m: %s\n' % router_names)
        else:
            router_names = '\n'.join([_['name'] for _ in routers])
            print(router_names)

        return routers

    def traceroute(self, router, address, vrf, max_routers, afi):
        try:
            routers = self.show_routers(router, max_routers, True)
        except RuntimeError as error:
            print(unicode(error))
            sys.exit(1)

        for _router in routers:
            print('\033[1mRouter\033[0m: %s' % _router['name'])
            try:
                result = self.client.traceroute(address, _router['id'], afi, vrf)
            except RuntimeError as error:
                print(unicode(error))
                sys.exit(1)

            self.print_result(result)
