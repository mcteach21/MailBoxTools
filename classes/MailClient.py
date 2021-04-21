import datetime
import email
import imaplib  # Library to interact with IMAP server

from classes.Mail import Mail


class MailClient:
    IMAP_Servers = ['imap.mail.yahoo.com', 'imap.gmail.com']

    def __init__(self, imap_server_id, email_login, email_password):

        imap_server = self.IMAP_Servers[imap_server_id]
        self.imap = imaplib.IMAP4_SSL(imap_server)
        self.mails = []

        print('Connection au server..{}'.format(imap_server))
        self.logged = self.connect(email_login, email_password)

    def connect(self, email_login, email_password):
        try:
            status, summary = self.imap.login(email_login, email_password)
            if status == "OK":
                print('Connection effectuée avec succès!')
                return True
        except imaplib.IMAP4.error:
            print('Error Connection au serveur!')  # str(imaplib.IMAP4.error)
        return False

    def logout(self):
        self.imap.close()
        self.imap.logout()

    def delete(self, to_trash=False):
        # if to_trash:
        #     self.imap.uid('STORE', msg_num, '+X-GM-LABELS', '\\Trash')
        # else:
        self.read(False)

        if len(self.mails) == 0:
            print("Aucun mail trouvé!")
        else:
            nb = len(self.mails)
            print("%d email(s) trouvé(s).." % nb)

            yes_no = input('Etes-vous sûr de vouloir Supprimer ces %d mails [o/N]? : ' % nb)
            if yes_no == 'o':
                for mail in self.mails:
                    print('supprimer mail..{}'.format(mail.num))
                    self.imap.store(mail.num, "+FLAGS", "\\Deleted")
                print("%d email(s) supprimé(s)!" % nb)

    def read(self, display=True):
        if not self.logged:
            print('Aucune connection au serveur!')
            return

        self.mails = []
        print('Lecture mails..')
        status, data = self.imap.select("Inbox")
        msg_count = int(data[0])
        # print('messages count : {}'.format(msg_count))

        from_filter = input('Expéditeur (filtre) : ') or 'ALL'
        # emails_params = {
        #     'from_filter': from_filter,
        # }

        date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
        # status, data = self.imap.search(None, ('UNSEEN'), '(SENTSINCE {0})'.format(date),
        #                                 '(FROM {0})'.format(from_filter.strip()))
        status, data = self.imap.search(None, '(SENTSINCE {0})'.format(date), '(FROM {0})'.format(from_filter.strip()))
        if status != 'OK':
            print('Aucun mail trouvé!')

        print('***************************************')
        msgs_ids = data[0].split()
        print('Nombre mails : {} (/{})'.format(len(msgs_ids), msg_count))
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

            if display:
                print(str(num) + ' ' + msg_date_formatted + ' - [' + msg_from + '] : ' + msg_subject)

