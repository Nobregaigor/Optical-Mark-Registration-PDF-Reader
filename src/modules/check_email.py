from .functions import read_pdf, read_emails_list

def get_email_from_pdf(*args, **kwargs):
    input_file = args[0]["input_file"]
    emails_list_file = args[0]["emails_list"]

    emails_df = read_emails_list(emails_list_file)
    (u_data, conf, conf_per_n) = read_pdf(input_file)

    unumber = int("".join([str(v) for v in u_data]))
    email = emails_df.loc[emails_df["UNUMBER"] == unumber]    
    print(email)
    return email

    
    
