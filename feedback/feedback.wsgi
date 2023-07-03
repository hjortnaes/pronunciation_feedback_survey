#!/usr/bin/python
import sys
import logging
import secret
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/nhjortn/pronunciation_feedback_survey/feedback/")

from index import app as application
application.secret_key = secret.SECRET_KEY
