from .functions.send_email import *

def test_email_with_default_data(*args, **kwargs):
  sender = args[0]["sender_email"]
  password = args[0]["password"]
  file = args[0]["test_file"]
  
  default_data = {
    "quiznumber": "TEST",
    "studentname": "Igor"
  }

  (header, body) = format_email(default_data)

  email_data = {
    "header": header,
    "body": body,
    "receiver": "noreply.teamcelestin@gmail.com",
    "filename": file
  }
  send_email(email_data, sender, password)
  
