#!/usr/bin/env python
# -*- mode: python; encoding: utf-8 -*-
"""Test the vfs gui interface."""


import mock
import unittest
from grr.gui import api_call_router_with_approval_checks
from grr.gui import gui_test_lib
from grr.gui.api_plugins import vfs as api_vfs

from grr.lib import flags
from grr.lib.rdfvalues import client as rdf_client
from grr.server import aff4
from grr.test_lib import fixture_test_lib


class VFSViewTest(gui_test_lib.GRRSeleniumTest):

  def setUp(self):
    super(VFSViewTest, self).setUp()
    # Prepare our fixture.
    self.client_id = rdf_client.ClientURN("C.0000000000000001")
    fixture_test_lib.ClientFixture(self.client_id, self.token)
    gui_test_lib.CreateFileVersions(self.token)
    self.RequestAndGrantClientApproval("C.0000000000000001")

  def testUnicodeContentIsShownInTree(self):
    # Open VFS view for client 1 on a specific location.
    self.Open("/#clients/C.0000000000000001/vfs/fs/os/c/Downloads/")

    # Click on the file containing unicode characters.
    self.Click(u"css=tr:contains(\"中.txt\")")
    # Then click on the "Download" tab.
    self.Click("css=li[heading=Download]:not(.disabled)")

    self.WaitUntil(self.IsTextPresent, u"中国新闻网新闻中.txt")

  def testFolderPathCanContainUnicodeCharacters(self):
    # Open VFS view for client 1 on a location containing unicode characters.
    self.Open("/#/clients/C.0000000000000001/vfs/fs/os/c/中国新闻网新闻中/")

    # Check that the correct file is listed.
    self.WaitUntil(self.IsElementPresent, "css=tr:contains(\"bzcmp\")")

  def testUrlSensitiveCharactersAreShownInTree(self):
    gui_test_lib.CreateFileVersion(
        "aff4:/C.0000000000000001/fs/os/c/foo?bar&oh/a&=?b.txt",
        "Hello World",
        timestamp=gui_test_lib.TIME_1,
        token=self.token)

    # Open VFS view for client 1 on a specific location.
    self.Open("/#c=C.0000000000000001&main=VirtualFileSystemView&t=_fs-os-c")

    # Wait until the folder gets selected and its information displayed in
    # the details pane.
    self.WaitUntil(self.IsTextPresent, "C.0000000000000001/fs/os/c")

    # Click on the "foo?bar&oh" subfolder.
    self.Click("css=#_fs-os-c-foo_3Fbar_26oh a:visible")

    # Some more unicode testing.
    self.Click(u"css=tr:contains(\"a&=?b.txt\")")
    self.Click("css=li[heading=Download]")

    self.WaitUntil(self.IsTextPresent, u"a&=?b.txt")

    # Test the text viewer.
    self.Click("css=li[heading=TextView]")
    self.WaitUntilContains("Hello World", self.GetText, "css=div.monospace pre")

  def testFolderPathCanContainUrlSensitiveCharacters(self):
    gui_test_lib.CreateFileVersion(
        "aff4:/C.0000000000000001/fs/os/c/foo?bar&oh/a&=?b.txt",
        "Hello World",
        timestamp=gui_test_lib.TIME_1,
        token=self.token)

    # Open VFS view for client 1 on a location containing unicode characters.
    self.Open("/#c=C.0000000000000001&main=VirtualFileSystemView&t=_fs-os-c"
              "-foo_3Fbar_26oh")

    # Check that the correct file is listed.
    self.WaitUntil(self.IsElementPresent, "css=tr:contains(\"a&=?b.txt\")")

  def testDoubleClickGoesInsideDirectory(self):
    """Tests that double click in FileTable goes inside the directory."""

    self.Open("/")

    self.Type("client_query", "C.0000000000000001")
    self.Click("client_query_submit")

    self.WaitUntilEqual(u"C.0000000000000001", self.GetText,
                        "css=span[type=subject]")

    # Choose client 1 and go to 'Browse Virtual Filesystem'
    self.Click("css=td:contains('0001')")
    self.Click("css=a[grrtarget='client.vfs']")
    self.Click("link=fs")

    # Now click on "os" inside the table. Tree shouldn't get updated,
    self.Click("css=td:contains('os')")

    # Now double click on "os".
    self.DoubleClick("css=td:contains('os')")

    # Now we should be inside the folder, and the tree should open.
    self.WaitUntil(self.IsElementPresent, "css=#_fs-os-c i.jstree-icon")
    # Check that breadcrumbs got updated.
    self.WaitUntil(self.IsElementPresent,
                   "css=#content_rightPane .breadcrumb li:contains('os')")

  def testClickingOnTreeNodeRefreshesChildrenFoldersList(self):
    self.Open("/#/clients/C.0000000000000001/vfs/fs/os/c/")

    self.WaitUntil(self.IsElementPresent, "link=Downloads")
    self.WaitUntil(self.IsElementPresent, "link=bin")

    aff4.FACTORY.Delete(
        "aff4:/C.0000000000000001/fs/os/c/bin", token=self.token)

    self.Click("link=c")
    self.WaitUntil(self.IsElementPresent, "link=Downloads")
    self.WaitUntilNot(self.IsElementPresent, "link=bin")

  def testClickingOnTreeNodeArrowRefreshesChildrenFoldersList(self):
    self.Open("/#/clients/C.0000000000000001/vfs/fs/os/c/")

    self.WaitUntil(self.IsElementPresent, "link=Downloads")
    self.WaitUntil(self.IsElementPresent, "link=bin")

    aff4.FACTORY.Delete(
        "aff4:/C.0000000000000001/fs/os/c/bin", token=self.token)

    # Click on the arrow icon, it should close the tree branch.
    self.Click("css=#_fs-os-c i.jstree-icon")
    self.WaitUntilNot(self.IsElementPresent, "link=Downloads")
    self.WaitUntilNot(self.IsElementPresent, "link=bin")

    # Click on the arrow icon again, it should reopen the tree
    # branch. It should be updated.
    self.Click("css=#_fs-os-c i.jstree-icon")
    self.WaitUntil(self.IsElementPresent, "link=Downloads")
    self.WaitUntilNot(self.IsElementPresent, "link=bin")

  @mock.patch.object(
      api_call_router_with_approval_checks.ApiCallRouterWithApprovalChecks,
      "GetVfsFilesArchive")
  def testClickingOnDownloadCurrentFolderButtonStartsDownload(
      self, mock_method):
    # Open VFS view for client 1 on a specific location.
    self.Open("/#c=C.0000000000000001&main=VirtualFileSystemView"
              "&t=_fs-os-c-proc")

    self.Click("css=grr-vfs-files-archive-button")
    self.Click("css=a[name=downloadCurrentFolder]")
    self.WaitUntilEqual(1, lambda: mock_method.call_count)
    mock_method.assert_called_once_with(
        api_vfs.ApiGetVfsFilesArchiveArgs(
            client_id="C.0000000000000001", file_path="fs/os/c/proc"),
        token=mock.ANY)

  @mock.patch.object(
      api_call_router_with_approval_checks.ApiCallRouterWithApprovalChecks,
      "GetVfsFilesArchive")
  def testClickingOnDownloadEverythingButtonStartsDownload(self, mock_method):
    # Open VFS view for client 1 on a specific location.
    self.Open("/#c=C.0000000000000001&main=VirtualFileSystemView"
              "&t=_fs-os-c-proc")

    self.Click("css=grr-vfs-files-archive-button")
    self.Click("css=a[name=downloadEverything]:not([disabled])")
    self.WaitUntilEqual(1, lambda: mock_method.call_count)
    mock_method.assert_called_once_with(
        api_vfs.ApiGetVfsFilesArchiveArgs(client_id="C.0000000000000001"),
        token=mock.ANY)


def main(argv):
  del argv  # Unused.
  # Run the full test suite
  unittest.main()


if __name__ == "__main__":
  flags.StartMain(main)
