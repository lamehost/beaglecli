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
"""

from __future__ import absolute_import
from __future__ import print_function

import click

from beaglecli.common_options import vrf_options

class TracerouteCli(object):
    def __init__(self):
        self.traceroute.add_command(TracerouteIpv4Cli().traceroute, name='ipv4')
        self.traceroute.add_command(TracerouteIpv6Cli().traceroute, name='ipv6')

    @click.group(
        help='Runs traceroute command on routers'
    )
    @click.pass_context
    def traceroute(ctx):
        pass

class TracerouteIpv4Cli(object):
    @click.command(
        help='Address Family IPv4 unicast'
    )
    @click.pass_obj
    @vrf_options
    @click.argument(
        'address',
        metavar="<address>"
    )
    def traceroute(commands, router, max_routers, address, vrf):
        commands.traceroute(router, address, vrf, max_routers, 1)

class TracerouteIpv6Cli(object):
    @click.command(
        help='Address Family IPv6 unicast'
    )
    @click.pass_obj
    @vrf_options
    @click.argument(
        'address',
        metavar="<address>"
    )
    def traceroute(commands, router, max_routers, address, vrf):
        commands.traceroute(router, address, vrf, max_routers, 2)