Setup
=====

Master Pi
*********

Backend - RESTful API
#####################

1. Install virtual environment tool  *pipenv*.

.. code-block:: bash

   $ pip3 install pipenv

2. Set up environment variables:

.. code-block:: bash

   $ export FLASK_APP=master_pi.py
   $ export FLASK_ENV=production
   $ export My_SQL={your local MySQL password}

3. Start MySQL deamon process.

.. code-block:: bash

   $ mysqld

4. Go to project folder, install required packages, and start backend server.

.. code-block:: bash

   $ cd {project_root_folder}/pi
   $ pipenv install 
   $ pipenv shell
   $ flask run

  
5. Access API root path with port *5000*.

.. code-block:: bash

   http://127.0.0.1:5000/

Frontend - React Web App
########################

1. Configure repository to install yarn.

.. code-block:: bash

   $ curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
   $ echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list

2. Install yarn package manager.

.. code-block:: bash

   $ sudo apt update && sudo apt install yarn

3. Go to project folder and install required node packages.

.. code-block:: bash

   $ cd {project_root_folder}/web
   $ yarn install
   $ yarn start

4. Access Master Pi website.

.. code-block:: bash

   http://127.0.0.1:3000/

Agent Pi
********

1. Install virtual environment tool  *pipenv*.

.. code-block:: bash

   $ pip3 install pipenv

2. Set up environment variables:

.. code-block:: bash

   $ export FLASK_APP=agent_pi.py
   $ export FLASK_ENV=production
   $ export My_SQL={your local MySQL password}

3. Go to project folder, install required packages, and start backend server.

*OpenCV (cv2)* package requires Python 3.7 or less.

.. code-block:: bash

   $ cd {project_root_folder}/pi
   $ pipenv install 
   $ pipenv install opencv-python
   $ pipenv shell
   $ flask run