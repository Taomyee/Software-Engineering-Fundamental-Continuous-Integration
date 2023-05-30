import json
from unittest import TestCase

from src.app.build_results import BuildResults
from src.app.continuous_integration import ContinuousIntegration
from src.app.repo_github import RepoGitHub


class TestContinuousIntegration(TestCase):

    def test_install_requirements_positive(self):
        """
        Valid test for install_requirements method, asserts that requirements are installed
        """
        f = open("testcases/data_test_ci.json", 'r')
        data = json.load(f)
        f.close()
        repo = RepoGitHub(data)
        buildResults = BuildResults(repo)
        repo.cloneRepo(buildResults.resultFileName)
        ci_server = ContinuousIntegration(repo.repo_path, buildResults.resultFileName, repo.OSPathResults, repo.OSPathSrc)
        ci_server.installRequirements()
        repo.removeRepo(buildResults.resultFileName)
        buildResults.resultFile.close()
        self.assertTrue(ci_server.isRequirementsInstalled)


    def test_install_requirements_wrong_path(self):
        """
        Invalid test requirements for install_requirements method, asserts that requirements are not installed
        """
        f = open("testcases/data_test_ci.json", 'r')
        data = json.load(f)
        f.close()
        repo = RepoGitHub(data)
        buildResults = BuildResults(repo)
        repo.cloneRepo(buildResults.resultFileName)
        ci_server = ContinuousIntegration("", buildResults.resultFileName, repo.OSPathResults,
                                          repo.OSPathSrc)
        ci_server.installRequirements()
        repo.removeRepo(buildResults.resultFileName)
        buildResults.resultFile.close()

        self.assertFalse(ci_server.isRequirementsInstalled)

    def test_static_syntax_check_positive(self):
        """
        Valid test for syntax_check method, asserts that syntax succeeded.
        """
        f = open("testcases/data_test_ci.json", 'r')
        data = json.load(f)
        f.close()
        repo = RepoGitHub(data)
        buildResults = BuildResults(repo)
        repo.cloneRepo(buildResults.resultFileName)
        ci_server = ContinuousIntegration(repo.repo_path, buildResults.resultFileName, repo.OSPathResults,
                                          repo.OSPathSrc)
        ci_server.installRequirements()
        ci_server.staticSyntaxCheck()
        repo.removeRepo(buildResults.resultFileName)
        buildResults.resultFile.close()
        self.assertTrue(ci_server.isSyntaxCheckingSucceeded)

    def test_static_syntax_check_wrong_result_file_name(self):
        """
        Invalid test for syntax_check method, asserts that syntax is not succeeded.
        """
        f = open("testcases/data_test_ci.json", 'r')
        data = json.load(f)
        f.close()
        repo = RepoGitHub(data)
        buildResults = BuildResults(repo)
        repo.cloneRepo(buildResults.resultFileName)
        ci_server = ContinuousIntegration(repo.repo_path, buildResults.resultFileName, repo.OSPathResults,
                                          repo.OSPathSrc)
        ci_server.installRequirements()
        ci_server.resultFileName = ""
        ci_server.staticSyntaxCheck()
        repo.removeRepo(buildResults.resultFileName)
        buildResults.resultFile.close()
        self.assertFalse(ci_server.isSyntaxCheckingSucceeded)

    def test_testing_positive(self):
        """
        Valid test method, asserts that tests are succeeded.
        """
        f = open("testcases/data_test_ci.json", 'r')
        data = json.load(f)
        f.close()
        repo = RepoGitHub(data)
        buildResults = BuildResults(repo)
        repo.cloneRepo(buildResults.resultFileName)
        ci_server = ContinuousIntegration(repo.repo_path, buildResults.resultFileName, repo.OSPathResults,
                                          repo.OSPathSrc)
        ci_server.installRequirements()
        ci_server.testing()
        repo.removeRepo(buildResults.resultFileName)
        buildResults.resultFile.close()
        self.assertTrue(ci_server.isTestingSucceeded)

    def test_testing_wrong_result_file_name(self):
        """
        Invalid test method, asserts that tests are not succeeded.
        """
        f = open("testcases/data_test_ci.json", 'r')
        data = json.load(f)
        f.close()
        repo = RepoGitHub(data)
        buildResults = BuildResults(repo)
        repo.cloneRepo(buildResults.resultFileName)
        ci_server = ContinuousIntegration(repo.repo_path, buildResults.resultFileName, repo.OSPathResults,
                                          repo.OSPathSrc)
        ci_server.installRequirements()
        ci_server.resultFileName = ""
        ci_server.testing()
        repo.removeRepo(buildResults.resultFileName)
        buildResults.resultFile.close()
        self.assertFalse(ci_server.isTestingSucceeded)