from colorama import Fore, Style, init  # type: ignore
from .ip_data import IPData
from datetime import datetime
import shutil, re
from config.settings import VERSION

init(autoreset=True)

ip_v4 = IPData.ipv4()
ip_v6 = IPData.ipv6()

C=Fore.CYAN; Y=Fore.YELLOW; G=Fore.GREEN; LR=Fore.LIGHTRED_EX
LW=Fore.LIGHTWHITE_EX; DIM=Style.DIM; RESET=Style.RESET_ALL; BRIGHT=Style.BRIGHT
LB=Fore.LIGHTBLUE_EX; R=Fore.RED

_ANSI = re.compile(r'\x1b\[[0-9;]*m')
def _w():     return shutil.get_terminal_size((100, 30)).columns
def _vlen(s): return len(_ANSI.sub('', s))
def hline():  return DIM + C + "─" * _w() + RESET
def center(text):
    pad = max(0, (_w() - _vlen(text)) // 2)
    return " " * pad + text

def row(label, value, value_color=LW):
    bracket = BRIGHT + G + "[+]" + RESET
    lbl     = DIM + C + f"{label:<8}" + RESET
    val     = BRIGHT + value_color + value + RESET
    return f"  {bracket} {lbl} : {val}"

ASCII_LINES = [
    r"  ███████╗ █████╗ ███╗   ██╗ ██████╗ ",
    r"  ██╔════╝██╔══██╗████╗  ██║██╔════╝ ",
    r"  █████╗  ███████║██╔██╗ ██║██║  ███╗",
    r"  ██╔══╝  ██╔══██║██║╚██╗██║██║   ██║",
    r"  ██║     ██║  ██║██║ ╚████║╚██████╔╝",
    r"  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝",
]

REPO    = "https://github.com/DeveloperAromal/Fang"
TAGLINE = "Autonomous Cybersecurity Reconnaissance Framework"

def banner():
    ts      = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ipv6_str = ip_v6 if ip_v6 else "N/A"

    print("")
    for line in ASCII_LINES:
        print(center(BRIGHT + LR + line + RESET))
    print("")
    print(center(DIM + Y + TAGLINE + RESET))
    print("")
    print(hline())
    print(row("Version",  VERSION))
    print(row("Author",   "Aromal"))
    print(row("IPv4",     ip_v4))
    print(row("Repo",     REPO, LB))
    print(hline())
    print("")