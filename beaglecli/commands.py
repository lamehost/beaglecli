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

import click


def ping(router, address, vrf, max_routers, afi):
    ctx = click.get_current_context()
    try:
        routers = ctx.meta['CLIENT'].get_routers(router)
    except RuntimeError, error:
        click.echo(error)
        sys.exit(1)

    limit = len(routers) if len(routers) < max_routers else max_routers
    click.echo(
        'Routers: %s\n' % ', '.join(sorted([_['name'] for _ in routers[:limit]]))
    )

    for _router in routers[:limit]:
        click.echo('Running query on router: %s' % _router['name'])
        try:
            output = ctx.meta['CLIENT'].ping(address, _router['id'], afi, vrf)
        except RuntimeError, error:
            output = error

        click.echo('%s\n' % output)

def show_bgp_unicast(router, prefix, vrf, max_routers, afi):
    ctx = click.get_current_context()
    try:
        routers = ctx.meta['CLIENT'].get_routers(router)
    except RuntimeError, error:
        click.echo(error)
        sys.exit(1)

    limit = len(routers) if len(routers) < max_routers else max_routers
    click.echo(
        'Routers: %s\n' % ', '.join(sorted([_['name'] for _ in routers[:limit]]))
    )

    for _router in routers[:limit]:
        click.echo('Running query on router: %s' % _router['name'])
        try:
            output = ctx.meta['CLIENT'].show_bgp_unicast(prefix, _router['id'], afi, vrf)
        except RuntimeError, error:
            output = error

        click.echo('%s\n' % output)

def show_routers(router):
    ctx = click.get_current_context()
    try:
        output = ctx.meta['CLIENT'].show_routers(router)
    except RuntimeError, error:
        click.echo(error)
        sys.exit(1)

    click.echo(output)

def traceroute(router, address, vrf, max_routers, afi):
    ctx = click.get_current_context()
    try:
        routers = ctx.meta['CLIENT'].get_routers(router)
    except RuntimeError, error:
        click.echo(error)
        sys.exit(1)

    limit = len(routers) if len(routers) < max_routers else max_routers
    click.echo(
        'Routers: %s\n' % ', '.join(sorted([_['name'] for _ in routers[:limit]]))
    )

    for _router in routers[:limit]:
        click.echo('Running query on router: %s' % _router['name'])
        try:
            output = ctx.meta['CLIENT'].traceroute(address, _router['id'], afi, vrf)
        except RuntimeError, error:
            output = error

        click.echo('%s\n' % output)
