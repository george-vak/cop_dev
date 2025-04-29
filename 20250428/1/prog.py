from pathlib import Path

DOIT_CONFIG = {"default_tasks": ["docs"]}


def task_docks():
    """Build documentation"""
    return {
        'task_dep': ['png'],
        "actions": ["sphinx-build -M html . _build"]
    }


def task_erase():
    return {
        "actions": ["git reset --hard", "git clean -xdf"]
    }

# def list_zip(name, outfile):
#     with ZipFile(name) as zf:
#         res = zf.namelist()
#     with open(outfile, "w") as of:
#         print("\n".join(res), file=of)
