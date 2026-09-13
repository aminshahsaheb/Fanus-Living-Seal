import subprocess

def get_git_diff():
    return subprocess.getoutput("git diff --name-only")

def build_context():
    return {
        "changed_files": get_git_diff()
    }
