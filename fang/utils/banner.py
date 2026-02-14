from colorama import Fore, Style, init #type: ignore

init(autoreset=True)


def banner():
    ascii_art = r"""
 ________________   _______    ________
 \_   _____/ _  \   \      \  /  _____/
 |    __)/  /_\  \  /   |   \/   \  ___
 |     \/    |    \/    |    \    \_\  \
 \___  /\____|__  /\____|__  /\______  /
     \/         \/         \/        \/
                """

    print(Fore.RED + ascii_art + Style.RESET_ALL)
    print(Fore.CYAN + "Automated Cyber Security Tool" + Style.RESET_ALL)
    print(Fore.YELLOW + (
        "--------------------------------------------------\n"
        "[!] CAUTION:\n"
        "    This tool is intended for EDUCATIONAL and\n"
        "    AUTHORIZED security testing only.\n"
        "    Unauthorized use against systems you do not\n"
        "    own or have explicit permission to test is ILLEGAL.\n\n"
        "Author : YourName\n"
        "Version: 1.0.0\n"
        "Use responsibly.\n"
        "--------------------------------------------------"
    ) + Style.RESET_ALL)
