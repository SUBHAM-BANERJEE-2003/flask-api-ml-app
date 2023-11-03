to create a python virtual environment

proj-directory> python -m pip install virtualenv
proj-directory> python -m venv flask

it creates an virtual environment named flask.

to open that environment:

proj-directory> flask\Scripts\activate
upon successful activation, it shows like this

(flask)proj-directory>

now install the required modules with their corresponding version using the command 
(flask)proj-directory> python -m pip install -r requirements.txt

finally to run the project, use
(flask)proj-directory> python app.py
This will launch the app in localhost 5000 which is flasks default port

to close your virtual environment type 
(flask)proj-directory> deactivate

it terminates your virtual environment and that (flask) part is now gone 
