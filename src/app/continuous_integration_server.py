from flask import request
from flask import Flask
import os

from src.app.build_results import BuildResults
from src.app.continuous_integration import ContinuousIntegration
from src.app.repo_github import RepoGitHub

app = Flask(__name__)


@app.route('/results')
def get_results():
    """
    Get the page content from the recorded results
    """
    dir_path = os.getcwd() + "\\results"
    page_content = ""
    numberResults = len(os.listdir(dir_path))
    if numberResults == 0:
        return "There are no results files."
    for filename in os.listdir(dir_path):
        page_content += "<a href='/results/" + filename + "'>" + filename + "</a><br>"
    return page_content


@app.route('/results/<filename>')
def get_resultFile(filename):
    """
    Record the result of handling requests in the path ./results/filename.
    """
    content = ""
    with open(os.path.join(os.getcwd() + "\\results", filename), 'r') as resultFile:
        for l in resultFile.readlines():
            content += l + "<br>"
    return content


@app.route('/')
def get_continuous_integration():
    """
    Indicate it's a continuous integration server.
    """
    return "Continuous Integration Server"


@app.route('/', methods=['POST'])
def continuous_integration_post():
    """
    This function is the endpoint for GitHub webhooks to handle POST request.
    1. Create a history entry recording the results
    2. Clone the repository
    3. Install the requirements.txt
    4. Syntax checking
    5. Test on unittests
    6. Remove the repository

    :return:
        If the server runs successfully, return "Succeeded"
        Otherwise, return "This action is not supported by the server."
    """
    dataJSON = request.json
    if 'pull_request' in dataJSON and (
            dataJSON['action'] == "opened" or dataJSON['action'] == 'synchronize' or dataJSON['action'] == "reopened"):
        repoGitHub = RepoGitHub(dataJSON)
        build_results = BuildResults(repoGitHub)
        repoGitHub.cloneRepo(build_results.resultFileName)
        if repoGitHub.isCloned:
            continuous_integration = ContinuousIntegration(repoGitHub.repo_path, build_results.resultFileName,
                                                           repoGitHub.OSPathResults, repoGitHub.OSPathSrc)
            continuous_integration.installRequirements()
            if continuous_integration.isRequirementsInstalled:
                continuous_integration.staticSyntaxCheck()
                continuous_integration.testing()
                continuous_integration.sendNotification(repoGitHub.userSender)
        repoGitHub.removeRepo(build_results.resultFileName)
        return "Succeeded"
    else:
        return "This action is not supported by the server."


if __name__ == '__main__':
    app.run(host="localhost", port=8015)
