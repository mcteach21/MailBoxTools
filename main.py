from classes.MailClient import MailClient
from classes.Menu import Menu
from classes.Option import Option


def print_msg(msg):
    print('***************************************')
    print(f'{msg}')
    print('***************************************')


def read():
    mc.read()
    print_msg('Résultat : {}'.format(len(mc.mails)) + ' mail(s).')


def clean():
    print('Nettoyer mails..')
    mc.delete()


def connect_server():
    global mc
    login = input('login : ')
    password = input('password : ')
    mc = MailClient(0, login, password)


# def test():
#     print('tests..')


if __name__ == '__main__':
    print_msg('Ma Boite Mail')

    connect_server()
    menu = Menu([
        Option('Boite Mail : Lire!', read),
        Option('Boite Mail : Nettoyer!', clean)
        # , Option('Tests', test)
    ])
    while not menu.want_exit:
        menu.show()
