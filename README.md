### Depression Analysis For Tweets ####

#### Setting up for the project ###
#clone the project 
#create an enviroment either using conda or virtualenv
#switch into your enviroment
#install the requirements.txt file by using pip

#### RUNNING THE PROGRAM #####
To  run this you run two files,run the < main_program.py >
At the same time run the < stream_listener.py > this fetches tweets from the db and runs the analysis to give an output of depressed or not depressed

### File descriptions ###
credentials.py - Has the credentials used to access our twitter api
database_connection.py - Connects to our database on aws and ensures our table exists
depression_visualization.ipynb - its the notebook version that fetch,analyses and displays the output of our tweets
main_program.py -,this analyses our tweets through our model and clasifies them
main.ipynb - notebook for connecting to the twitter api and fetching tweets
preprocessing_for_db.py - this has functions to process the raw tweets before they are stored in the database
preprocessing_for_model.py - this has functions to process our tweets from the db before they are fed into our model
requirements.txt - has all the dependencies used to setup this project
settings.py - has settings for our table that we use in the database,such as tablenames,columns etc
stream_listener_class.py - contains settings used to develop our streamlistener class
stream_listener.py - its the program we run to listen for tweets through the api and saves them to our db
testfile.sav - this is our first classification model
