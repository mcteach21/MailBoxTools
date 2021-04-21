import datetime
import email
import imaplib  # Library to interact with IMPAP server

from classes.Mail import Mail


class MailClient:
    IMAP_Servers = ['imap.mail.yahoo.com', 'imap.gmail.com']

    def __init__(self, imap_server_id, email_login, email_password):

        imap_server = self.IMAP_Servers[imap_server_id]
        self.imap = imaplib.IMAP4_SSL(imap_server)
        self.mails = []

        print('connecting to server..{}'.format(imap_server))
        self.logged = self.connect(email_login, email_password)

    def connect(self, email_login, email_password):
        try:
            status, summary = self.imap.login(email_login, email_password)
            if status == "OK":
                print(summary)
                print('connection success!')
                return True
        except imaplib.IMAP4.error:
            print('Error Loging to server!')  # str(imaplib.IMAP4.error)
        return False

    def logout(self):
        self.imap.close()
        self.imap.logout()

    def delete(self, to_trash=False):
        # if to_trash:
        #     # self.imap.uid('STORE', msg_num, '+X-GM-LABELS', '\\Trash')
        #     pass
        # else:

        from_filter = input('from filter : ') or 'ALL'
        emails_params = {
            'from_filter': from_filter,
        }
        self.read(emails_params)

        if len(self.mails) == 0:
            print("Aucun mail trouvé!")
        else:
            nb = len(self.mails)
            print("%d email(s) trouvé(s).." % nb)

            yes_no = input('Etes-vous sûr de vouloir Supprimer ces %d mails [o/N]? : ' % nb)
            print('yes_no = {}'.format(yes_no))

            if yes_no == 'o':
                for mail in self.mails:
                    print('delete..{}'.format(mail.num))
                    # self.imap.store(mail.num, "+FLAGS", "\\Deleted")
                print("%d email(s) supprimé(s)!" % nb)

    def read(self, emails_params):
        if not self.logged:
            print('not logged! cannot read.')
            return

        self.mails = []
        print('reading mails..')
        status, data = self.imap.select("Inbox")
        msg_count = int(data[0])
        # print('messages count : {}'.format(msg_count))

        from_filter = emails_params['from_filter']
        print('from_filter = '+from_filter)

        date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")

        # status, data = self.imap.search(None, ('UNSEEN'), '(SENTSINCE {0})'.format(date),
        #                                 '(FROM {0})'.format("Groupon".strip()))
        status, data = self.imap.search(None,  '(SENTSINCE {0})'.format(date), '(FROM {0})'.format("Groupon".strip()))
        if status != 'OK':
            print('No messages found!')

        print('***************************************')
        msgs_ids = data[0].split()
        print('Nb. emails : {} (/{})'.format(len(msgs_ids), msg_count))
        print('***************************************')

        msgs_ids = sorted(msgs_ids, reverse=True)

        for num in msgs_ids:
            status, data = self.imap.fetch(num, '(RFC822)')
            if status != 'OK':
                print('Erreur lecture mail : ', num)

            msg = email.message_from_bytes(data[0][1])
            msg_from = msg['From']
            try:
                hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
                msg_subject = str(hdr)
            except TypeError:
                msg_subject = 'None'

            msg_date = email.utils.parsedate_tz(msg['Date'])
            msg_date_formatted = '?'
            if msg_date:
                local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(msg_date))
                msg_date_formatted = local_date.strftime("%d-%m-%Y %H:%M")

            self.mails.append(Mail(num, msg_date, msg_from, msg_subject, '..'))
            print(str(num) + ' ' + msg_date_formatted + ' - [' + msg_from + '] : ' + msg_subject)

            # if msg.is_multipart():
            #     for part in msg.walk():
            #         type = part.get_content_type()
            #         disp = str(part.get('Content-Disposition'))
            #         # look for plain text parts, but skip attachments
            #         if type == 'text/plain' and 'attachment' not in disp:
            #             charset = part.get_content_charset()
            #             # decode the base64 unicode bytestring into plain text
            #             body = part.get_payload(decode=True).decode(encoding=charset, errors="ignore")
            #             # if we've found the plain/text part, stop looping thru the parts
            #
            #             print(body)
            #             break
            # else:
            #     # not multipart - i.e. plain text, no attachments
            #     charset = msg.get_content_charset()
            #     body = msg.get_payload(decode=True).decode(encoding=charset, errors="ignore")
            #     print('====================================')
            #     print(body)
            #     print('====================================')
