import yagmail

header = "Your Graded Quiz ${QUIZNUMBER} from EGN3343"
body = """
<body>
  <h1> Hello ${STUDENTNAME}, </h1>
  <p> Here is your freshly-graded thermo quiz. </p>
</body>
<footer>
<p> Have a great day! <br> Your friendly neighborhood themo professor (and TAs!) </p>
</footer>
"""

def get_email_password():
  password = input("Type your password and press enter: ")
  return password

def get_email_sender():
  email = input("Type the sender email and press enter: ")
  return email

def get_email_sender_and_password():
  email = get_email_sender()
  password = get_email_password()
  return (email, password)

def format_email(data):
  h = header.replace("${QUIZNUMBER}", data["quiznumber"])
  b = body.replace("${STUDENTNAME}", data["studentname"])
  return (h, b)

def send_email(email_data, sender=None, password=None):
  if sender == None:
    sender = get_email_sender()
  if password == None:
    password = get_email_password()
  
  yag = yagmail.SMTP(sender,password)
  try:
    yag.send(
        to=email_data["receiver"],
        subject=email_data["header"],
        contents=email_data["body"], 
        attachments=email_data["filename"],
    )
    return 0
  except:
    print("Could not send email")
    return -1