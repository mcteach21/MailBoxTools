from termcolor import colored


class Menu:
    menu_color = 'yellow'
    want_exit = False

    def __init__(self, options):
        self.options = options

    def show(self):
        print(colored("************** Menu *******************", self.menu_color))
        num = 1
        for option in self.options:
            print(colored(str(num) + '- ' + option.text, self.menu_color))
            num = num + 1
        print(colored(str(num) + '- Quitter!', self.menu_color))
        print(colored("***************************************", self.menu_color))

        try:
            num = int(input('choice (1-{}) ==> '.format(len(self.options))))
            self.handle_input(num)
        except:
            self.init()

    def error(self, mess):
        print(colored("(x) " + mess + "! try again.", 'red'))

    def init(self):
        self.show()

    def handle_input(self, num):
        if num > len(self.options):
            func = lambda: print("Bye!")
            self.want_exit = True
        else:
            func = self.options[num-1].func
            # print("(!) func (exec0.) ==> " + func.__name__)
        return func()
