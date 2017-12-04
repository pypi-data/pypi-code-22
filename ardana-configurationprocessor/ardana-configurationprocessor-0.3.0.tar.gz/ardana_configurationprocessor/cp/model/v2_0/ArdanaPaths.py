#
# (c) Copyright 2015 Hewlett Packard Enterprise Development LP
# (c) Copyright 2017 SUSE LLC
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
import os
from .CloudDescription import CloudDescription


class ArdanaPaths(object):
    @staticmethod
    def get_output_path(instructions, cloud_desc):
        cloud_name = CloudDescription.get_cloud_name(cloud_desc)
        cloud_name = cloud_name.replace(' ', '_')

        path = instructions['cloud_output_path']
        path = path.replace('@CLOUD_NAME@', cloud_name)

        return path

    @staticmethod
    def make_path(path):
        if not os.path.exists(path):
            os.makedirs(path)
