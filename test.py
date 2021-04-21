import imaplib

if __name__ == '__main__':
    imap = imaplib.IMAP4_SSL('imap.mail.yahoo.com')
    try:
        pwd = input('password : ')
        status, summary =  imap.login('yasmineouared@yahoo.fr', '')
        if status == "OK":
            print(summary)
            print('connection success!')
    except imaplib.IMAP4.error:
        print('Error Loging to server!')
