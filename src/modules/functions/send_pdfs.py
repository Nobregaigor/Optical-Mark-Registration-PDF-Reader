from .find_files import find_files
from .read_emails_list import read_emails_list
import pandas as pd
from os.path import join, isfile
import click
import time
from .send_email import *

def send_pdfs_from_dir(sender, password, path_to_pdfs, path_to_emails_list, quiz_number, minscore):

  emails_list = read_emails_list(path_to_emails_list).to_dict('records')
  # files = find_files(path_to_pdfs, ("fileFormat", "pdf"))

  if minscore == None:
    minscore = 0.85
  else:
    minscore = float(minscore)
  
  fill_char = click.style('=', fg='yellow')
  with click.progressbar(range(len(emails_list)), label='Sending emails...', fill_char=fill_char) as bar:
    for i, student in enumerate(emails_list):
      if student["MATCH"] == True and student["CONFD"] >= minscore:
        email = student["EMAIL"]
        name = student["NAME"]
        
        # check if file exists
        pdf_file_path = join(path_to_pdfs, email.split("@")[0] + ".pdf" )
        if isfile(pdf_file_path) == False:
          student["EMAIL-SENT"] = False
          continue

        # format email text
        email_text_data = {
          "quiznumber": quiz_number,
          "studentname": name
        }
        (header, body) = format_email(email_text_data)

        # set email data
        email_data = {
          "header": header,
          "body": body,
          "receiver": email,
          "filename": pdf_file_path
        }

        # try to send email
        res = send_email(email_data, sender, password)
        if res == -1:
          student["EMAIL-SENT"] = False
        else:
          student["EMAIL-SENT"] = True

      else:
        student["EMAIL-SENT"] = False

      bar.update(i)
      time.sleep(0.002)
    bar.finish()
  
  # rename_log_file_path = join(out_dir, "renamed_log.xlsx")
  emails_df = pd.DataFrame.from_records(emails_list)
  emails_df = emails_df.sort_values(by=['EMAIL-SENT','MATCH', 'CONFD'], ascending=False)
  emails_df.to_excel(path_to_emails_list)

