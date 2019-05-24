# twitter-cli
Python CLI fetching data on Twitter

##Configuration

- Create virtualenv running the following command:
```make venv```
- Setup your Docker Postgres image for testing by running:
```sh docker-init.sh```
(Note: this will install Docker if not already installed on your computer, pull the Postgres image if needed, and run 
it with the credentials set in config.ini)
- Fill in your Twitter API credentials in config.ini
- Run ```source venv/bin/activate``` to activate your venv 
- You're good to go !

## How to

The CLI can be used the following way:
```
python3 main.py fetch --user userName --n 30
```

## Twitter data model

The nature of Twitter's data model seems to make an interesting use case for using
a graph database such as Neo4j.

The following chart represents the way entities relationships could be structured in
such a database.

![data-model-example](twitter-data-model.png?raw=true "Twitter Graph Data Model Example")

## Next steps

- Extract user data from user JSON field of each tweet, create SQLAlchemy User model
and store information in a new 'users' table

- Define one-to-many relationship between User and Tweet objects

- Parse tags/hashtags, create models for them and define relationships to other objects

