# Sender

Email sender microservice


This is a proof of concept. A RESTful microservice to send e-mails using smtp credentials.


### Configuration

#### Credentials

It's necessary to create the `.env` file:

```bash
cp .env.template .env
```

And fill all variables.


#### To run the webserver:

```bash
docker-compose up --build
```



### Using

#### To list all created emails:

```
GET to http://0.0.0.0:3000/emails/
```

Returns a list of all e-mails.


#### To create an email:

```
POST to http://0.0.0.0:3000/emails/
```

__Parameters__:

```
autosend: true|false
```
Determines if email should be sent in the same moment or not.


__Body (json)__:

```json
{
  "subject": "Hi!",
  "text_message": "This is my first e-mail using sender webservice!"
}
```

__Headers__:

```
"Content-type": "application/json"
```


#### To send an email:

You can send an email passing 'true' to autosend parameter when creating it.

If you need to send an email which is already created, you should do:
```
POST to http://0.0.0.0:3000/emails/<int:email_id>/send
```


#### To run the tests:

Execute next lines from src:

```bash
pytest --cov=. --flake8 tests/
```
