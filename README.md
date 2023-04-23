# powerplant-coding-challenge

This is my implementation of the [powerplant coding challenge](https://github.com/gem-spaas/powerplant-coding-challenge).

## How to run
### Using docker-compose
1. Simply run 
   `````bash
   docker-compose up
   `````
   to build and run the app, which is accessible through [localhost:8888](http://127.0.0.1:8888/).


2. You can also run the tests with:
   ````bash
   docker exec -it powerplant-coding-challenge-app-1 python manage.py test
   ````
### Using docker
1. To build and run this application using docker, simply navigate to the root of this repository and run:
    ````bash
    docker build -t powerplants . && docker run --name pplants --rm -it powerplants
    ````
2. You can test the application with the example payloads using this command:
    ````bash
    docker exec -it pplants python manage.py test
    ````

### Without docker
0. Optionally, it is recommended to start by creating and activating a [virtual environment](https://docs.python.org/3/tutorial/venv.html).
1. To install the necessary python3 libraries, run the following command:
   `````bash
   pip install -r requirements.txt
    `````
2. Then, to run the server, simply run:
   `````bash
   cd src/ucp
   python manage.py runserver 8888
   `````
3. Finally, you can run the test suite with:
   `````bash
   python manage.py test
   `````

## How it works
This was implemented in Python, using Django.

To come up with the main algorithm, I inspired myself of the outline described on the following page:
[https://optimization.cbe.cornell.edu/index.php?title=Unit_commitment_problem](https://optimization.cbe.cornell.edu/index.php?title=Unit_commitment_problem).

