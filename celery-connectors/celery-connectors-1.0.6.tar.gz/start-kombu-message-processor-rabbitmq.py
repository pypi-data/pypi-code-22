#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import logging
from celery_connectors.utils import ev
from celery_connectors.logging.setup_logging import setup_logging
from celery_connectors.message_processor import MessageProcessor

setup_logging()

name = "msg-proc"

log = logging.getLogger("loader-name")

log.info("Start - {}".format(name))

# want to change where you're subscribing vs publishing?
sub_ssl_options = {}
sub_auth_url = ev("SUB_BROKER_URL", "amqp://rabbitmq:rabbitmq@localhost:5672//")
pub_ssl_options = {}
pub_auth_url = ev("PUB_BROKER_URL", "redis://localhost:6379/0")

# start the message processor
msg_proc = MessageProcessor(name=name,
                            sub_auth_url=sub_auth_url,
                            sub_ssl_options=sub_ssl_options,
                            pub_auth_url=pub_auth_url,
                            pub_ssl_options=pub_ssl_options)

# configure where this is consuming:
queue = "user.events.conversions"

# Relay Publish Hook - sending to Redis
# where is it sending handled messages using a publish-hook or auto-caching:
exchange = "reporting.accounts"
routing_key = "reporting.accounts"

# set up the controls and long-term connection attributes
seconds_to_consume = 10.0
heartbeat = 60
serializer = "application/json"
pub_serializer = "json"
expiration = None
consume_forever = True

# start consuming
msg_proc.consume_queue(queue=queue,
                       heartbeat=heartbeat,
                       expiration=expiration,
                       sub_serializer=serializer,
                       pub_serializer=pub_serializer,
                       seconds_to_consume=seconds_to_consume,
                       forever=consume_forever,
                       # Optional: if you're chaining a publish hook to another system
                       exchange=exchange,
                       # Optional: if you're chaining a publish hook to another system
                       routing_key=routing_key)

log.info("End - {}".format(name))
