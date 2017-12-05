# Copyright 2013: Mirantis Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_config import cfg

OPTS = {"openstack": [
    # prepoll delay, timeout, poll interval
    # "start": (0, 300, 1)
    cfg.FloatOpt("nova_server_start_prepoll_delay",
                 default=0.0,
                 deprecated_group="benchmark",
                 help="Time to sleep after start before polling for status"),
    cfg.FloatOpt("nova_server_start_timeout",
                 default=300.0,
                 deprecated_group="benchmark",
                 help="Server start timeout"),
    cfg.FloatOpt("nova_server_start_poll_interval",
                 deprecated_group="benchmark",
                 default=1.0,
                 help="Server start poll interval"),
    # "stop": (0, 300, 2)
    cfg.FloatOpt("nova_server_stop_prepoll_delay",
                 default=0.0,
                 help="Time to sleep after stop before polling for status"),
    cfg.FloatOpt("nova_server_stop_timeout",
                 default=300.0,
                 deprecated_group="benchmark",
                 help="Server stop timeout"),
    cfg.FloatOpt("nova_server_stop_poll_interval",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Server stop poll interval"),
    # "boot": (1, 300, 1)
    cfg.FloatOpt("nova_server_boot_prepoll_delay",
                 default=1.0,
                 deprecated_group="benchmark",
                 help="Time to sleep after boot before polling for status"),
    cfg.FloatOpt("nova_server_boot_timeout",
                 default=300.0,
                 deprecated_group="benchmark",
                 help="Server boot timeout"),
    cfg.FloatOpt("nova_server_boot_poll_interval",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Server boot poll interval"),
    # "delete": (2, 300, 2)
    cfg.FloatOpt("nova_server_delete_prepoll_delay",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Time to sleep after delete before polling for status"),
    cfg.FloatOpt("nova_server_delete_timeout",
                 default=300.0,
                 deprecated_group="benchmark",
                 help="Server delete timeout"),
    cfg.FloatOpt("nova_server_delete_poll_interval",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Server delete poll interval"),
    # "reboot": (2, 300, 2)
    cfg.FloatOpt("nova_server_reboot_prepoll_delay",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Time to sleep after reboot before polling for status"),
    cfg.FloatOpt("nova_server_reboot_timeout",
                 default=300.0,
                 deprecated_group="benchmark",
                 help="Server reboot timeout"),
    cfg.FloatOpt("nova_server_reboot_poll_interval",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Server reboot poll interval"),
    # "rebuild": (1, 300, 1)
    cfg.FloatOpt("nova_server_rebuild_prepoll_delay",
                 default=1.0,
                 deprecated_group="benchmark",
                 help="Time to sleep after rebuild before polling for status"),
    cfg.FloatOpt("nova_server_rebuild_timeout",
                 default=300.0,
                 deprecated_group="benchmark",
                 help="Server rebuild timeout"),
    cfg.FloatOpt("nova_server_rebuild_poll_interval",
                 default=1.0,
                 deprecated_group="benchmark",
                 help="Server rebuild poll interval"),
    # "rescue": (2, 300, 2)
    cfg.FloatOpt("nova_server_rescue_prepoll_delay",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Time to sleep after rescue before polling for status"),
    cfg.FloatOpt("nova_server_rescue_timeout",
                 default=300.0,
                 deprecated_group="benchmark",
                 help="Server rescue timeout"),
    cfg.FloatOpt("nova_server_rescue_poll_interval",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Server rescue poll interval"),
    # "unrescue": (2, 300, 2)
    cfg.FloatOpt("nova_server_unrescue_prepoll_delay",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Time to sleep after unrescue "
                      "before polling for status"),
    cfg.FloatOpt("nova_server_unrescue_timeout",
                 default=300.0,
                 deprecated_group="benchmark",
                 help="Server unrescue timeout"),
    cfg.FloatOpt("nova_server_unrescue_poll_interval",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Server unrescue poll interval"),
    # "suspend": (2, 300, 2)
    cfg.FloatOpt("nova_server_suspend_prepoll_delay",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Time to sleep after suspend before polling for status"),
    cfg.FloatOpt("nova_server_suspend_timeout",
                 default=300.0,
                 deprecated_group="benchmark",
                 help="Server suspend timeout"),
    cfg.FloatOpt("nova_server_suspend_poll_interval",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Server suspend poll interval"),
    # "resume": (2, 300, 2)
    cfg.FloatOpt("nova_server_resume_prepoll_delay",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Time to sleep after resume before polling for status"),
    cfg.FloatOpt("nova_server_resume_timeout",
                 default=300.0,
                 deprecated_group="benchmark",
                 help="Server resume timeout"),
    cfg.FloatOpt("nova_server_resume_poll_interval",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Server resume poll interval"),
    # "pause": (2, 300, 2)
    cfg.FloatOpt("nova_server_pause_prepoll_delay",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Time to sleep after pause before polling for status"),
    cfg.FloatOpt("nova_server_pause_timeout",
                 default=300.0,
                 deprecated_group="benchmark",
                 help="Server pause timeout"),
    cfg.FloatOpt("nova_server_pause_poll_interval",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Server pause poll interval"),
    # "unpause": (2, 300, 2)
    cfg.FloatOpt("nova_server_unpause_prepoll_delay",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Time to sleep after unpause before polling for status"),
    cfg.FloatOpt("nova_server_unpause_timeout",
                 default=300.0,
                 deprecated_group="benchmark",
                 help="Server unpause timeout"),
    cfg.FloatOpt("nova_server_unpause_poll_interval",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Server unpause poll interval"),
    # "shelve": (2, 300, 2)
    cfg.FloatOpt("nova_server_shelve_prepoll_delay",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Time to sleep after shelve before polling for status"),
    cfg.FloatOpt("nova_server_shelve_timeout",
                 default=300.0,
                 deprecated_group="benchmark",
                 help="Server shelve timeout"),
    cfg.FloatOpt("nova_server_shelve_poll_interval",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Server shelve poll interval"),
    # "unshelve": (2, 300, 2)
    cfg.FloatOpt("nova_server_unshelve_prepoll_delay",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Time to sleep after unshelve before "
                      "polling for status"),
    cfg.FloatOpt("nova_server_unshelve_timeout",
                 default=300.0,
                 deprecated_group="benchmark",
                 help="Server unshelve timeout"),
    cfg.FloatOpt("nova_server_unshelve_poll_interval",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Server unshelve poll interval"),
    # "image_create": (0, 300, 2)
    cfg.FloatOpt("nova_server_image_create_prepoll_delay",
                 default=0.0,
                 deprecated_group="benchmark",
                 help="Time to sleep after image_create before polling"
                      " for status"),
    cfg.FloatOpt("nova_server_image_create_timeout",
                 default=300.0,
                 deprecated_group="benchmark",
                 help="Server image_create timeout"),
    cfg.FloatOpt("nova_server_image_create_poll_interval",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Server image_create poll interval"),
    # "image_delete": (0, 300, 2)
    cfg.FloatOpt("nova_server_image_delete_prepoll_delay",
                 default=0.0,
                 deprecated_group="benchmark",
                 help="Time to sleep after image_delete before polling"
                      " for status"),
    cfg.FloatOpt("nova_server_image_delete_timeout",
                 default=300.0,
                 deprecated_group="benchmark",
                 help="Server image_delete timeout"),
    cfg.FloatOpt("nova_server_image_delete_poll_interval",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Server image_delete poll interval"),
    # "resize": (2, 400, 5)
    cfg.FloatOpt("nova_server_resize_prepoll_delay",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Time to sleep after resize before polling for status"),
    cfg.FloatOpt("nova_server_resize_timeout",
                 default=400.0,
                 deprecated_group="benchmark",
                 help="Server resize timeout"),
    cfg.FloatOpt("nova_server_resize_poll_interval",
                 default=5.0,
                 deprecated_group="benchmark",
                 help="Server resize poll interval"),
    # "resize_confirm": (0, 200, 2)
    cfg.FloatOpt("nova_server_resize_confirm_prepoll_delay",
                 default=0.0,
                 deprecated_group="benchmark",
                 help="Time to sleep after resize_confirm before polling"
                      " for status"),
    cfg.FloatOpt("nova_server_resize_confirm_timeout",
                 default=200.0,
                 deprecated_group="benchmark",
                 help="Server resize_confirm timeout"),
    cfg.FloatOpt("nova_server_resize_confirm_poll_interval",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Server resize_confirm poll interval"),
    # "resize_revert": (0, 200, 2)
    cfg.FloatOpt("nova_server_resize_revert_prepoll_delay",
                 default=0.0,
                 deprecated_group="benchmark",
                 help="Time to sleep after resize_revert before polling"
                      " for status"),
    cfg.FloatOpt("nova_server_resize_revert_timeout",
                 default=200.0,
                 deprecated_group="benchmark",
                 help="Server resize_revert timeout"),
    cfg.FloatOpt("nova_server_resize_revert_poll_interval",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Server resize_revert poll interval"),
    # "live_migrate": (1, 400, 2)
    cfg.FloatOpt("nova_server_live_migrate_prepoll_delay",
                 default=1.0,
                 deprecated_group="benchmark",
                 help="Time to sleep after live_migrate before polling"
                      " for status"),
    cfg.FloatOpt("nova_server_live_migrate_timeout",
                 default=400.0,
                 deprecated_group="benchmark",
                 help="Server live_migrate timeout"),
    cfg.FloatOpt("nova_server_live_migrate_poll_interval",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Server live_migrate poll interval"),
    # "migrate": (1, 400, 2)
    cfg.FloatOpt("nova_server_migrate_prepoll_delay",
                 default=1.0,
                 deprecated_group="benchmark",
                 help="Time to sleep after migrate before polling for status"),
    cfg.FloatOpt("nova_server_migrate_timeout",
                 default=400.0,
                 deprecated_group="benchmark",
                 help="Server migrate timeout"),
    cfg.FloatOpt("nova_server_migrate_poll_interval",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Server migrate poll interval"),
    # "detach":
    cfg.FloatOpt("nova_detach_volume_timeout",
                 default=200.0,
                 deprecated_group="benchmark",
                 help="Nova volume detach timeout"),
    cfg.FloatOpt("nova_detach_volume_poll_interval",
                 default=2.0,
                 deprecated_group="benchmark",
                 help="Nova volume detach poll interval")
]}
