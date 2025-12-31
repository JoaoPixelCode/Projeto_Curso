import re
import string
from datetime import date
import random


class validador_usuario:
    @staticmethod
    #Talvez eu deva tirar esse Validador, pos o banca já impede que sejam inseridos email vazios e invalidos
    def ValidadorEmail(email):
        padrao = r'^[\w\.-]+@[\w\.-]+\.[\w]{2,}$'
        if not email:
            return False, f"Por favor insira o email"
        if '@' not in email:
            return False, f"Por favor insira um email valido"
        if not re.match(padrao, email):
            return False, f"Por favor insira um email valido"
        
        return True,None
    
    #Chamei de matricula por falta de um nome melhor,ele gera uma matricula basica usando o ano de cadastro, e dois numeros
    #aleatorios um de 3 digitos e outro de 2 digitos.
    def gerarMatricula(matricula):
        data_atual = date.today().year
        dia = date.today().day
        numero_aleatorio = random.randint(100,999)
        numero_aleatorio2 = random.randint(0,99)
        numero = (dia * 2 * numero_aleatorio) % 1000
        matricula='{}{}{}'.format(data_atual,numero,numero_aleatorio2)
        return f'{matricula}'

    #Validador de senha funciona e é necessario, ele verifica se a senha está vazia, contem menos de 8 caracteres, 
    #se possui letras maisculas,minusculas, caracteres especiais e se contem numeros, respectivamente
    #Foi feito assim para forçar senhas fortes de usuarios/funcionarios
    def ValidadorSenha(senha, senha2):
            if not senha:
                return False, f"Por favor insira a sua senha"
            if len(senha) < 8:
                return False, f"Por favor insira ao menos 8 caracteres em sua senha"  
            if not any(x.isupper() for x in senha):
                return False, f"Por favor insira uma letra maiscula"
            if not any(x.islower() for x in senha):
                return False, f"Por favor insira uma letra minuscula"
            if not any(x.isdigit() for x in senha):
                return False, f"Por favor insira ao menos um numero"
            if not any(x in string.punctuation for x in senha):
                return False, f"Por favor insira ao menos um caracter especial (@,#,$,etc)"
            if senha != senha2:
                return False, f"Senhas nao sao iguais"
           
            return True, None
    def ValidadorTelefone(telefone):
        if not telefone:
            return False, f"Por favor insira um telefone para contato"
        if len(telefone) < 8:
            return False,f"Insira um numero valido"
        if len(telefone) > 10:
            return False,f"Insiria um numero valido"
        
        return True, None