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

_ANSI = re.compile(r'\x1b\[[0-9;]*m')
def _w():         return shutil.get_terminal_size((100, 30)).columns
def _vlen(s):     return len(_ANSI.sub('', s))
def hline(c="─"): return DIM + C + c * _w() + RESET
def fill(left, right):
    gap = max(1, _w() - _vlen(left) - _vlen(right))
    return left + " " * gap + right


ASCII_LINES = [
    r" ███████╗ █████╗ ███╗   ██╗ ██████╗",
    r" ██╔════╝██╔══██╗████╗  ██║██╔════╝",
    r" █████╗  ███████║██╔██╗ ██║██║  ███╗",
    r" ██╔══╝  ██╔══██║██║╚██╗██║██║   ██║",
    r" ██║     ██║  ██║██║ ╚████║╚██████╔╝",
    r" ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝",
]


def banner():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ipv6_str = ip_v6 if ip_v6 else "N/A"

    print("")
    for line in ASCII_LINES:
        print(BRIGHT + LR + line + RESET)
    print("")
    print(hline())
    print(fill(
        f"  {DIM+C}Version {RESET}{BRIGHT+LW}{VERSION}{RESET}  {DIM+C}Author {RESET}{BRIGHT+LW}Aromal{RESET}  {DIM+C}Status {RESET}{BRIGHT+G}● ACTIVE{RESET}",
        f"{DIM+C}IPv4 {RESET}{BRIGHT+LW}{ip_v4}{RESET}  {DIM+C}IPv6 {RESET}{BRIGHT+LW}{ipv6_str}  {RESET}"
    ))
    print(hline())
    print(f"  {BRIGHT+LR} {DIM+Y}Authorized use only. All requests exit from {BRIGHT+LW}{ip_v4}{DIM+Y}. Devs hold NO liability.{RESET}")
    print(hline())
    print("")