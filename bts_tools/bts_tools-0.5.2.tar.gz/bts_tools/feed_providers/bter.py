#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# bts_tools - Tools to easily manage the bitshares client
# Copyright (c) 2017 Nicolas Wack <wackou@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


from . import FeedPrice, check_online_status, check_market
import requests
import logging

log = logging.getLogger(__name__)

NAME = 'Bter'
AVAILABLE_MARKETS = [('BTS', 'BTC'), ('BTS', 'CNY'), ('BTC', 'CNY')]
TIMEOUT = 60

@check_online_status
@check_market
def get(cur, base):
    log.debug('checking feeds for %s/%s at %s' % (cur, base, NAME))
    r = requests.get('http://data.bter.com/api/1/ticker/%s_%s' % (cur.lower(), base.lower()),
                     timeout=TIMEOUT).json()
    return FeedPrice(float(r['last']) or ((float(r['sell']) + float(r['buy'])) / 2),
                     cur, base,
                     volume=float(r['vol_%s' % cur.lower()]),
                     provider=NAME)
