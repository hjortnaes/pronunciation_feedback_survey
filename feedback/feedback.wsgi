#!/home/nhjortn/pronunciation_feedback_survey/venv/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/nhjortn/pronunciation_feedback_survey/venv/lib/python3.8/site-packages/")
sys.path.insert(0,"/home/nhjortn/pronunciation_feedback_survey/feedback/")

from index import app as application
application.secret_key = '6f6a0e2e01e09f021bf449a4f64c6cdfd62b5a30b188dcac307f471dd14f0a9b' 
