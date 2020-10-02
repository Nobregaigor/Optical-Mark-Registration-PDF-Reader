

import click
import webbrowser

# from ..cli import console_log as log
# from .. import console_log as log

from .. import get_unumber_from_pdf, get_email_from_pdf, rename_pdf_files_with_email, test_email_with_default_data, send_graded_quizzes_emails

#! =========================================
#! Setting up click
#! =========================================

#! - - - - - - - - - - - - - - - - - - - - -
#! Main click group


@click.group()
def main():
    pass

#! - - - - - - - - - - - - - - - - - - - - -
#! Run subgroup


@main.group(short_help="Executes a given command. Ask 'run --help' to learn more.", help="Executes one of the commands listed below.")
def run():
    pass

# read_pdf


@run.command(short_help="Checks the u-number recognized by the OMR algorithm.")
@click.option("--input-file", '-i', type=click.Path(exists=True, dir_okay=False), help="Input pdf file with data code to be read.")
def check_unumber(**kargs):
    unumber = get_unumber_from_pdf(kargs)
    return unumber

@run.command(short_help="Checks the email associated with the pdf file by using the u-number obtained by the algorithm.")
@click.option("--input-file", '-i', type=click.Path(exists=True, dir_okay=False), help="Input pdf file with data code to be read. ")
@click.option("--emails-list", '-e', type=click.Path(exists=True, dir_okay=False), help="Input file with list of unumbers (first column) and emails (second column). It can be a excel or csv format.")
def check_email(**kargs):
    return get_email_from_pdf(kargs)


@run.command(short_help="Copies and renames a set of PDF files in a given directory to a new one.")
@click.option("--pdfs-dir", '-p', type=click.Path(exists=True, dir_okay=True, file_okay=False), help="Path to directory that contains all pdf files to be renamed")
@click.option("--emails-list", '-e', type=click.Path(exists=True, dir_okay=False), help="Input file with list of unumbers (first column) and emails (second column). It can be a excel or csv format.")
@click.option("--out-dir", '-o', type=click.Path(exists=True, dir_okay=True, file_okay=False), help="Output directory. If not provided, will create a sub-directory on pdfs dir.")
def rename_pdfs(**kargs):
    return rename_pdf_files_with_email(kargs)


@run.command(short_help="Test the send email function with a set of default parameters.")
@click.option("--test-file", '-f', type=click.Path(exists=True, dir_okay=False), help="Test file to be sent ")
@click.option("--sender-email", '-s', type=str, help="Sender email.")
@click.option("--password", '-p', type=str, help="Sender password.")
def test_email(**kargs):
    return test_email_with_default_data(kargs)


@run.command(short_help="Send emails from an excel file with email and confidence score. Files must be names with the email name before @.")
@click.option("--sender-email", '-s', type=str, help="Sender email.")
@click.option("--password", '-p', type=str, help="Sender password.")
@click.option("--pdfs-dir", '-d', type=click.Path(exists=True, dir_okay=True, file_okay=False), help="Path to directory that contains all pdf files to be renamed")
@click.option("--emails-list", '-e', type=click.Path(exists=True, dir_okay=False), help="Input file with list of unumbers (first column) and emails (second column). It can be a excel or csv format.")
@click.option("--quiz-number", '-n', type=str, help="Quiz number.")
@click.option("--min-confd-score", '-m', type=str, help="Min confidence score required to send email. Default is 0.85.")
def send_emails(**kargs):
    return send_graded_quizzes_emails(kargs)