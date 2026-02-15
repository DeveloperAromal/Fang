from fang.utils.banner import banner
from fang.modules.web.basic.subdomain_enumerator import SubdomainEnumerator
from fang.modules.web.basic.tech_fingerprint import TechFingerprint

banner()

SubdomainEnumerator("https://www.steyp.com").scan()

TechFingerprint("https://www.steyp.com")

fp = TechFingerprint("https://www.steyp.com")
result = fp.fingerprint()
print(result)