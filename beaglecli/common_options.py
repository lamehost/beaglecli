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


class Routers(object):
    def __init__(self):
        self.router = '*'
        self.max_routers = 1

def max_routers_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(Routers)
        state.max_routers = value
        return value
    return click.option(
        '-m', '--max-routers',
        nargs=1,
        type=int,
        default=1,
        help='Max routers to run command on. Default: 1.'
    )(f)

def router_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(Routers)
        state.router = value
        return value
    return click.option(
        '-r', '--router',
        nargs=1,
        type=str,
        default='*',
        metavar='GLOB',
        help='GLOB matching the routers to run the command on. Default: "*".'
    )(f)


class Vrf(Routers):
    def __init__(self):
        self.vrf = 'global'
        super(self, Vrf).__init__()

def vrf_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(Vrf)
        state.vrf = value
        return value
    return click.option(
        '-v', '--vrf',
        nargs=1,
        type=str,
        default='global',
        metavar='NAME',
        help='VRF table. Default: global.'
    )(f)


def router_options(f):
    f = max_routers_option(f)
    f = router_option(f)
    return f

def vrf_options(f):
    f = vrf_option(f)    
    f = max_routers_option(f)
    f = router_option(f)
    return f