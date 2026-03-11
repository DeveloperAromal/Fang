from config.settings import IS_NEW


class ConfigHelper:

    def __init__(self):
        pass

    def _check_is_new(self):
        return IS_NEW

    def _add_key(self):

        key = input("Paste your Google API key (https://aistudio.google.com/api-keys): ")

        with open("config/settings.py", "r") as f:
            config = f.readlines()

        with open("config/settings.py", "w") as f:
            for line in config:
                if line.strip().startswith("LLM_API_KEY"):
                    f.write(f'LLM_API_KEY = "{key}"\n')
                elif line.strip().startswith("IS_NEW"):
                    f.write("IS_NEW = True\n")
                else:
                    f.write(line)
                                
                    
    def check(self):
        
        if self._check_is_new():
            return
        
        else: 
            self._add_key()
            
