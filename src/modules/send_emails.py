from .functions.send_email import *
from .functions import send_pdfs_from_dir

def send_graded_quizzes_emails(*args, **kwargs):
  sender = args[0]["sender_email"]
  password = args[0]["password"]
  pdfs_dir = args[0]["pdfs_dir"]
  emails_list_file = args[0]["emails_list"]
  quiz_number = args[0]["quiz_number"]
  min_score = args[0]["min_confd_score"]

  send_pdfs_from_dir(sender, password, pdfs_dir, emails_list_file, quiz_number, min_score)
  
