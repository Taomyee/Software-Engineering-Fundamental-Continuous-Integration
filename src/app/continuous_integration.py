import os
import re
import smtplib
import ssl
from sys import platform

import subprocess
from email.message import EmailMessage


"""Continuous Integration"""

class ContinuousIntegration:
    """ Continuous Integration class.

    :ivar: repo_path: Path to the project repository locally.
    :type: path
    :ivar: resultFileName: Name of the result file containing date stamp and person who did pull request.
    :type: string
    :ivar: isRequirementsInstalled: Check if requirements are installed.
    :type: boolean
    :ivar: isSyntaxCheckingSucceeded: Check if the syntax is ok.
    :type: boolean
    :ivar: isTestingSucceeded: Check if all tests passed.
    :type: boolean
    :ivar: pathOSResults: Path to results folder in OS.
    :type: path
    :ivar: pathSrc: Path to source folder in OS.
    :type: path

    """

    def __init__(self, repo_path, resultFileName, pathOSResults, pathOSSrc):
        """ Initializing the object.

        :param repo_path: Path to the project repository locally.
        :type: repo_path: path
        :param resultFileName: Name of the result file containing time stamp and person who did pull request.
        :type: resultFileName: string
        :param pathOSResults: Path to results folder in OS.
        :type: pathOSResults: path
        :param pathOSSrc: Path to source folder in OS.
        :type: PathOSSrc: path
        """
        self.repo_path = repo_path
        self.resultFileName = resultFileName
        self.isRequirementsInstalled = False
        self.isSyntaxCheckingSucceeded = True
        self.isTestingSucceeded = False
        self.pathOSResults = pathOSResults
        self.pathSrc = pathOSSrc

    def installRequirements(self):
        """Method to install all the requirements needed for continuous integration and write results to a file.

        :returns: Print statement that the installation of requirements either failed or succeeded.
        """

        with open(os.path.join(os.getcwd() + self.pathOSResults, self.resultFileName), 'a') as resultFile:
            resultFile.write(f'2. Installing the requirements\n')
            resultFile.write("=================================================================================\n")
        if not self.repo_path:
            with open(os.path.join(os.getcwd() + self.pathOSResults, self.resultFileName), 'a') as resultFile:
                resultFile.write("The requirements file is missing.\n\n")
        else:
            path_req = self.repo_path + "/src/requirements.txt"
            with open(os.path.join(os.getcwd() + self.pathOSResults, self.resultFileName), 'a') as resultFile:
                subprocess.call("pip install -r " + path_req, shell = True, stdout=resultFile)
            self.isRequirementsInstalled = True
        if self.isRequirementsInstalled:
            print(f'Requirements installing succeeded.')
        else:
            print(f'Requirements installing failed.')

    def staticSyntaxCheck(self):
        """Method to check if syntax is correct and write the results to a file.

        :return: Print statement that checking the syntax either failed or succeeded.
        """
        if self.resultFileName:
            with open(os.path.join(os.getcwd() + self.pathOSResults, self.resultFileName), 'a') as resultFile:
                resultFile.write(f'\n2. Syntax checking\n')
                resultFile.write("=================================================================================\n")
            with open(os.path.join(os.getcwd() + self.pathOSResults, self.resultFileName), 'a') as resultFile:
                subprocess.call("pylint --disable=W,C,R,E0401 " + self.repo_path + self.pathSrc, shell = True, stdout=resultFile)
            with open("results" + ("/" if platform != "win32" else "\\") + self.resultFileName, 'r') as resultFile:
                result = None
                for l in resultFile:
                    result = re.search('E\d\d\d\d:', l)
                    if result is not None:
                        self.isSyntaxCheckingSucceeded = False
            if self.isSyntaxCheckingSucceeded:
                print(f'Syntax checking succeeded.')
            else:
                print(f'Syntax checking failed.')
        else:
            self.isSyntaxCheckingSucceeded = False
    def testing(self):
        """Method to test that the CI server works and write the results to a file.

        :return: Print statement that the testing either failed or succeeded.
        """

        if self.resultFileName:
            with open(os.path.join(os.getcwd() + self.pathOSResults, self.resultFileName), 'a') as resultFile:
                resultFile.write(f'3. Testing\n')
                resultFile.write("=================================================================================\n")
            with open(os.path.join(os.getcwd() + self.pathOSResults, self.resultFileName), 'a') as resultFile:
                subprocess.call("python -m unittest discover " + self.repo_path, shell=True, stderr=resultFile)
            with open("results" + ("/" if platform != "win32" else "\\") + self.resultFileName, 'r') as f:
                if not ("FAILED" in f.read()):
                    self.isTestingSucceeded = True
            if self.isTestingSucceeded:
                print(f'Testing succeeded.')
            else:
                print(f'Testing failed.')

    def sendNotification(self, userSender):
        """ Method to send message through email with with build results to user email
        :return: Results of build
        """
        team_dict = {
            'OudayAhmed': "oydddua@gmail.com",
            'ChristoferVikstroem': "christofer.vikstrom@outlook.com",
            'eliu1217': "eliu@kth.se",
            'OscarKnowles': "Oscar@knowles.se",
            'Taomyee': "yimingju2000@gmail.com"
        }
        email_message = EmailMessage()
        email_message['Subject'] = 'Build Results'
        syntaxCheckingResult = "succeeded" if self.isSyntaxCheckingSucceeded else "failed"
        testingResult = "succeeded" if self.isTestingSucceeded else "failed"
        resultDetails = ".\nFor more details: http://localhost:8015/results/" + self.resultFileName
        msg = "Syntax checking " + syntaxCheckingResult + ".\nTesting " + testingResult + resultDetails
        email_message.set_content(msg)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as stmp:
            stmp.login(os.environ.get('CI_EMAIL'), os.environ.get('CI_EMAIL_PASSWORD'))
            stmp.sendmail('cigroup15vt23@gmail.com', team_dict[userSender], email_message.as_string())
            print("The email notification has been sent")
