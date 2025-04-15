from github import Github
from github.GithubException import GithubException
from git.exc import GitCommandError
import os
import shutil
import stat

def create_branch_and_pr(repo, local_path, branch_name, modified_files, user_token):
    origin_url = repo.remotes.origin.url

    # Create a new local branch from HEAD
    repo.git.checkout("HEAD", b=branch_name)

    # Stage and commit modified files
    for file in modified_files:
        rel_path = os.path.relpath(file, local_path)
        repo.git.add(rel_path)

    repo.git.commit("-m", "Fix dead links via DeadLinkFixer")

    # Try pushing the branch to origin
    try:
        repo.git.push("origin", branch_name)
    except GitCommandError as e:
        return {
            "message": f"Push failed: {parse_git_error(e)}",
            "pull_request_url": None,
            "is_existing_pr": False
        }
    finally:
        cleanup_local_repo(local_path)

    # Authenticate with GitHub
    g = Github(user_token)
    remote_path = origin_url.split(".com/")[1].replace(".git", "")
    gh_repo = g.get_repo(remote_path)

    # Detect default branch (main/master/etc.)
    default_branch = gh_repo.default_branch

    # Check for existing open PR from this branch
    existing_prs = gh_repo.get_pulls(state="open", head=f"{gh_repo.owner.login}:{branch_name}")
    if existing_prs.totalCount > 0:
        pr = existing_prs[0]
        return {
            "message": "Dead links fixed. An existing pull request was found.",
            "pull_request_url": pr.html_url,
            "is_existing_pr": True
        }

    # Create new PR
    try:
        pr = gh_repo.create_pull(
            title="Fix dead links",
            body="This pull request was automatically created by DeadLinkFixer.",
            head=branch_name,
            base=default_branch
        )
        return {
            "message": "Dead links fixed and pull request created.",
            "pull_request_url": pr.html_url,
            "is_existing_pr": False
        }
    except GithubException as e:
        return {
            "message": f"Failed to create PR: {e.data}",
            "pull_request_url": None,
            "is_existing_pr": False
        }

def parse_git_error(e):
    if hasattr(e, "stderr") and e.stderr:
        lines = e.stderr.strip().splitlines()
        for line in lines:
            if "Updates were rejected" in line or "error:" in line or "hint:" in line:
                return line
    return str(e)

def cleanup_local_repo(path):
    try:
        shutil.rmtree(path, onerror=force_remove_readonly)
        print(f"Deleted local repo: {path}")
    except Exception as e:
        print(f"Failed to delete local repo: {e}")

def force_remove_readonly(func, path, exc_info):
    import errno
    exc_type, exc_value, _ = exc_info
    if isinstance(exc_value, PermissionError) or (
        hasattr(exc_value, 'winerror') and exc_value.winerror == 5
    ):
        try:
            os.chmod(path, stat.S_IWRITE)
            func(path)
        except Exception as e:
            print(f"Force delete failed on {path}: {e}")
    else:
        raise
