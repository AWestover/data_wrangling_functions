# functions to help with email sending and parsing


# libraries
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
import configparser as cp
import time


# functions


# takes text and moves every letter up by a standard key
def caesar_shifter(message, key):
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    new_message = ''
    used = False
    for char in message:
        for k in range(0, len(alphabet)):
            if char.lower() == alphabet[k]:
                new_message += alphabet[(k + int(key)) % len(alphabet)]
                used = True
        if not used:
            new_message += char
    return new_message


# for easy selection of a config file
def get_config(env):
    c_config = cp.ConfigParser()
    if env == "DEV":
        c_config.read(['config/development.cfg'])
    # I could have a separate config for my real email and my fake one but i don't at the moment
    elif env == "PROD":
        c_config.read(['config/production.cfg'])
    return c_config


# send mail easily
def mail(from_who: str, password: str, to_who: list, subject: str, text: str, attach=None):
    # basic program for now, improve later
    msg = MIMEText(text)

    msg['From'] = from_who  # config.get('email', 'user')
    msg['To'] = ", ".join(to_who)
    msg['Subject'] = subject

    mail_server = smtplib.SMTP("smtp.gmail.com", 587)
    mail_server.ehlo()
    mail_server.starttls()
    mail_server.ehlo()
    mail_server.login(from_who, password)
    mail_server.sendmail(from_who, to_who, msg.as_string())
    mail_server.close()
    print("Your message was sent")
    print("To: ", ", ".join(to_who))
    print("Subject: " + subject)
    print("Message: " + text)
    print("Good thing you didn't have to send that message yourself!\n")


# parses out the text of a message!
def get_text(msg):
    if msg.is_multipart():
        return get_text(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)


# Responds to all of your emails and then deletes them
def respond_all(unm: str, pwd: str):
    # Get the first email in your inbox with imaplib, more elaborate functions can be created later
    msrvr = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    msrvr.login(unm, pwd)
    msrvr.select('inbox')
    result, data = msrvr.search(None, "ALL")
    ids = data[0]  # data is a list.
    id_list = ids.split()  # ids is a space separated string

    for an_id in id_list:
        result, data = msrvr.fetch(an_id, "(RFC822)")
        cur_email = data[0][1]
        cur_msg = email.message_from_bytes(cur_email)
        sender = cur_msg['From']
        old_subject = cur_msg['Subject']
        message = get_text(cur_msg).decode("UTF-8")
        message = caesar_shifter(message, 1)
        message += "\nPS, I didn't find your email interesting. \n-From, Com Puter"
        if sender != unm:
            mail(my_user, my_pwd, [sender], old_subject, message)

    typ, data = msrvr.search(None, "ALL")
    for num in data[0].split():
        msrvr.store(num, '+FLAGS', '\\Deleted')
    msrvr.expunge()

    msrvr.close()
    msrvr.logout()
    print("Your messages were responded to and deleted\n")



print(get_config("DEV").get('email', 'user'))
time.sleep(3)
# use config to get user and pwd
config = get_config("DEV")
my_user = config.get('email', 'user')
my_pwd = config.get('email', 'password')
server = False

print("Checking your emails")
if server:
    while True:
        try:
            respond_all(my_user, my_pwd)
        except:
            print("YOUR EMAIL WAS NOT SENT")
            print("Fatal error")
            print("Your lucky im still alive")
        time.sleep(10)
else:
    try:
        for i in range(0, 5):
            respond_all(my_user, my_pwd)
            time.sleep(60)
    except:
        print("YOUR EMAIL WAS NOT SENT")
        print("Fatal error")
        print("Your lucky im still alive")

