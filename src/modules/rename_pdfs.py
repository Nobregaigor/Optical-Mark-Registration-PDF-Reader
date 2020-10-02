

from .functions import rename_files_with_email


def rename_pdf_files_with_email(*args, **kwargs):
  pdfs_dir = args[0]["pdfs_dir"]
  emails_list_file = args[0]["emails_list"]
  out_dir = args[0]["out_dir"]
  rename_files_with_email(pdfs_dir, emails_list_file, out_dir)

# AvocadoToast123!
  