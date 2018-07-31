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

from beaglecli.beaglecli import Commands
from beaglecli.configuration import get_config
from beaglecli.configuration import search_config
from beaglecli import clis


@click.group(name='beaglecli')
@click.pass_context
def _cli(ctx, config_path=None, router='*', max_routers=1):
    config = False

    if config_path is None:
        config = search_config('beaglecli.conf', create_default=False)

        if not config:
            config_path = os.path.join(os.path.expanduser('~'), '.beaglecli.conf')
            config = get_config(config_path, create_default=True)
    else:
        try:
            config = get_config(config_path, create_default=False)
        except (SyntaxError), error:
            click.echo('Invalid syntax for: %s' % config_path)
            click.echo(error)
            sys.exit() 



    ctx.obj = Commands(**config)


def cli():
    _cli.add_command(clis.PingCli().ping)
    _cli.add_command(clis.ShowCli().show)
    _cli.add_command(clis.TracerouteCli().traceroute)

    _cli()


def main():
    cli()


if __name__ == '__main__':
    main()
