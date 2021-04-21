from classes.MailClient import MailClient
from classes.Menu import Menu
from classes.Option import Option


def print_msg(msg):
    print('***************************************')
    print(f'{msg}')
    print('***************************************')


def read():
    from_filter = input('from filter : ') or 'ALL'
    emails_params = {
        'from_filter': from_filter,
    }
    mc.read(emails_params)
    print_msg('Résultat : {}'.format(len(mc.mails)) + ' mail(s).')


def clean():
    print('clean mails..')
    mc.delete()


def connect_server():
    global mc
    login = input('login : ')
    password = input('password : ')
    mc = MailClient(0, login, password)


def test():
    print('tests..')


if __name__ == '__main__':
    print_msg('Mails Tools')

    connect_server()
    menu = Menu([
        Option('Read Mails', read),
        Option('Clean Mails', clean),
        Option('Tests', test)
    ])
    while not menu.want_exit:
        menu.show()
