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
CLI for Beagle BGP looking glass
"""

from __future__ import absolute_import
from __future__ import print_function

import os
import sys

import click
from click_default_group import DefaultGroup

from beaglecli.configuration import get_config
from beaglecli.rest_client import RESTClient
from beaglecli import commands


class DefaultAliasedGroup(DefaultGroup):
    def __init__(self, *args, **kwargs):
        super(DefaultAliasedGroup, self).__init__(*args, **kwargs)

    def get_command(self, ctx, cmd_name):
        base = super(DefaultAliasedGroup, self)

        command = base.get_command(ctx, cmd_name)
        if command is not None:
            return command
        if self.find_aliases:
            matches = [x for x in self.list_commands(ctx) if x.startswith(cmd_name)]
            if not matches:
                ctx.arg0 = cmd_name
                return base.get_command(ctx, self.default_cmd_name)
            elif len(matches) == 1:
                return base.get_command(ctx, matches[0])
            ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))

        return False


@click.group(cls=DefaultAliasedGroup)
def cli():
    ctx = click.get_current_context()

    # Read configuration
    config = {}
    for base_dir in ['.', os.path.expanduser('~'), '/etc/config/']:
        for file_name in ['.beaglecli.conf', 'beaglecli.conf']:
            config_path = os.path.join(base_dir, file_name)
            try:
                config = get_config(config_path, create_default=False)
                break
            except IOError:
                pass
            except (SyntaxError), error:
                click.echo('Invalid syntax for: %s' % config_path)
                click.echo(error)
                sys.exit()

        if config:
            break

    if not config:
        config_path = os.path.join(os.path.expanduser('~'), '.beaglecli.conf')
        config = get_config(config_path, create_default=True)

    ctx.meta['CONFIG'] = config

    ctx.meta['CLIENT'] = RESTClient(
        config['api_base'],
        config['username'],
        config['password'],
        config['verify_ssl'],
        False
    )


# ping
@cli.group(
    cls=DefaultAliasedGroup,
    default='ipv4',
    default_if_no_args=False,
    help='Runs ping command on the router matching "routers" GLOB.'
)
def ping():
    pass

# ping ipv4
@ping.command(name='ipv4')
@click.argument('address', metavar="<address>")
@click.option(
    '--router',
    nargs=1,
    type=str,
    default='*',
    metavar='GLOB',
    help='GLOB matching the routers to run the command on. Default: "*".'
)
@click.option(
    '--max-routers',
    nargs=1,
    type=int,
    default=1,
    help='Max routers to run command on. Default: 1.'
)
@click.option(
    '--vrf',
    nargs=1,
    type=str,
    default='global',
    help='VRF table. Default: global.'
)
def ping_ipv4(router, address, vrf, max_routers):
    commands.ping(router, address, vrf, max_routers, 1)


# ping ipv6
@ping.command(name='ipv6')
@click.argument(
    'address',
    metavar='<address> or "summary"'
    )
@click.option(
    '--router',
    nargs=1,
    type=str,
    default='*',
    metavar='GLOB',
    help='GLOB matching the routers to run the command on. Default: "*".'
    )
@click.option(
    '--max-routers',
    nargs=1,
    type=int,
    default=1,
    help='Max routers to run command on. Default: 1.'
)
@click.option(
    '--vrf',
    nargs=1,
    type=str,
    default='global',
    help='VRF table. Default: global.'
)
def ping_ipv6(router, address, vrf, max_routers):
    commands.ping(router, address, vrf, max_routers, 2)


# traceroute
@cli.group(
    cls=DefaultAliasedGroup,
    default='ipv4',
    default_if_no_args=False,
    help='Runs traceroute command on the router matching "routers" GLOB.'
)
def traceroute():
    pass


# traceroute ipv4
@traceroute.command(name='ipv4')
@click.argument(
    'address', metavar='<address>'
)
@click.option(
    '--router',
    nargs=1,
    type=str,
    default='*',
    metavar='GLOB',
    help='GLOB matching the routers to run the command on. Default: "*".'
)
@click.option(
    '--max-routers',
    nargs=1,
    type=int,
    default=1,
    help='Max routers to run command on. Default: 1.'
)
@click.option(
    '--vrf',
    nargs=1,
    type=str,
    default='global',
    help='VRF table. Default: global.'
)
def traceroute_ipv4(router, address, vrf, max_routers):
    commands.traceroute(router, address, vrf, max_routers, 1)


# traceroute ipv6
@traceroute.command(name='ipv6')
@click.argument(
    'address',
    metavar='<address>'
)
@click.option(
    '--router',
    nargs=1,
    type=str,
    default='*',
    metavar='GLOB',
    help='GLOB matching the routers to run the command on. Default: "*".'
)
@click.option(
    '--max-routers',
    nargs=1,
    type=int,
    default=1,
    help='Max routers to run command on. Default: 1.'
)
@click.option(
    '--vrf',
    nargs=1,
    type=str,
    default='global',
    help='VRF table. Default: global.'
)
def traceroute_ipv6(router, address, vrf, max_routers):
    commands.traceroute(router, address, vrf, max_routers, 2)


# show
@cli.group(cls=DefaultAliasedGroup)
def show():
    pass


# show routers
@show.command(
    name='routers',
    help='Show routers matching the specified GLOB.'
)
@click.option(
    '--router',
    nargs=1,
    type=str,
    default='*',
    metavar='GLOB',
    help='GLOB matching the routers to run the command on. Default: "*".'
)
def show_routers(router):
    commands.show_routers(router)


# show bgp
@show.group(
    cls=DefaultAliasedGroup,
    default='ipv4',
    default_if_no_args=False,
    help='Runs ping command on the router matching "routers" GLOB.'
)
def bgp():
    pass


# show bgp ipv4
@bgp.group(
    cls=DefaultAliasedGroup,
    default='unicast',
    default_if_no_args=False
)
def ipv4():
    pass


# show bgp ipv4 unicast
@ipv4.command(
    name='unicast',
    help='Show BGP IPv4 prefixes from the router matching GLOB.'
)
@click.argument(
    'prefix',
    metavar='<prefix>',
    default="summary"
)
@click.option(
    '--router',
    nargs=1,
    type=str,
    default='*',
    metavar='GLOB',
    help='GLOB matching the routers to run the command on. Default: "*".'
)
@click.option(
    '--max-routers',
    nargs=1,
    type=int,
    default=1,
    help='Max routers to run command on. Default: 1.'
)
@click.option(
    '--vrf',
    nargs=1,
    type=str,
    default='global',
    help='VRF table. Default: global.'
)
def show_bgp_ipv4_unicast(router, prefix, vrf, max_routers):
    commands.show_bgp_unicast(router, prefix, vrf, max_routers, 1)


# show bgp ipv6
@bgp.group(
    cls=DefaultAliasedGroup,
    default='unicast',
    default_if_no_args=False
)
def ipv6():
    pass


# show bgp ipv6 unicast
@ipv6.command(
    name='unicast',
    help='Show BGP IPv6 prefixes from the router matching GLOB.'
)
@click.argument(
    'prefix',
    metavar='<prefix>',
    default="summary"
)
@click.option(
    '--router',
    nargs=1,
    type=str,
    default='*',
    metavar='GLOB',
    help='GLOB matching the routers to run the command on. Default: "*".'
)
@click.option(
    '--max-routers',
    nargs=1,
    type=int,
    default=1,
    help='Max routers to run command on. Default: 1.'
)
@click.option(
    '--vrf',
    nargs=1,
    type=str,
    default='global',
    help='VRF table. Default: global.'
)
def show_bgp_ipv4_unicast(router, prefix, vrf, max_routers):
    commands.show_bgp_unicast(router, prefix, vrf, max_routers, 2)


def main():
    cli()


if __name__ == '__main__':
    main()
