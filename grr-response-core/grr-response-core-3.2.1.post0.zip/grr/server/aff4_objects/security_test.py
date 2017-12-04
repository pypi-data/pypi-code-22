#!/usr/bin/env python
"""Tests for grr.server.aff4_objects.security."""

from grr import config
from grr.lib import flags
from grr.lib import rdfvalue
from grr.lib import utils
from grr.server import access_control
from grr.server import aff4
from grr.server.aff4_objects import security
from grr.server.aff4_objects import users
from grr.test_lib import acl_test_lib
from grr.test_lib import test_lib


class ApprovalTest(test_lib.GRRBaseTest, acl_test_lib.AclTestMixin):
  """Test for Approval."""

  def setUp(self):
    super(ApprovalTest, self).setUp()
    self.client_id = self.SetupClients(1)[0]
    self.approval_expiration = rdfvalue.Duration(
        "%ds" % config.CONFIG["ACL.token_expiry"])

  def testGetApprovalForObjectRaisesWhenTokenIsNone(self):
    with self.assertRaisesRegexp(access_control.UnauthorizedAccess,
                                 "No token given"):
      security.Approval.GetApprovalForObject(self.client_id, token=None)

  def testGetApprovalForObjectRaisesIfNoApprovals(self):
    with self.assertRaisesRegexp(access_control.UnauthorizedAccess,
                                 "No approval found"):
      security.Approval.GetApprovalForObject(self.client_id, token=self.token)

  def testGetApprovalForObjectRaisesIfSingleAvailableApprovalExpired(self):
    self.RequestAndGrantClientApproval(self.client_id, token=self.token)

    # Make sure approval is expired by the time we call GetApprovalForObject.
    now = rdfvalue.RDFDatetime.Now()
    with test_lib.FakeTime(now + self.approval_expiration +
                           rdfvalue.Duration("1s")):
      with self.assertRaisesRegexp(access_control.UnauthorizedAccess,
                                   "Requires 2 approvers for access."):
        security.Approval.GetApprovalForObject(self.client_id, token=self.token)

  def testGetApprovalForObjectRaisesIfAllAvailableApprovalsExpired(self):
    # Set up 2 approvals with different reasons.
    token1 = access_control.ACLToken(
        username=self.token.username, reason="reason1")
    self.RequestAndGrantClientApproval(self.client_id, token=token1)

    token2 = access_control.ACLToken(
        username=self.token.username, reason="reason2")
    self.RequestAndGrantClientApproval(self.client_id, token=token2)

    # Make sure that approvals are expired by the time we call
    # GetApprovalForObject.
    now = rdfvalue.RDFDatetime.Now()
    with test_lib.FakeTime(now + self.approval_expiration +
                           rdfvalue.Duration("1s")):
      with self.assertRaisesRegexp(access_control.UnauthorizedAccess,
                                   "Requires 2 approvers for access."):
        security.Approval.GetApprovalForObject(self.client_id, token=self.token)

  def testGetApprovalForObjectReturnsSingleAvailableApproval(self):
    self.RequestAndGrantClientApproval(self.client_id, token=self.token)

    approved_token = security.Approval.GetApprovalForObject(
        self.client_id, token=self.token)
    self.assertEqual(approved_token.reason, self.token.reason)

  def testGetApprovalForObjectReturnsNonExpiredApprovalFromMany(self):
    token1 = access_control.ACLToken(
        username=self.token.username, reason="reason1")
    self.RequestAndGrantClientApproval(self.client_id, token=token1)

    now = rdfvalue.RDFDatetime.Now()
    with test_lib.FakeTime(now + self.approval_expiration, increment=1e-6):
      token2 = access_control.ACLToken(
          username=self.token.username, reason="reason2")
      self.RequestAndGrantClientApproval(self.client_id, token=token2)

    # Make sure only the first approval is expired by the time
    # GetApprovalForObject is called.
    with test_lib.FakeTime(now + self.approval_expiration +
                           rdfvalue.Duration("1h")):
      approved_token = security.Approval.GetApprovalForObject(
          self.client_id, token=self.token)
      self.assertEqual(approved_token.reason, token2.reason)

  def testGetApprovalForObjectRaisesIfApprovalsAreOfWrongType(self):
    # Create AFF4Volume object where Approval is expected to be.
    approval_urn = aff4.ROOT_URN.Add("ACL").Add(self.client_id.Path()).Add(
        self.token.username).Add(utils.EncodeReasonString(self.token.reason))
    with aff4.FACTORY.Create(
        approval_urn, aff4.AFF4Volume, token=self.token) as _:
      pass

    with self.assertRaisesRegexp(access_control.UnauthorizedAccess,
                                 "Couldn't open any of 1 approvals"):
      security.Approval.GetApprovalForObject(self.client_id, token=self.token)

  def testApprovalDoesNotCreateUser(self):

    username = "doesnotexist"

    user = aff4.FACTORY.Open("aff4:/users/%s" % username, token=self.token)
    self.assertFalse(isinstance(user, users.GRRUser))

    security.ClientApprovalRequestor(
        subject_urn=self.client_id,
        reason=self.token.reason,
        approver=username,
        token=self.token).Request()

    user = aff4.FACTORY.Open("aff4:/users/%s" % username, token=self.token)
    self.assertFalse(isinstance(user, users.GRRUser))


