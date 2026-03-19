import re

@staticmethod
def config():
    SETTINGS_PATH = "config/settings.py"

    with open(SETTINGS_PATH, "r") as f:
        content = f.read()

    content = re.sub(r'^LLM_API_KEY\s*=.*$', 'LLM_API_KEY = ""', content, flags=re.MULTILINE)
    content = re.sub(r'^IS_NEW\s*=.*$', 'IS_NEW = False', content, flags=re.MULTILINE)

    with open(SETTINGS_PATH, "w") as f:
        f.write(content)
        
        
config()