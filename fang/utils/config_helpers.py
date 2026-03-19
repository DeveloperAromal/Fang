class ConfigHelper:

    SETTINGS_PATH = "config/settings.py"

    def __init__(self):
        pass



    def _read_setting(self, key: str) -> str:
        with open(self.SETTINGS_PATH, "r") as f:
            for line in f:
                stripped = line.strip()
                if stripped.startswith(key) and "=" in stripped:
                    _, _, value = stripped.partition("=")
                    return value.strip().strip('"').strip("'")
        return ""



    def _write_settings(self, updates: dict):
        with open(self.SETTINGS_PATH, "r") as f:
            lines = f.readlines()


        with open(self.SETTINGS_PATH, "w") as f:
            for line in lines:
                matched = False
                stripped = line.strip()
                for key, value in updates.items():
                    if stripped.startswith(key) and "=" in stripped:
                        if isinstance(value, bool):
                            f.write(f"{key} = {value}\n")
                        else:
                            f.write(f'{key} = "{value}"\n')
                        matched = True
                        break
                if not matched:
                    f.write(line)



    def _is_configured(self) -> bool:
        return self._read_setting("IS_NEW") == "True"



    def _add_key(self):
        key = input("Paste your Google API key (https://aistudio.google.com/api-keys): ").strip()
        self._write_settings({
            "LLM_API_KEY": key,
            "IS_NEW": True,
        })
        print("API key saved successfully.\n")

    def check(self):
        if not self._is_configured():  
            self._add_key()