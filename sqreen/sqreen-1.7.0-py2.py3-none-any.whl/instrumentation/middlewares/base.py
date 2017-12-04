# -*- coding: utf-8 -*-
# Copyright (c) 2016, 2017 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Base middleware for peripheric frameworks integration
"""
import logging

from ...constants import ACTIONS
from ...exceptions import AttackBlocked
from ...rules import record_observation
from ..hook_point import (execute_failing_callbacks, execute_post_callbacks,
                          execute_pre_callbacks)

LOGGER = logging.getLogger(__name__)


class BaseMiddleware(object):
    """ Middleware base class for frameworks middleware hooks
    """

    def __init__(self, strategy, observation_queue, queue):
        LOGGER.debug("%s for %s", self.__class__.__name__, strategy)
        self.strategy = strategy
        self.observation_queue = observation_queue
        self.queue = queue

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, repr(self.strategy))

    def execute_pre_callbacks(self, args=None, record_500=False):
        """ Execute pre callbacks with None original and args. Only process
        valid action, in this context it's raising.
        """
        action = execute_pre_callbacks(self.strategy.strategy_key, self.strategy,
                                       original=None, args=args)

        action_status = action.get('status')

        if not action_status:
            return

        if action_status == ACTIONS['RAISE']:
            LOGGER.debug("Callback %s detected an attack", action.get('rule_name'))

            # With some frameworks (Flask, Pyramid), raising an exception here
            # will not result in failing callbacks being executed
            if record_500 is True:
                record_observation(self.strategy.observation_queue, self.strategy.queue,
                                   'http_code', '500', 1)

            raise AttackBlocked(action.get('rule_name'))
        else:
            LOGGER.warning("Invalid action status %s", action_status)

    def execute_post_callbacks(self, response, args=None, record_500=False):
        """ Execute post callbacks with None original and args. Only process
        valid action, in this context it's raising.
        """
        action = execute_post_callbacks(self.strategy.strategy_key, self.strategy,
                                        original=None, result=response, args=args)

        action_status = action.get('status')

        if not action_status:
            return response

        if action_status == ACTIONS['RAISE']:
            LOGGER.debug("Callback %s detected an attack", action.get('rule_name'))

            # With some frameworks (Flask, Pyramid), raising an exception here
            # will not result in failing callbacks being executed
            if record_500 is True:
                record_observation(self.strategy.observation_queue, self.strategy.queue,
                                   'http_code', '500', 1)

            raise AttackBlocked(action.get('rule_name'))
        else:
            LOGGER.warning("Invalid action status %s", action_status)

        return response

    def execute_failing_callbacks(self, exception, args=None):
        """ Execute failing callbacks with None original and args. Only process
        valid action, in this context it's None.
        """
        action = execute_failing_callbacks(self.strategy.strategy_key, self.strategy,
                                           original=None, exc_infos=exception, args=args)

        action_status = action.get('status')

        if not action_status:
            return

        LOGGER.warning("Invalid action status %s", action_status)
