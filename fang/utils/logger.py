from colorama import Fore, Style, init

init(autoreset=True)

class Logger:

    @staticmethod
    def info(msg: str):
        print(f"{Fore.CYAN}[*]{Style.RESET_ALL} {msg}")

    @staticmethod
    def success(msg: str):
        print(f"{Fore.GREEN}[+]{Style.RESET_ALL} {msg}")

    @staticmethod
    def warning(msg: str):
        print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} {msg}")

    @staticmethod
    def error(msg: str):
        print(f"{Fore.RED}[-]{Style.RESET_ALL} {msg}")

    @staticmethod
    def result(key: str, value):
        print(f"{Fore.MAGENTA}[>]{Style.RESET_ALL} {key}: {value}")