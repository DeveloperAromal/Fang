

class WorldStates:
    
    def __init__(self, url):
        
        self.target = url
        self.host = set([url])
        self.open_ports = {}
        self.services = {}
        self.endpoints = set()
        self.forms = []
        self.subdomains = set()
        self.vulnerabilities = []
        self.actions_taken = []
        
    def log_action(self, action_name):
        self.actions_taken.append(action_name)