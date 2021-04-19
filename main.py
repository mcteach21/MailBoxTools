import datetime
import email

from classes.MailClient import MailClient
from classes.Menu import Menu
from classes.Option import Option


def print_msg(msg):
    print('***************************************')
    print(f'{msg}')
    print('***************************************')


def read():
    from_filter = input('from filter : ')
    mc.read('FROM ' + from_filter)
    print_msg('Résultat : {}'.format(len(mc.mails)) + ' mail(s).')

    mail = mc.mails[38]
    print(mail.num)
    # date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(mail.email_date)).strftime("%d-%m-%Y %H:%M")
    # print(date + ' - [' + mail.email_from + '] : ' + mail.email_subject)


def clean():
    print('clean mails..')
    msg_num = input('num message to delete : ')
    mc.delete(msg_num)


def connect_server():
    global mc

    login = input('login : ')
    password = input('password : ')
    mc = MailClient(0, 'yasmineouared@yahoo.fr', 'ldftmlvhkhswbvwe')


if __name__ == '__main__':
    print_msg('Mails Tools')
    connect_server()

    menu = Menu([
        Option('Read Mails', read),
        Option('Clean Mails', clean)
    ])
    while not menu.want_exit:
        menu.show()
