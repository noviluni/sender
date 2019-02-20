# Sender

Email sender microservice


This is a proof of concept. A RESTful microservice to send e-mails using smtp credentials.


### Configuration

#### Credentials

It's necessary to create the `.env` file:

```bash
cp .env.template .env
```

And fill `DEFAULT_TO_ADDRESS`, `FROM_ADDRESS` and `EMAIL_PASSWORD` variables.


#### To build the image:

```bash
make build
```

#### To run the webserver:

```bash
make up
```


### Using

#### To list all created emails:

```
GET to http://0.0.0.0:3000/emails/
```

Returns a list of all created e-mails.

__URL parameters__:

```
limit: int (optional)
```

Determines the number of emails that should be shown. Default value is 10 and can be changed setting `DEFAULT_LIMIT` in the `.env` file.


```
sent: true|false (optional)
```

Allow to filter emails according if they have been sent or not.


__Example__:

Request:
```
GET to http://0.0.0.0:3000/emails/?limit=10
```

Response:

```json
[
  {
    "created_at": "2019-02-03 20:48:44.573069",
    "from_address": "test@test.com", 
    "html_message": null, 
    "id": 1, 
    "retries": 1, 
    "sent": true, 
    "sent_at": "2019-02-03 20:48:53.534887", 
    "subject": "Test 1", 
    "text_message": "Just testing the sender app", 
    "to_address": "example@example.com"
  }, 
  {
    "created_at": "2019-02-03 21:07:04.140945", 
    "from_address": "test@test.com", 
    "html_message": null, 
    "id": 2, 
    "retries": 1, 
    "sent": true, 
    "sent_at": "", 
    "subject": "Test 2", 
    "text_message": "Another example", 
    "to_address": "example@example.com"
  }
]
```


#### To see the detail of a created email:

```
GET to http://0.0.0.0:3000/emails/
```

Returns a list of all created e-mails.

Example:


__Example__:

Request:
```
GET to http://0.0.0.0:3000/emails/1/
```

Response:
```json
  {
    "created_at": "2019-02-03 20:48:44.573069",
    "from_address": "test@test.com",
    "html_message": null,
    "id": 1,
    "retries": 1,
    "sent": true,
    "sent_at": "2019-02-03 20:48:53.534887",
    "subject": "Test 1",
    "text_message": "Just testing the sender app",
    "to_address": "noviluni@gmail.com"
  }
```


#### To create an email:

```
POST to http://0.0.0.0:3000/emails/
```

__URL parameters__:

```
autosend: true|false (optional)
```
Determines if email should be sent in the same moment or not.


__Body (json)__:

It should include: `subject`, `text_message`.

It can, optionally, include:  `to_address`, `subject`, `text_message`, `html_message`.


__Headers__:

```
"Content-type": "application/json"
```


__Example__:

Request:
```
POST to http://0.0.0.0:3000/emails/
```

Body:
```json
  {
    "subject": "Hi!",
    "text_message": "This is my first e-mail using sender webservice!"
  }
```

Response:

```json
  {
    "id": 3,
    "sent": true
  }
```


#### To send an email:

You can send an email passing `true` to `autosend` parameter when creating it.

If you need to send an email which is already created, you should:
```
POST to http://0.0.0.0:3000/emails/<int:email_id>/send
```


__Example__:

Request:
```
POST to http://0.0.0.0:3000/emails/1/send
```

Response:

```json
  {
    "id": 1,
    "sent": true
  }
```


### Testing

To build the test image:
```bash
make build-test
```


To run tests:

```bash
make test
```
