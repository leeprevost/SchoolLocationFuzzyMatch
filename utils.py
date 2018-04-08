import subprocess


def current_git_sha():
    return subprocess.check_output([
        'git', 'rev-parse', '--short=6', 'HEAD']).decode("utf-8").strip()
