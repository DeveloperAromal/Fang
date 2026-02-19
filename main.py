from fang.utils.banner import banner
from fang.modules.web.basic.subdomain_enumerator import SubdomainEnumerator
from fang.modules.web.basic.tech_fingerprint import TechFingerprint
from fang.modules.web.basic.robots_parser import RobotsParser
from fang.modules.web.osint.social_media_data_extracter import SocialMediaDataOSINT
from fang.modules.web.osint.domain_details import DomainDetails
banner()    

# SubdomainEnumerator("https://www.steyp.com").scan()

# TechFingerprint("https://www.steyp.com")

# fp = TechFingerprint("https://www.steyp.com")
# result = fp.fingerprint()
# print(result)

# rp = RobotsParser("https://www.nytimes.com").parse()

# print(rp)

# osint = SocialMediaDataOSINT("https://www.steyp.com/").osint()

# print(osint)


d = DomainDetails("https://steyp.com")
result = d.scan()
print(result)