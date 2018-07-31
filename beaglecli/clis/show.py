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

from beaglecli.common_options import router_options
from beaglecli.common_options import vrf_options


class ShowCli(object):
    def __init__(self):
        self.show.add_command(ShowRoutersCli().show, name='routers')
        self.show.add_command(ShowBgpCli().bgp, name='bgp')

    @click.group(
        help='Runs show commands on routers'
    )
    @click.pass_context
    def show(ctx):
        pass

class ShowRoutersCli(object):
    @click.command(
        help='Show list of routers'
    )
    @click.pass_obj
    @click.option(
        '-r', '--router',
        nargs=1,
        type=str,
        default='*',
        metavar='GLOB',
        help='GLOB matching the routers to run the command on. Default: "*".'
    )
    @click.option(
        '-m', '--max-routers',
        nargs=1,
        type=int,
        default=0,
        help='Max routers to run command on. Default: No limit.'
    )
    def show(commands, router, max_routers):
        commands.show_routers(router, max_routers)

class ShowBgpCli(object):
    def __init__(self):
        self.bgp.add_command(ShowBgpIpv4Cli().ipv4, name='ipv4')
        self.bgp.add_command(ShowBgpIpv6Cli().ipv6, name='ipv6')

    @click.group(
        help='Show list of BGP commands'
    )
    @click.pass_obj
    @vrf_options
    def bgp(*args, **kwargs):
        pass

class ShowBgpIpv4Cli(object):
    def __init__(self):
        self.ipv4.add_command(
            ShowBgpIpv4UnicastCli().unicast, name='unicast'
        )

    @click.group(
        help='Address Family IPv4'
    )
    @click.pass_obj
    @vrf_options
    def ipv4(*args, **kwargs):
        pass

class ShowBgpIpv6Cli(object):
    def __init__(self):
        self.ipv6.add_command(
            ShowBgpIpv6UnicastCli().unicast, name='unicast'
        )

    @click.group(
        help='Address Family IPv6'
    )
    @click.pass_obj
    @vrf_options
    def ipv6(*args, **kwargs):
        pass

class ShowBgpIpv4UnicastCli(object):
    @click.command(
        help='Address Family IPv4 unicast'
    )
    @click.pass_obj
    @vrf_options
    @click.argument(
        'address',
        metavar="<address>"
    )
    def unicast(commands, router, max_routers, address, vrf):
        commands.show_bgp_unicast(router, address, vrf, max_routers, 1)

class ShowBgpIpv6UnicastCli(object):
    @click.command(
        help='Address Family IPv6 unicast'
    )
    @click.pass_obj
    @vrf_options
    @click.argument(
        'address',
        metavar="<address>"
    )
    def unicast(commands, router, max_routers, address, vrf):
        commands.show_bgp_unicast(router, address, vrf, max_routers, 2)