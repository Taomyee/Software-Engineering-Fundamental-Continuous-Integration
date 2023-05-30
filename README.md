# Assignment 2 - Continuous-Integration
This repository consist of code for the Continuous Integration lab (course DD2480) at KTH. 

The program in this repository is an implementation of a small continuous integration CI server. The features of the server is:
- Compilation
    - The server supports compiling the group project.
    - The server has a syntax check that is performed for languages without compilers. 
    - Compilation is triggered as webhook.
- Testing
    - The server supports executing the automated tests for the group project. 
    - Testing is triggered as webhook on the branch where the change has been made (as specified in the HTTP payload).
- Notification
    - The server supports notification of CI results.
    - The server sends an email to the project member about the build result. 

## Installation
In order to run the code properly, a version of Python >= 3.8 (placeholder) is required.

### Run code and tests
Before you can run the program you need to install the requirements. To do this first navigate to the src folder, then the app folder, and run this command in the terminal:

    python3 continuous_integration.py

To troubleshoot any potential requirement installations, the packages could be installed manually in the terminal as well with these following commands:

    pip install Flask
    pip install pylint
    pip install Flask-Mail
    pip install GitPython

To run the server, navigate to the src folder, then the app folder, and run this command in the terminal:

    python3 continuous_intergration_server.py

To run the tests, navigate to the src folder, then the test folder. Then run this command in the terminal:
    
    python3 -m unittest discover

To open the documentation, you can access it by navigating to the following path in the web browser:

    doc/_build/html/index.html

## Contributions

- **Ouday Ahmed**: Ouday designed and implemented the general code architecture of the project, including the class skeletons.  He has also written the code for the methods in continouous_integraton.py
- **Yiming Ju**: Yiming has implemented the tests and written documentation for the repo_github.py methods. 
- **Oscar Knowles**: Oscar has implemented the tests and written documentation for the continuous_integration.py methods and written SEMAT and project documentation (README) together with Christofer and Elin. 
- **Elin Liu**: Elin was the stakeholder for building and implemententing the Sphinx tests and written SEMAT togheter with Oscar and Christofer.
- **Christofer Vikström**: Christofer created the code and documentation for the notification method that sends email from the group dedicated CI gmail to the team member with the build results. He also created the SEMAT and project documentation (README) together with Oscar and Elin. 


### Argument 1 for P+:
Property: Most commits (typically 90%) are linked to an issue describing the feature / commit.

Currently, the requirements regarding commits tracing to issues is fulfilled.

### Argument 2 for P+:
Property: This history persists even if the server is rebooted. Each build is given a unique URL, that is accessible to get the build information (commit identifier, build date, build logs). One URL exists to list all builds.

All builds are stored in a unique URL that can be found in /results.



