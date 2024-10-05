Application Setup
Prerequisites
1.	Python: Have Python 3.x installed.
2.	pip: This usually comes with Python.
3.	A code editor: Visual Studio Code
Step 1: Create a Project Directory
1.	Open your terminal or command prompt.
2.	Create a new directory for your project and navigate into it:
mkdir python_web_app
cd python_web_app
Step 2: Create a Virtual Environment
1.	Create a virtual environment:
python -m Web_app venv
2.	Activate the virtual environment:
Web_app \Scripts\activate
Step 3: Create the Python Application
1.	Create a new Python file:
touch app.py
2.	Open app.py in your code editor and add simple code
Step 4: Install Flask
Once virtual environment is activated (you should see (Web_app) in your terminal).
Install Flask using pip:
pip install Flask
Step 5: Run the Application
In your terminal, run the application:
python app.py
You should see output indicating that the server is running, typically on 5000 port.
Step 6: Access the Application
1.	Open your web browser.
2.	Go to localhost:5000
You should see the message displayed in your browser.
Step 7: Stop the Application
To stop the application, return to your terminal and press Ctrl + C.

Push Files to GitHub repository
1. Navigate to Your Project Directory
Open your terminal and navigate to the directory containing your project files:
cd path/to/your/project
2. Initialize a Local Git Repository
git init
3. Add Remote Repository
git remote add origin <repository-url>
4. Add Files to Staging Area
git add .
5. Commit Your Changes
git commit -m "Initial commit"
6. Rename branch 
git branch -M main
7. Push to repository
git push -u origin main

Pipeline overview
Workflow Details
Prerequisites
•	Ensure EC2 instances have Docker, Git, and Ansible installed, or pipeline is configured to install them.
•	The necessary security groups and firewall rules should allow SSH access and HTTP traffic to the application.
Trigger
The workflow is triggered on a push to the main branch.
Jobs
The workflow consists of a single job named build, which runs on an ubuntu-latest runner. It contains several steps as outlined below.
Steps
1.	Checkout Code
o	Uses the actions/checkout@v2 action to check out the code from the repository.
2.	Log in to Docker Hub
o	Uses the docker/login-action@v1 action to log in to Docker Hub with credentials stored in GitHub Secrets:
	DOCKER_HUB_USERNAME
	DOCKER_HUB_ACCESS_TOKEN
3.	Build and Deploy to Development EC2
o	Uses the appleboy/ssh-action@master action to SSH into the development EC2 instance.
o	The following operations are performed:
	Adds the host key to known_hosts.
	Installs git if not already installed.
	Clones the repository if it does not exist or pulls the latest changes if it does.
	Installs ansible if not already installed.
	Runs an Ansible playbook for configuration (configuration_dev.yml).
	Cleans up old Docker images.
	Builds the Docker image.
	Runs tests using pytest within the Docker container.
	Logs in to Docker Hub and pushes the newly built image.
	Stops and removes the existing Docker container, if it exists.
	Runs a new Docker container with the updated image.
4.	Deploy to Production EC2
o	Similar to the development step, but targets the production EC2 instance and uses a different Ansible playbook (configuration_prod.yml).
o	Pulls the latest Docker image and manages the Docker container as in the development step.
Secrets
The following secrets are used in this workflow and must be configured in the GitHub repository settings:
•	DOCKER_HUB_USERNAME: Your Docker Hub username.
•	DOCKER_HUB_ACCESS_TOKEN: A Docker Hub access token for authentication.
•	SSH_PRIVATE_KEY: The private SSH key for accessing the EC2 instances.
•	DEV_IP_ADDRESS: The IP address of the development EC2 instance.
•	PROD_IP_ADDRESS: The IP address of the production EC2 instance.

Structure of the Dockerfile
The Dockerfile consists of three main stages: builder, tester, and final. Each stage is designed to handle specific tasks efficiently.
1. Builder Stage
•	Base Image:
o	Uses the official python:3.9-slim image as the base for building the application.
•	Working Directory:
o	Sets the working directory to /app.
•	Install Dependencies:
o	Copies requirements.txt to the container.
o	Installs the required Python packages listed in requirements.txt using pip with the --no-cache-dir option to reduce image size.
•	Copy Application Code:
o	Copies the rest of the application code into the container.
2. Tester Stage
•	Environment Variable:
o	Sets PYTHONPATH to the current working directory to ensure the application can be found when running tests.
•	Run Tests:
o	Executes tests using pytest. Ensure that pytest is included in the requirements.txt file.
3. Final Stage
•	Base Image:
o	Again uses the python:3.9-slim image for the final runtime environment.
•	Working Directory:
o	Sets the working directory to /app.
•	Copy Necessary Files:
o	Copies application files and installed packages from the builder stage to the final image.
•	Expose Port:
o	Exposes port 5000 for the Flask application.
•	Run Command:
o	Specifies the command to run the application: CMD ["python", "app.py"].

Structure of Ansible Playbook
1. Update Apt Package Index
•	Updates the package index to ensure the latest version of packages can be installed.
2. Check if Docker is Installed
•	Executes the command docker --version to check if Docker is already installed on the host. The result is registered for use in subsequent tasks.
3. Install Docker if Not Installed
•	Installs Docker using the package manager if the previous command indicates that Docker is not installed.
4. Verify Docker Installation
•	Checks the installed Docker version to confirm that it has been installed correctly.
5. Debug Output
•	Outputs the installed Docker version for confirmation.

Structure of Inventory file
•  Group Name: dev, prod
•	This section contains hosts that belong to the development environment and production environment.
•  Host Definition:
•	dev-server: A name you can use to refer to this server within your Ansible playbooks.
•	ansible_host: The actual IP address of the development server.
•	prod-ec2-instance: A name for the production server, used within Ansible.
•	ansible_host: The actual IP address of the production EC2 instance.
•  Global Variables: This section defines variables that apply to all hosts.
•	ansible_user=ubuntu: The default user to connect to the servers via SSH

Test file structure
•  Importing Dependencies:
•	pytest: The testing framework.
•	app: The Flask application instance to be tested.
•  Fixture:
•	client(): A pytest fixture that creates a test client for the Flask application. This allows you to simulate requests to your application.
•  Test Case:
•	test_homepage(client): A function that tests the homepage of the application.
o	Sends a GET request to the homepage (/).
o	Asserts that the response status code is 200 OK.
o	Checks that the response content contains the text "Welcome to IQVIA!".

Dependencies
The following packages are included in the requirements.txt file:
1.	Flask: Version 2.1.2
o	A lightweight WSGI web application framework in Python. It is designed to make getting started quick and easy, with the ability to scale up to complex applications.
2.	Jinja2: Version 3.0.3
o	A modern and designer-friendly templating language for Python, used by Flask to render HTML templates.
3.	Werkzeug: Version 2.0.3
o	A comprehensive WSGI web application library that powers Flask. It provides utilities for building web applications in Python.
4.	pytest
o	A framework that makes building simple and scalable test cases easy. It is used for writing and running tests for your Flask application.
