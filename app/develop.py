from bot_classes import DriverManager, HaddanBot
from constants import FIRST_CHAR, PASSWORD


def start_game():
    client = DriverManager()
    client.options.add_argument('--start-maximized')
    client.options.add_experimental_option("detach", True)

    client.start_driver()

    user = HaddanBot(
        char=FIRST_CHAR,
        password=PASSWORD,
        driver=client.driver
    )
    user.login_to_game()
    return client, user


if __name__ == '__main__':
    client, user = start_game()
    client.try_to_switch_to_central_frame()
    client.save_url_content()
