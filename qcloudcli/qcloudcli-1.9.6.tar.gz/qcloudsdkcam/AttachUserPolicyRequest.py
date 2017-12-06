# -*- coding: utf-8 -*-

from qcloudsdkcore.request import Request

class AttachUserPolicyRequest(Request):

    def __init__(self):
        super(AttachUserPolicyRequest, self).__init__(
            'cam', 'qcloudcliV1', 'AttachUserPolicy', 'cam.api.qcloud.com')

    def get_uin(self):
        return self.get_params().get('uin')

    def set_uin(self, uin):
        self.add_param('uin', uin)
