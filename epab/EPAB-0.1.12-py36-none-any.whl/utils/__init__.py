# coding=utf-8

from ._console import _error, _info, _cmd, _out
from ._do import do, do_ex, find_executable
from ._pipenv import write_reqs, update_env, ensure_module
from ._repo import repo_ensure, repo_get_latest_tag, repo_get_current_branch, repo_is_dirty, repo_commit,\
    repo_checkout, repo_merge, repo_push, repo_tag, repo_remove_tag
from ._run_once import run_once
from ._temp_dir import temporary_working_dir
from ._version import bump_version
from ._dry_run import dry_run


def ensure_exe(exe_name: str, path: str = None):
    if not find_executable(exe_name, path):
        _error(f'Could not find "{exe_name}.exe" on this system')
        exit(-1)
