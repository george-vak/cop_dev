import argparse
from git import Repo

def list_branches(repo):
    branches = repo.branches
    for branch in branches:
        print(branch.name)

def show_last_commit(repo, branch_name):
    commit = repo.commit(branch_name)
    print(f"tree {commit.tree.hexsha}")
    if commit.parents:
        print(f"parent {commit.parents[0].hexsha}")
    print(f"author {commit.author.name} <{commit.author.email}>")
    print(f"committer {commit.committer.name} <{commit.committer.email}>")
    print(f"\n{commit.message.strip()}")

def show_tree(repo, commit):
    tree = commit.tree
    for item in tree:
        if item.type == 'blob':
            print(f"blob {item.hexsha}\t{item.path}")
        elif item.type == 'tree':
            print(f"tree {item.hexsha}\t{item.path}")

def traverse_history(repo, branch_name):
    commit = repo.commit(branch_name)
    while commit:
        print(f"TREE for commit {commit.hexsha}")
        show_tree(repo, commit)
        if commit.parents:
            commit = commit.parents[0]
        else:
            break


parser = argparse.ArgumentParser(description='Git Repository Viewer')
parser.add_argument('repo_path', help='Path to the git repository')
parser.add_argument('branch', nargs='?', help='Branch name (optional)')
args = parser.parse_args()

repo = Repo(args.repo_path)

if not args.branch:
    list_branches(repo)
else:
    show_last_commit(repo, args.branch)
    commit = repo.commit(args.branch)
    print('\n')
    show_tree(repo, commit)
    print('\n')
    traverse_history(repo, args.branch)
