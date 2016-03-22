# PSYMBIOSYS-Influencial

A demonstrative BIG DATA project of the PSYMBIOSYS H2020 project for the task 8.7

## Installing the Infrastructure
 In order to run the system, first you need to setup the underlying infrastructure which builds the HDFS, HADOOP and SPARK ecosystem.
 For this, follow first the instructions from this [repo](https://github.com/epu-ntua/pyspark-docker).
 
 
## Running the Project
 The project is a simple [django](https://www.djangoproject.com/) app and can be build as follows:
 * Install dependencies.  `$ pip install -r requirements.txt`
 * Run the Server `$ python manage.py runserver`
 * Point your browser at, [http://localhost:8000/](http://localhost:8000/)
