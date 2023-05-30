import json
import os.path
from unittest import TestCase

from src.app.repo_github import RepoGitHub

"""TestRepoGitHub"""


class TestRepoGitHub(TestCase):
    """TestRepoGitHub class

    contains the test cases for repository cloning and removing
    """

    def test_clone_repo_pos(self):
        """Positive test for cloning repository

        Check whether the function cloneRepo() succeeds to clone the repo to a local directory
        """
        f = open("testcases/data_test_ci.json", 'r')
        data = json.load(f)
        f.close()
        repoGitHub = RepoGitHub(data)
        repoGitHub.cloneRepo("result.txt")
        self.assertTrue(os.path.isdir(repoGitHub.repo_folder_name))
        repoGitHub.removeRepo("result.txt")

    def test_clone_repo_neg(self):
        """Negative test for cloning repository

        Check whether the function cloneRepo() fails to clone the repo to a local directory
        """
        f = open("testcases/data_test_ci.json", 'r')
        data = json.load(f)
        f.close()
        repoGitHub = RepoGitHub(data)
        repo_folder_name_origin = repoGitHub.repo_folder_name
        repoGitHub.branch_name = ""
        repoGitHub.cloneRepo("result.txt")
        self.assertFalse(os.path.isdir(repo_folder_name_origin))

    def test_remove_repo_pos(self):
        """Positive test for removing repository

        Check whether the function removeRepo() succeeds to remove the repo from a local directory
        """
        f = open("testcases/data_test_ci.json", 'r')
        data = json.load(f)
        f.close()
        repoGitHub = RepoGitHub(data)
        repoGitHub.cloneRepo("result.txt")
        repoGitHub.removeRepo("result.txt")
        self.assertFalse(os.path.isdir(repoGitHub.repo_folder_name))

    def test_remove_repo_neg(self):
        """Negative test for removing repository

        Check whether the function removeRepo() fails to remove the repo from a local directory
        """
        f = open("testcases/data_test_ci.json", 'r')
        data = json.load(f)
        f.close()
        repoGitHub = RepoGitHub(data)
        repoGitHub.cloneRepo("result.txt")
        repoGitHub.repo_path = ""
        repoGitHub.removeRepo("result.txt")
        self.assertTrue(os.path.isdir(repoGitHub.repo_folder_name))


