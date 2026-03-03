# from fang.utils.banner import banner
# from fang.modules.web.basic.subdomain_enumerator import SubdomainEnumerator
# from fang.modules.web.basic.tech_fingerprint import TechFingerprint
# from fang.modules.web.basic.robots_parser import RobotsParser
# from fang.modules.web.osint.social_media_data_extracter import SocialMediaDataOSINT
# from fang.modules.web.osint.domain_details import DomainDetails
# from fang.modules.network.port_scanner import PortScanner
# from fang.modules.web.basic.url_crawler import URLCrawler
from fang.modules.network.capture_banner import CaptureBanner
# SubdomainEnumerator("https://www.steyp.com").scan()

# TechFingerprint("https://www.steyp.com")

# fp = TechFingerprint("https://www.steyp.com")
# result = fp.fingerprint()
# print(result)

# rp = RobotsParser("https://www.nytimes.com").parse()

# print(rp)

# osint = SocialMediaDataOSINT("https://www.steyp.com/").osint()

# print(osint)


# d = DomainDetails("https://steyp.com")
# result = d.scan()
# print(result)

# po = PortScanner("https://vidyatcklmr.ac.in/")

# result = po.scan()

# print(result)



# ur = URLCrawler("https://vidyatcklmr.ac.in/")

# result = ur.crawl()

# print(result)


open_ports = [21, 53, 80, 110, 143, 443, 465, 587, 993, 2082, 2083, 3306]
for  port in open_ports:
    
    ur = CaptureBanner("vidyatcklmr.ac.in/", port)

    result = ur.grab()

    print(result)


# from fang.agent.graph import build_graph

# if __name__ == "__main__":

#     app = build_graph()

#     result = app.invoke({
#         "messages": [
#             ("user", "Perform reconnaissance on https://vidyatcklmr.ac.in")
#         ]
#     })

#     print(result)a

