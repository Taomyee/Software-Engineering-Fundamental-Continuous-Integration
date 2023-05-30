from git import Repo
import os
import tempfile
from git import rmtree
from sys import platform

"""RepoGitHub class"""
class RepoGitHub:
    """ RepoGitHub class

    :ivar: data: a json file recording the POST request
    :type: data: dict
    :ivar: repo_name: the repository name
    :type: repo_name: string
    :ivar: branch_name: the branch name
    :type: branch_name: string
    :ivar: clone_url: the url of clone repository
    :type: clone_url: string
    :ivar: userSender: the user that sends the request
    :type: userSender: string
    :ivar: action: the action of the request
    :type: action: string
    :ivar: repo_path: the repository path locally
    :type: repo_path: string
    :ivar: repo_folder_name: the name of repository folder
    :type: repo_folder_name: string
    :ivar: isCloned: whether the repository is cloned
    :type: isCloned: bool
    :ivar: isRemoved: whether the repository is removed
    :type: isRemoved: bool
    :ivar: OSPathResults: OS path of results folder
    :type: OSPathResults: string
    :ivar: OSPathSrc: OS path of src folder
    :type: OSPathSrc: string
    """
    def __init__(self, data):
        """ Initializing the class

        :param data: a json file
        :type data: dict
        """
        self.data = data
        self.repo_name = data['pull_request']['head']['repo']['name']
        self.branch_name = data['pull_request']['head']['ref']
        self.clone_url = data['pull_request']['head']['repo']['clone_url']
        self.userSender = data['sender']['login']
        self.action = data['action']
        self.repo_path = ""
        self.repo_folder_name = ""
        self.isCloned = False
        self.isRemoved = False
        self.OSPathResults = ""
        self.OSPathSrc = ""
        self.checkOS()

    def cloneRepo(self, resultFileName):
        """ Clone the repository to the local

        :param resultFileName: the folder name of result files
        :type resultFileName: string
        """
        with open(os.path.join(os.getcwd() + self.OSPathResults, resultFileName), 'a') as resultFile:
            resultFile.write(f'1. Cloning the Repo\n')
            resultFile.write("=================================================================================\n")
            if not self.repo_name:
                resultFile.write("The repo name is missing.\n\n")
            elif not self.branch_name:
                resultFile.write("The branch name is missing.\n\n")
            elif not self.userSender:
                resultFile.write("Username is missing.\n\n")
            else:
                resultFile.write(f'Cloning the {self.repo_name} repo from the {self.branch_name} branch after a '
                                 f'pull\nrequest is {self.action} by {self.userSender}.\n\n')
                self.repo_path = tempfile.mkdtemp(dir=os.getcwd())
                self.repo_folder_name = self.repo_path[len(os.getcwd()) + 1:]
                Repo.clone_from(self.clone_url, self.repo_path, branch=self.branch_name)
                self.isCloned = True
            if self.isCloned:
                print(f'{self.repo_name} repo cloning succeeded.')
            else:
                print(f'{self.repo_name} repo cloning failed.')

    def removeRepo(self, resultFileName):
        """ Remove the repository from the local

        :param resultFileName: the folder name of result files
        :type resultFileName: string
        """
        with open(os.path.join(os.getcwd() + self.OSPathResults, resultFileName), 'a') as resultFile:
            if not self.repo_path:
                resultFile.write("The repo path is missing.\n\n")
            else:
                rmtree(self.repo_path)
                self.isRemoved = True
            if self.isRemoved:
                print(f'{self.repo_name} repo removing succeeded.')
            else:
                print(f'{self.repo_name} repo removing failed.')

    def checkOS(self):
        """ Store the path according to different operating systems

        """
        if platform == "darwin" or platform == "linux" or platform == "linux2":
            self.OSPathResults = "/results"
            self.OSPathSrc = "/src"
        else:
            self.OSPathResults = "\\results"
            self.OSPathSrc = "\\src"