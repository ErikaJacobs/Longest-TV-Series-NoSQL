# A NoSQL Database of TV Show Episode Data
This project scrapes data from a Wikipedia table for [longest running scripted U.S. primetime television series](https://en.wikipedia.org/wiki/List_of_longest-running_scripted_U.S._primetime_television_series), and pulls episode information for those shows from a television API through TV Maze. This project then organizes this data with an appropriate key/value structure, and uploads the data to DynamoDB, an AWS NoSQL database.

## Methods Used
* Web Scraping
* API Connection
* Aggregation

## Technologies Used
* Python
* DynamoDB

## Packages Used
* Requests
* Boto3

## How To Run

##### *AWS Credentials*
AWS Credentials will need to be saved locally in the .aws directory of an operating system in order for this project to successfully run. [Click here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) to learn more about this process.
##### *Install Requirements and Run*
On the command line of your operating system, navigate to the repository directory (ideally using a Python virtual environment).

Run the following code on the command line to install requirements:
```
pip install -r requirements.txt 
```

Run the following code on the command line to run this project:
```
Python main.py
```

# Featured Scripts or Deliverables
* [```main.py```](main.py)

# Sources
* [TV Maze API](https://www.tvmaze.com/api)
* [Wikipedia list of longest running scripted U.S. primetime television series](https://en.wikipedia.org/wiki/List_of_longest-running_scripted_U.S._primetime_television_series)
* [DynamoDB - Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.03.html)
