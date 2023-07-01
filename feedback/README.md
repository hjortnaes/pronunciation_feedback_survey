# pronunciation_feedback_survey

## Testing
Open a console, navigate to feedback, and run:

`python3 -m flask --app index run --debug`

Open in your browser: 

`http://127.0.0.1:5000`

## Secrets
Create a python file called `secret.py` in the feedback directory

The file should contain a string `SECRET_KEY` with any contents.
Note this should be a proper key in production.
