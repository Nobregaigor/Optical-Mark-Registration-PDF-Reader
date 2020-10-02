import pandas as pd
import pathlib

def read_emails_list(list_path):
  ext = pathlib.Path(list_path).suffix
  if ext in [".xlsx", ".xls"]:
    df = pd.read_excel(list_path)
  elif ext == ".csv":
    df = pd.read_csv(list_path)
  else:
    print("Sorry, could not read emails list. Please check file format.")
  return df