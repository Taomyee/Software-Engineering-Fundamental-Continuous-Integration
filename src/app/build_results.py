import os
from datetime import datetime


class BuildResults:

    def __init__(self, repoGitHub):
        self.repoGitHub = repoGitHub
        self.dateFileCreated = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.resultFileName = self.dateFileCreated + "_" + repoGitHub.userSender + '.txt'
        self.resultFile = open(os.path.join(os.getcwd() + repoGitHub.OSPathResults, self.resultFileName), 'x')