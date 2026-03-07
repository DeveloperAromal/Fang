from colorama import Fore, Back, Style, init  # type: ignore
from .ip_data import IPData
from datetime import datetime
import shutil
import textwrap
import re

init(autoreset=True)

ip_v4 = IPData.ipv4()
ip_v6 = IPData.ipv6()

R  = Fore.RED
C  = Fore.CYAN
Y  = Fore.YELLOW
G  = Fore.GREEN
W  = Fore.WHITE
M  = Fore.MAGENTA
LR = Fore.LIGHTRED_EX
LC = Fore.LIGHTCYAN_EX
LY = Fore.LIGHTYELLOW_EX
LW = Fore.LIGHTWHITE_EX
DIM    = Style.DIM
RESET  = Style.RESET_ALL
BRIGHT = Style.BRIGHT

_ANSI = re.compile(r'\x1b\[[0-9;]*m')

def _vlen(s):
    """Visible length of a string (strips ANSI codes)."""
    return len(_ANSI.sub('', s))

def _w():
    return shutil.get_terminal_size((100, 30)).columns

def hline(char="─"):
    return DIM + C + char * _w() + RESET

def dline(char="═"):
    return BRIGHT + C + char * _w() + RESET

def centered(text, color=""):
    pad = max(0, (_w() - _vlen(text)) // 2)
    return " " * pad + color + text + RESET

def fill_row(left, right):
    """Place left on the left edge, right on the right edge."""
    w    = _w()
    llen = _vlen(left)
    rlen = _vlen(right)
    gap  = max(1, w - llen - rlen)
    return left + " " * gap + right

def two_col(lbl1, val1, lbl2, val2):
    w     = _w()
    left  = f"  {BRIGHT + C}{lbl1:<16}{RESET}{DIM + LW}{val1}{RESET}"
    right = f"{BRIGHT + C}{lbl2:<16}{RESET}{DIM + LW}{val2}{RESET}  "
    gap   = max(2, w - _vlen(left) - _vlen(right))
    return left + " " * gap + right

def center_art(lines, color=""):
    max_len = max(len(l) for l in lines)
    w   = _w()
    pad = max(0, (w - max_len) // 2)
    return [" " * pad + color + l + RESET for l in lines]



ASCII_LINES = [
    r"  ███████╗ █████╗ ███╗   ██╗ ██████╗  ",
    r"  ██╔════╝██╔══██╗████╗  ██║██╔════╝  ",
    r"  █████╗  ███████║██╔██╗ ██║██║  ███╗ ",
    r"  ██╔══╝  ██╔══██║██║╚██╗██║██║   ██║ ",
    r"  ██║     ██║  ██║██║ ╚████║╚██████╔╝ ",
    r"  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ",
]



def banner():
    w   = _w()
    now = datetime.now()
    ts  = now.strftime("%Y-%m-%d  %H:%M:%S")
    ipv6_str = ip_v6 if ip_v6 else "N/A"

    print(BRIGHT + C + "╔" + "═" * (w - 2) + "╗" + RESET)
    print(BRIGHT + C + "║" + " " * (w - 2) + "║" + RESET)

    # ascii art
    for l in center_art(ASCII_LINES, BRIGHT + LR):
        vis   = _ANSI.sub('', l)
        total = len(vis)
        right = max(0, w - 2 - total)
        print(BRIGHT + C + "║" + RESET + l + " " * right + BRIGHT + C + "║" + RESET)

    print(BRIGHT + C + "║" + " " * (w - 2) + "║" + RESET)

    subtitle = "[ A U T O M A T E D   C Y B E R   S E C U R I T Y   F R A M E W O R K ]"
    sub_pad  = max(0, (w - 2 - len(subtitle)) // 2)
    sub_line = " " * sub_pad + BRIGHT + W + subtitle + RESET + " " * (w - 2 - sub_pad - len(subtitle))
    print(BRIGHT + C + "║" + RESET + sub_line + BRIGHT + C + "║" + RESET)

    tagline = ">>  Recon  |  Enumeration  |  Exploitation  |  Post-Exploitation  |  Reporting  <<"
    tag_pad = max(0, (w - 2 - len(tagline)) // 2)
    tag_line = " " * tag_pad + DIM + Y + tagline + RESET + " " * (w - 2 - tag_pad - len(tagline))
    print(BRIGHT + C + "║" + RESET + tag_line + BRIGHT + C + "║" + RESET)

    print(BRIGHT + C + "║" + " " * (w - 2) + "║" + RESET)
    print(BRIGHT + C + "╠" + "═" * (w - 2) + "╣" + RESET)

    def inner(text):
        vis_len = _vlen(text)
        pad = max(0, w - 2 - vis_len - 2)
        print(BRIGHT + C + "║ " + RESET + text + " " * pad + BRIGHT + C + "║" + RESET)

    inner("")
    inner(two_col("Version",  "2.0.0",           "Build Date",  ts))
    inner(two_col("Author",   "YourName",         "Platform",    "Linux / Windows / macOS"))
    inner(two_col("Module",   "Net Recon & VA",   "Status",      f"{BRIGHT + G}● ACTIVE{RESET}"))
    inner("")

    print(BRIGHT + C + "╠" + "─" * (w - 2) + "╣" + RESET)

    inner("")

    ip4_row = (f"  {BRIGHT + G}◈  IPv4 ORIGIN{RESET}   "
               f"{BRIGHT + LW}{ip_v4:<40}{RESET}   "
               f"{DIM + Y}All outbound requests originate from this IP{RESET}")
    ip6_row = (f"  {BRIGHT + G}◈  IPv6 ORIGIN{RESET}   "
               f"{BRIGHT + LW}{ipv6_str:<40}{RESET}   "
               f"{DIM + Y}Operator bears full legal responsibility for use{RESET}")
    inner(ip4_row)
    inner(ip6_row)
    inner("")

    notice = (f"  {DIM + Y}By using FANG you confirm that all activities are performed on systems you own or "
              f"have explicit written authorisation to test. The developer(s) accept NO liability "
              f"whatsoever for misuse, illegal access, or any damage caused by this tool.{RESET}")
    for chunk in textwrap.wrap(_ANSI.sub('', notice), width=w - 6):
        inner(f"  {DIM + Y}{chunk}{RESET}")

    inner("")
    print(BRIGHT + C + "╠" + "─" * (w - 2) + "╣" + RESET)

    inner("")

    disc_title = f"  {BRIGHT + LR}⚠   LEGAL DISCLAIMER  &  TERMS OF USE{RESET}"
    inner(disc_title)
    inner("")

    items = [
        ("AUTHORIZED USE ONLY",  "For educational & authorized penetration testing ONLY."),
        ("NO LIABILITY",         "Developers assume ZERO responsibility for misuse or damages."),
        ("ILLEGAL USE BANNED",   "Unauthorized system access violates computer crime laws worldwide."),
        ("USER ACCOUNTABILITY",  "You are solely responsible for complying with applicable laws."),
        ("IP ON RECORD",         f"Your origin IP [ {ip_v4} ] is displayed above — act responsibly."),
    ]

    for title, desc in items:
        label = f"  {BRIGHT + R}[ {title} ]{RESET}"
        val   = f"{DIM + W}{desc}{RESET}"
        gap   = max(2, w - 4 - _vlen(label) - _vlen(val))
        inner(label + " " * gap + val)

    inner("")
    print(BRIGHT + C + "╠" + "═" * (w - 2) + "╣" + RESET)

    print(BRIGHT + C + "║" + " " * (w - 2) + "║" + RESET)

    status  = f"  {BRIGHT + G}●  READY{RESET}"
    repo    = f"{DIM + C}github.com/DeveloperAromal/fang{RESET}"
    time_r  = f"{DIM + W}{ts}{RESET}  "
    s_len   = _vlen(status)
    r_len   = _vlen(repo)
    t_len   = _vlen(time_r)
    gap1    = max(2, (w - 2 - s_len - r_len - t_len) // 2)
    gap2    = w - 2 - s_len - r_len - t_len - gap1
    bar     = status + " " * gap1 + repo + " " * max(1, gap2) + time_r
    # pad bar to fill interior
    bar_vis = _vlen(bar)
    bar_pad = max(0, w - 2 - bar_vis)
    print(BRIGHT + C + "║" + RESET + bar + " " * bar_pad + BRIGHT + C + "║" + RESET)

    print(BRIGHT + C + "║" + " " * (w - 2) + "║" + RESET)
    print(BRIGHT + C + "╚" + "═" * (w - 2) + "╝" + RESET)
    print()