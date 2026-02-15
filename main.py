from fang.utils.banner import banner
from fang.modules.web.basic.subdomain_enumerator import SubdomainEnumerator

banner()

SubdomainEnumerator("https://www.steyp.com").scan()