# Sender

Email sender microservice


This is a proof of concept. A RESTful microservice to send e-mails using gmail credentials.


### Configuration

#### Credentials

```bash
cp conf.py.template conf.py
```

And fill all variables.


#### To install dependencies:

```bash
pip install -r requirements.txt
```

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
Determines if email should be sended in the same moment or not.


__Body (json)__:

```
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

To send a created email

You can send an email passing 'true' to autosend parameter when creating.