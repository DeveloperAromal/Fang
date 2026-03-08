from colorama import Fore, Style, init

class PromptUser:
    
    def __init__(self, placeholder: str):
        self.placeholder = placeholder
    
    def collect(self):
        
        usr_input = input(Fore.GREEN + f"{self.placeholder}" + Style.RESET_ALL)
        
        return usr_input