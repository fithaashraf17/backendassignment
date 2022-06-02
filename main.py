from src.interface import UserInterface


def main():
    """
    Main code for mycart
   """
    ui = UserInterface()
    print('*' * 110)
    splash = '''
                                   __  ___     _____         __ 
                                  /  |/  /_ __/ ___/__ _____/ /_
                                 / /|_/ / // / /__/ _ `/ __/ __/
                                /_/  /_/\_, /\___/\_,_/_/  \__/ 
                                       /___/                           
       '''
    print(splash)
    print('*' * 110)
    print("Please login to continue\n")
    username = input("Username: ")
    password = input("Password: ")

    user = ui.user_act.login(username, password)

    if user:
        if user.username == 'admin':
            ui.title("Welcome Admin")
            ui.admin_ui()
        else:
            ui.title('WELCOME %s' % username)
            ui.user_act.username = username
            ui.user_act.get_user_id()
            # start ui
            ui.user_ui()
    else:
        print("Invalid login, please try again")


if __name__ == '__main__':
    main()
