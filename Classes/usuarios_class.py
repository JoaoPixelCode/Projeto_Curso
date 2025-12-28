import re

class validador_usuario:
    @staticmethod
    def ValidadorEmail(email):
        if not email:
            return False, f"Por favor insira o email"
        if  '@' not in email:
            return False, f"Por favor insira um email valido"
        else:
            return True,None