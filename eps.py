#!/usr/bin/env python3
'''
Explain all running processes.
Require: psutil>=5.2.2
'''
import subprocess as spr
from functools import lru_cache

import psutil


def run_cmd(cmd):
    p = spr.Popen(cmd, stdout=spr.PIPE, stderr=spr.PIPE)
    out, err = p.communicate()
    if p.returncode != 0:
        raise spr.CalledProcessError(cmd, p.returncode)
    else:
        return out


@lru_cache(maxsize=128)
def query_summary(pkg):
    return run_cmd(['dpkg-query', '-f', '${binary:Summary}',
                   '--show', pkg]).decode()


def get_pkg_of_exe(exe_path):
    return run_cmd(['dpkg', '--search', exe_path]).split(b':')[0].decode()


def explain(process):
    p = process
    try:
        exe_path = p.exe()
    except psutil.AccessDenied:
        exe_path = 'Kernel'
        pkg = 'Kernel'
        summary = 'Kernel'
    else:
        try:
            pkg = get_pkg_of_exe(exe_path)
            summary = query_summary(pkg)
        except spr.CalledProcessError:
            pkg = "UNKNOWN"
            summary = "UNKNOWN"

    FMT = ('PID: {pid:<5} {name} - EXE: {exe}, PKG: {pkg}'
           '\n\tSummary: {summary}')
    print(FMT.format(pid=p.pid, name=p.name(),
                     exe=exe_path, pkg=pkg, summary=summary))


def main():
    for p in psutil.process_iter():
        explain(p)


if __name__ == "__main__":
    main()