class ClientApprovalTest(test_lib.GRRBaseTest):
  """Test for client approvals."""

  def testCreatingApprovalCreatesSymlink(self):
    client_id = self.SetupClients(1)[0]

    security.ClientApprovalRequestor(
        subject_urn=client_id,
        reason=self.token.reason,
        approver="approver",
        token=self.token).Request()

    approval_id = list(
        aff4.FACTORY.ListChildren(
            "aff4:/users/test/approvals/client/C.1000000000000000"))[
                0].Basename()
    self.assertTrue(approval_id.startswith("approval:"))

    fd = aff4.FACTORY.Open(
        "aff4:/users/test/approvals/client/C.1000000000000000/%s" % approval_id,
        follow_symlinks=False,
        mode="r",
        token=self.token)
    self.assertEqual(fd.Get(fd.Schema.TYPE), "AFF4Symlink")
    self.assertEqual(
        fd.Get(fd.Schema.SYMLINK_TARGET),
        "aff4:/ACL/C.1000000000000000/test/%s" % approval_id)


class CronJobAprrovalTest(test_lib.GRRBaseTest):
  """Test for cron job approvals."""

  def testCreatingApprovalCreatesSymlink(self):
    cron_urn = rdfvalue.RDFURN("aff4:/cron/CronJobName")

    security.CronJobApprovalRequestor(
        reason=self.token.reason,
        subject_urn=cron_urn,
        approver="approver",
        token=self.token).Request()

    approval_id = list(
        aff4.FACTORY.ListChildren(
            "aff4:/users/test/approvals/cron/CronJobName"))[0].Basename()
    self.assertTrue(approval_id.startswith("approval:"))

    fd = aff4.FACTORY.Open(
        "aff4:/users/test/approvals/cron/CronJobName/%s" % approval_id,
        follow_symlinks=False,
        mode="r",
        token=self.token)
    self.assertEqual(fd.Get(fd.Schema.TYPE), "AFF4Symlink")
    self.assertEqual(
        fd.Get(fd.Schema.SYMLINK_TARGET),
        "aff4:/ACL/cron/CronJobName/test/%s" % approval_id)


class HuntApprovalTest(test_lib.GRRBaseTest):
  """Test for hunt approvals."""

  def testCreatingApprovalCreatesSymlink(self):
    hunt_urn = rdfvalue.RDFURN("aff4:/hunts/H:ABCD1234")

    security.HuntApprovalRequestor(
        reason=self.token.reason,
        subject_urn=hunt_urn,
        approver="approver",
        token=self.token).Request()

    approval_id = list(
        aff4.FACTORY.ListChildren(
            "aff4:/users/test/approvals/hunt/H:ABCD1234"))[0].Basename()
    self.assertTrue(approval_id.startswith("approval:"))

    fd = aff4.FACTORY.Open(
        "aff4:/users/test/approvals/hunt/H:ABCD1234/%s" % approval_id,
        follow_symlinks=False,
        mode="r",
        token=self.token)
    self.assertEqual(fd.Get(fd.Schema.TYPE), "AFF4Symlink")
    self.assertEqual(
        fd.Get(fd.Schema.SYMLINK_TARGET),
        "aff4:/ACL/hunts/H:ABCD1234/test/%s" % approval_id)


def main(argv):
  test_lib.main(argv)


if __name__ == "__main__":
  flags.StartMain(main)
