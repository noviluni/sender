from api import create_app
from config import DEBUG


app = create_app()
app.run(port=3000, host='0.0.0.0', debug=DEBUG)
