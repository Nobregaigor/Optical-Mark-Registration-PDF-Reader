from .find_files import find_files
from .read_emails_list import read_emails_list
from .read_pdf import read_pdf
import pandas as pd
from os import mkdir
from os.path import join, isdir
import shutil
import click
import time

def rename_files_with_email(path_to_pdfs, path_to_emails_list, out_dir):

  emails_list = read_emails_list(path_to_emails_list).to_dict('records')
  files = find_files(path_to_pdfs, ("fileFormat", "pdf"))

  if out_dir == None:
    out_dir = join(path_to_pdfs, "renamed_output")

  out_matched = join(out_dir, "matched")
  out_unmatched = join(out_dir, "not_matched")

  for p in [out_dir, out_matched, out_unmatched]:
    if isdir(p) == False:
      mkdir(p)

  unumbers_dict = dict()
  u_e = []

  fill_char = click.style('=', fg='yellow')
  with click.progressbar(range(len(files)), label='Processing pdfs...', fill_char=fill_char) as bar:
    for i, (fp, ff, fn) in enumerate(files):
      (u_data, conf, conf_per_n) = read_pdf(fp)
      unumber = int("".join([str(v) for v in u_data]))

      u_e.append((unumber, fn))
      unumbers_dict[unumber] = (unumber, conf, fn, fp)
      bar.update(i)
    bar.finish()
  
  fill_char = click.style('=', fg='yellow')
  with click.progressbar(range(len(emails_list)), label='Cpyping and Renaming files...', fill_char=fill_char) as bar:
    for i, student in enumerate(emails_list):
      if student["UNUMBER"] in unumbers_dict:
        pdf_data = unumbers_dict[student["UNUMBER"]]
        student["MATCH"] = True
        student["CONFD"] = pdf_data[1]
        new_filename = student["EMAIL"].split("@")[0]
        new_filepath = join(out_matched, new_filename + ".pdf")
        shutil.copyfile(fp, new_filepath)
      else:
        student["MATCH"] = False
        student["CONFD"] = 0.0
        new_filepath = join(out_unmatched, fn + ".pdf")
        shutil.copyfile(fp, new_filepath)
      bar.update(i)
      time.sleep(0.002)
    bar.finish()
  
  rename_log_file_path = join(out_dir, "renamed_log.xlsx")
  emails_df = pd.DataFrame.from_records(emails_list)
  emails_df = emails_df.sort_values(by=['MATCH', 'CONFD'], ascending=False)
  emails_df.to_excel(rename_log_file_path)

