import sys
import re


# Fichero fuente.
argc = len(sys.argv[1:])
if (argc == 0 or argc > 2):
    # Número de argumentos incorrecto.
    print("Uso: sintactico.py <fichero_fuente>")
    exit(0)

# Abrir ficheros de entrada y de salida.
lista_tokens = open(sys.argv[1], 'r')
ts_out = open("tabla" + ".ts", 'w')
variables = open("variables" + ".var", 'r')
pila_var =  []
for linea in variables:
    pila_var.append(linea[:-1])

indice_var = len(pila_var)
list_var= {}
for x in range(indice_var, 0, -1):
    list_var[x] = pila_var.pop()

contador = 1
# Generar salida por defecto.
parser_out = open("parser_out" + ".parser", 'w')
#Conjunto de No terminales
cNoTerminal={"A", "B", "Bp", "C", "D", "E", "Ep", "F", "G", "Gp", "H", "Hp", "I", "Ip", "Ipp", "J", "Jp", "K", "L", "M", "N", "O", "Q", "R", "Y", "Yp", "Z"}
cTerminal={"&&", "(", ")", "+", "+=", ",", ":", ";", "=", ">=", "alert", "boolean", "break","cadena", "case","cteEntera" , 
           "default", "else", "function", "id", "if", "input","let", "number", "return", "string", "switch","{","}","$"}

pila = ['$', 'A']
pila_atr = ['-', '-']
sig_token = ""
tokens_actual =  []
indice = 0
pila_aux = []
pila_aux_atr = []

# Diccionarios para la tabla de símbolos.
# La clave es el lexema y el valor es el
# correspondiente de cada diccionario.
ts_types = {} # int, string, boolean o func.
ts_displacements = {} # Desplazamiento en memoria de cada símbolo.
ts_displacement = 0 # Desplazamiento para el próximo símbolo a añadir.
ts_func_displacement = 0 # Desplazamiento para el próximo símbolo a añadir.
ts_func_return_types = {} # Tipo de retorno de la función.
ts_func_parameters = {} # Los valores son diccionarios con los símbolos de la función.
ts_func_symbols = {} # Los valores son diccionarios de listas con los símbolos de la función. 0 = tipo, 1 = deslp.
ts_func_tags = {} # Etiqueta de la función.
ts_current = 0


# Funciones auxiliares.
def dic_fun(terminal, sig_token):
    if(terminal == "A"):
        p_A(sig_token)
    if(terminal == "B"):
        p_B(sig_token)
    if(terminal == "C"):
        p_C(sig_token)
    if(terminal == "D"):
        p_D(sig_token)
    if(terminal == "E"):
        p_E(sig_token)
    if(terminal == "F"):
        p_F(sig_token)
    if(terminal == "G"):
        p_G(sig_token)
    if(terminal == "H"):
        p_H(sig_token)
    if(terminal == "I"):
        p_I(sig_token)
    if(terminal == "J"):
        p_J(sig_token)
    if(terminal == "K"):
        p_K(sig_token)
    if(terminal == "L"):
        p_L(sig_token)
    if(terminal == "M"):
        p_M(sig_token)
    if(terminal == "N"):
        p_N(sig_token)
    if(terminal == "O"):
        p_O(sig_token)
    if(terminal == "Q"):
        p_Q(sig_token)
    if(terminal == "R"):
        p_R(sig_token)
    if(terminal == "Bp"):
        p_Bp(sig_token)
    if(terminal == "Ep"):
        p_Ep(sig_token)
    if(terminal == "Gp"):
        p_Gp(sig_token)
    if(terminal == "Hp"):
        p_Hp(sig_token)
    if(terminal == "Ip"):
        p_Ip(sig_token)
    if(terminal == "Jp"):
        p_Jp(sig_token)
    if(terminal == "Ipp"):
        p_Ipp(sig_token)
    if(terminal == "Y"):
        p_Y(sig_token)
    if(terminal == "Yp"):
        p_Yp(sig_token)
    if(terminal == "Z"):
        p_Z(sig_token)
despl = {
    "number" : 1,
    "string" : 64,
    "boolean" : 1,
}        
def dic_sem(num):
    global sig_token
    global contador
    global list_var
    if(num == 1.1 or num == 2.1 or num == 3.1 or num == 4.1):
        pila.pop()
        pila_atr.pop()
        pila_aux.pop()
        pila_aux_atr.pop()
    if(num == 6.1):
        pila.pop()
        pila_atr.pop()
        atributo = pila_aux_atr[-1]
        pila_aux_atr[pila_aux.index("B")] = atributo
        if(pila[-1] == sig_token):
            sig_token=act_pila()
    if(num == 6.2):
        pila.pop()
        pila_atr.pop()
        add_var_symbol(list_var[contador], pila_aux_atr[pila_aux.index("B")])
        contador+=1
        for x in range (0, 4):
            pila_aux.pop()
            pila_aux_atr.pop()
        if(pila[-1] == sig_token):
            sig_token=act_pila()
    if(num == 7.1):
        pila.pop()
        pila_atr.pop()
        if(not symbol_exists(list_var[contador])):
            print("error semántico")
        print(symbol_type(list_var[contador]))
        print("hola javiii")
        pila_aux_atr[-1] = symbol_type(list_var[contador])
        print(sig_token)
        print(pila)
        print(pila_atr)
        if(pila[-1] == sig_token):
            sig_token=act_pila()
    if(num == 7.2):
        pila.pop()
        pila_atr.pop()
        for x in range (0, 2):
            pila_aux.pop()
            pila_aux_atr.pop()
        if(pila[-1] == sig_token):
            sig_token=act_pila()
    if(num == 11.1):

        pila.pop()
        pila_atr.pop()
        print(pila)
        print(pila_atr)
        print(pila_aux)
        print(pila_aux_atr)
        print("adfsdfsdfsdf")
        if(pila[-1] == sig_token):
            sig_token=act_pila()
    if(num == 11.2):
        pila.pop()
        pila_atr.pop()
        for x in range (0, 4):
            pila_aux.pop()
            pila_aux_atr.pop()
        if(pila[-1] == sig_token):
            sig_token=act_pila()
    if(num == 17.1 or num == 18.1 or num ==19.1):
        pila.pop()
        pila_atr.pop()
        pila_aux_atr.pop()
        tope = pila_aux.pop()
        pila_aux_atr.pop()
        pila_aux_atr.append(tope)
        if(pila[-1] == sig_token):
            sig_token=act_pila()
    else:
        print("No hace nada")

def symbol_exists (s_lexem):
    global ts_types

    try:
        symbol_type = ts_types[s_lexem]
    except KeyError:
        if ts_current != 0:
            try:
                symbol_type = ts_current[s_lexem]
            except KeyError:
                try:
                    symbol_type = ts_current["params"][s_lexem]
                except KeyError:
                    return False
                return True
            return True
        else:
            return False
    return True

def symbol_type (s_lexem):
    global ts_current
    
    if not symbol_exists(s_lexem):
        return ""
    if ts_current != 0:
        try:
            s_type = ts_current["params"][s_lexem]
        except KeyError:
            try:
                s_type = ts_current[s_lexem][0]
            except KeyError:
                s_type = ts_types[s_lexem]
    else:
        s_type = ts_types[s_lexem]
    if s_type == "func":
        s_type = ts_func_return_types[s_lexem]
    return s_type

def check_calling_parameters (function_lexem, parameters):
    function_parameters = ts_func_parameters[function_lexem]
    if len(function_parameters) != len(parameters):
        # Ni siquiera coincide el número de parámteros.
        return False
    to_return = True
    i = 0
    for parameter in function_parameters:
        to_return &= function_parameters[parameter] == parameters[i]
        i += 1
    return to_return
    
def add_var_symbol (s_lexem, s_type):
    global ts_types
    global ts_displacements
    global ts_displacement
    global despl
    global ts_current
    global ts_func_displacement
    
    if symbol_exists(s_lexem):
        # Return an error if the symbol already exists in the ts.
        return False
    if ts_current != 0:
        ts_current[s_lexem] = [s_type, ts_func_displacement]
        ts_func_displacement = ts_func_displacement + despl[s_type]

    else:
        ts_types[s_lexem] = s_type
        ts_displacements[s_lexem] = ts_displacement
        ts_displacement = ts_displacement + despl[s_type]
    return True

def add_func_params (f_params):
    global ts_current

    ts_current = {}

    for param in f_params:
        add_var_symbol(param, f_params[param])

def add_func_symbol (s_lexem, s_return_type, s_params):
    global ts_types
    global ts_func_return_types
    global ts_func_tags
    global ts_func_parameters
    global ts_current
    
    if symbol_exists(s_lexem):
        # Return an error if the symbol already exists in the ts.
        return False
    ts_types[s_lexem] = "func"
    ts_func_return_types[s_lexem] = s_return_type
    ts_func_tags[s_lexem] = "Et" + s_lexem
    ts_func_parameters[s_lexem] = s_params
    ts_func_symbols[s_lexem] = ts_current
    ts_current = 0
    ts_func_displacement = 0
    return True

def es_flotante(variable):
    try:
        float(variable)
        return True
    except:
        return False       
def act_pila():
    pila_aux.append(pila[-1])
    pila_aux_atr.append("-")
    pila.pop()
    pila_atr.pop()  
    global indice

    global sig_token 
        
    indice = indice +1  
    if(indice < len(tokens_actual)):
        sig_token = tokens_actual[indice]

        while(sig_token == pila[-1]):
            pila_aux.append(pila[-1])
            pila_aux_atr.append("-")
            pila.pop()
            pila_atr.pop()
            indice = indice +1
            sig_token = tokens_actual[indice]
        while(es_flotante(pila[-1])):
            dic_sem(pila[-1])
        return  sig_token

def bor_pila(sig_token):

    if(not pila):
        print("pila vacía")
    else:

        if(pila[-1] in cNoTerminal):
            dic_fun(pila[-1], sig_token)

        else:
            pila.pop()
            pila_atr.pop()
            if(pila[-1] == sig_token):
                sig_token=act_pila()
            if pila[-1] in cTerminal:
                print("Error sintático")
        
            if pila[-1] in cNoTerminal:
                temp = pila[-1]
                dic_fun(temp, sig_token)

def equipara (line):
    conv = ""
    if "<number,>" in line:
        conv = "number"
    if "<boolean,>" in line:
        conv = "boolean"
    if "<string,>" in line:
        conv = "string"
    if "<function,>" in line:
        conv = "function"
    if "<input,>" in line:
        conv = "input"
    if "<return,>" in line:
        conv = "return"
    if "<alert,>" in line:
        conv = "alert"
    if "<if,>" in line:
        conv = "if"
    if "<else,>" in line:
        conv = "else"
    if "<switch,>" in line:
        conv = "switch"
    if "<case,>" in line:
        conv = "case"
    if "<default,>" in line:
        conv = "default"
    if "<break,>" in line:
        conv = "break"
    if "<let,>" in line:
        conv = "let"
    patron = re.compile('<cteEntera,.*>')
    st = str(line)
    busqueda = re.findall(patron, st)
    for i in busqueda:
        conv = "cteEntera"

    
    patron = re.compile('<cadena,.*>')
    st = str(line)
    busqueda = re.findall(patron, st)
    for i in busqueda:
        conv = "cadena"


    patron = re.compile('<id,.*>')
    st = str(line)
    busqueda = re.findall(patron, st)
    for i in busqueda:
        conv = "id"

    if "<asignacion,equal>" in line:
        conv = "="
    if "<coma,>" in line:
        conv = ","
    if "<puntoComa,>" in line:
        conv = ";"
    if "<dosPuntos,>" in line:
        conv = ":"
    if "<parOp,>" in line:
        conv = "("
    if "<parCl,>" in line:
        conv = ")"
    if "<llavOp,>" in line:
        conv = "{"
    if "<llavCl,>" in line:
        conv = "}"
    if "<opAritmetico,sum>" in line:
        conv = "+"
    if "<opRelacion,bt>" in line:
        conv = ">="
    if "<opLogico,and>" in line:
        conv = "&&"
    if "<asignacion,add>" in line:
        conv = "+="
    return conv

def p_A(sig_token):
    if(sig_token == 'function'):
        pila.pop()
        pila_atr.pop()
        parser_out.write('3 ')
        pila.append(3.1)
        pila_atr.append("-")
        pila.append("A")
        pila_atr.append("-")
        pila.append("F")
        pila_atr.append("-")
        bor_pila(sig_token)
    elif(sig_token == 'if'):
        pila.pop()
        pila_atr.pop()
        parser_out.write('3 ')
        pila.append(2.1)
        pila_atr.append("-")
        pila.append("A")
        pila_atr.append("-")
        pila.append("I")
        pila_atr.append("-")
        bor_pila(sig_token)
    elif(sig_token == 'let' or sig_token == 'alert' or sig_token == 'id' or sig_token == 'input' or sig_token == 'return'):
        parser_out.write('1 ')
        pila.pop()
        pila_atr.pop()
        pila.append(1.1)
        pila_atr.append("-")
        pila.append("A")
        pila_atr.append("-")
        pila.append("B")
        pila_atr.append("-")

        pila_aux.append("A")
        pila_aux_atr.append("-")
        bor_pila(sig_token)
    elif(sig_token == 'switch'):
        pila.pop()
        pila_atr.pop()
        parser_out.write('3 ')
        pila.append(3.1)
        pila_atr.append("-")
        pila.append("A")
        pila_atr.append("-")
        pila.append("Z")
        pila_atr.append("-")
        bor_pila(sig_token)
    elif(sig_token == "$"):
        parser_out.write('5')
        pila.pop()
        pila_atr.pop()
        dic_sem(pila[-1])
        print("FIN")
    
def p_B(sig_token):
    if(sig_token == 'alert'):
        parser_out.write('9 ')
        pila.pop()
        pila_atr.pop()
        pila_aux.append("B")
        pila_aux_atr.append("-")
        pila.append(9.2)
        pila_atr.append("-")
        pila.append(";")
        pila_atr.append("-")
        pila.append(")")
        pila_atr.append("-")
        pila.append("E")
        pila_atr.append("-")
        pila.append(9.1)
        pila_atr.append("-")
        pila.append("(")
        pila_atr.append("-")
        pila.append("alert")
        pila_atr.append("-")
        if(pila[-1] == sig_token):
            sig_token=act_pila()
        bor_pila(sig_token)
    elif(sig_token == 'id'):
        parser_out.write('7 ')
        pila.pop()
        pila_atr.pop()
        pila_aux.append("B")
        pila_aux_atr.append("-")
        pila.append(7.2)
        pila_atr.append("-")
        pila.append("Bp")
        pila_atr.append("-")
        pila.append(7.1)
        pila_atr.append("-")
        pila.append("id")
        pila_atr.append("-")
        print(pila)
        print(pila_atr)
        if(pila[-1] == sig_token):
            sig_token=act_pila()
        bor_pila(sig_token)
    elif(sig_token == 'input'):
        parser_out.write('10 ')
        pila.pop()
        pila_atr.pop()
        pila_aux.append("B")
        pila_aux_atr.append("-")
        pila.append(10.2)
        pila_atr.append("-")
        pila.append(";")
        pila_atr.append("-")
        pila.append(")")
        pila_atr.append("-")
        pila.append("id")
        pila_atr.append("-")
        pila.append(10.1)
        pila_atr.append("-")
        pila.append("(")
        pila_atr.append("-")
        pila.append("input")
        pila_atr.append("-")
        if(pila[-1] == sig_token):
            sig_token=act_pila()
        bor_pila(sig_token)
    elif(sig_token == 'let'):
        parser_out.write('6 ')
        pila.pop()
        pila_atr.pop()
        pila_aux.append("B")
        pila_aux_atr.append("-")
        pila.append(6.2)
        pila.append(";")
        pila_atr.append("-")
        pila_atr.append("-")
        pila.append("id")
        pila_atr.append("-")
        pila.append(6.1)
        pila_atr.append("-")
        pila.append("D")
        pila_atr.append("-")

        pila.append("let")
        pila_atr.append("-")
        if(pila[-1] == sig_token):
            sig_token=act_pila()
        p_D(sig_token)
    elif(sig_token == 'return'):
        parser_out.write('8 ')
        pila.pop()
        pila_atr.pop()
        pila_aux.append("B")
        pila_aux_atr.append("-")
        pila.append(8.2)
        pila_atr.append("-")
        pila.append(";")
        pila_atr.append("-")
        pila.append("Q")
        pila_atr.append("-")
        pila.append(8.1)
        pila_atr.append("-")
        pila.append("return")
        pila_atr.append("-")
        if(pila[-1] == sig_token):
            sig_token=act_pila()
        p_Q(sig_token)
             
def p_Bp(sig_token):
    if(sig_token == '('):
        parser_out.write('13 ')
        pila.pop()
        pila.append(";")
        pila.append(")")
        pila.append("K")
        pila.append("(")
        if(pila[-1] == sig_token):
            sig_token=act_pila()
        bor_pila(sig_token)
    elif(sig_token == '+='):
        parser_out.write('12 ')
        pila.pop()
        pila.append(";")
        pila.append("E")
        pila.append("+=")
        if(pila[-1] == sig_token):
            sig_token=act_pila()
        bor_pila(sig_token)
    elif(sig_token == '='):
        parser_out.write('11 ')
        pila.pop()
        pila_atr.pop()
        pila.append(11.2)
        pila_atr.append("-")      
        pila.append(";")
        pila_atr.append("-")
        pila.append("E")
        pila_atr.append("-")
        pila.append(11.1)
        pila_atr.append("-") 
        pila.append("=")
        pila_atr.append("-")
        if(pila[-1] == sig_token):
            sig_token=act_pila()
        bor_pila(sig_token)

def p_C (sig_token):
    if(sig_token == 'alert' or sig_token == 'id' or sig_token == 'input' or sig_token == 'let' or sig_token == 'return'):
        parser_out.write('14 ')
        pila.append("B")
        p_B(sig_token)  
    elif(sig_token == 'break' or sig_token == 'case' or sig_token == 'default' or sig_token == '}'):
        pila.pop()
        parser_out.write('16 ')
        if(pila[-1] == sig_token):
            sig_token=act_pila()
        bor_pila(sig_token)
    elif(sig_token == 'if'):
        parser_out.write('15 ')
        pila.append("I")
        p_I(sig_token)
        
def p_D (sig_token):
    if(sig_token == 'boolean'):
        parser_out.write('17 ')
        pila_aux.append(pila[-1])
        pila_aux_atr.append("-")
        pila.pop()
        pila_atr.pop()
        pila.append(17.1)
        pila_atr.append("-") 
        pila.append("boolean")
        pila_atr.append("-")
        if(pila[-1] == sig_token):
            sig_token=act_pila()
            bor_pila(sig_token)
    elif(sig_token == 'string'):
        parser_out.write('18 ')
        pila_aux.append(pila[-1])
        pila_aux_atr.append("-")
        pila.pop()
        pila_atr.pop()
        pila.append(18.1)
        pila_atr.append("-") 
        pila.append("string")
        pila_atr.append("-")
        if(pila[-1] == sig_token):
            sig_token=act_pila()
            bor_pila(sig_token)
    elif(sig_token == 'number'):
        parser_out.write('19 ')
        pila_aux.append(pila[-1])
        pila_aux_atr.append("-")
        pila.pop()
        pila_atr.pop()
        pila.append(19.1)       
        pila_atr.append("-")
        pila.append("number") 
        pila_atr.append("-")
       
        if(pila[-1] == sig_token):
            sig_token=act_pila()  
            bor_pila(sig_token)
               
def p_E (sig_token):
    if(sig_token == '(' or sig_token == 'cadena' or sig_token == 'cteEntera' or sig_token == 'id'):
        parser_out.write('20 ')
        pila.pop()
        pila_atr.pop()
        pila.append(20.2)       
        pila_atr.append("-")
        pila.append("Ep")
        pila_atr.append("-")
        pila.append(20.1)       
        pila_atr.append("-")
        pila.append("G")
        pila_atr.append("-")
        p_G(sig_token)

def p_Ep (sig_token):
    if(sig_token == '&&'):
        parser_out.write('21 ')
        pila.append("G")
        pila.append("&&")
        if(pila[-1] == sig_token):
            sig_token=act_pila()
        bor_pila(sig_token)
    elif(sig_token == ')' or sig_token == ',' or sig_token == ':' or sig_token == ';'):
        parser_out.write('22 ')
        pila.pop()
        if(pila[-1] == sig_token):
            sig_token=act_pila()
        bor_pila(sig_token)
    elif(sig_token == "$"):
        pila.pop()
        bor_pila(sig_token)
def p_F (sig_token):
    if(sig_token == 'function'):
        parser_out.write('23 ')
        pila.pop()
        pila.append("}")
        pila.append("C")
        pila.append("{")
        pila.append(")")
        pila.append("N")
        pila.append("(")
        pila.append("id")
        pila.append("M")
        pila.append("function")
        if(pila[-1] == sig_token):
            sig_token=act_pila()
        p_M(sig_token)
        
def p_G (sig_token):
    if(sig_token == '(' or sig_token == 'cadena' or sig_token == 'cteEntera' or sig_token == 'id'):
        parser_out.write('24 ')
        pila.pop()
        pila_atr.pop()
        pila.append(24.2)
        pila.append("-")
        pila.append("Gp")
        pila.append("-")
        pila.append(24.1)
        pila.append("-")
        pila.append("H")
        pila.append("-")
        p_H(sig_token)
        
def p_Gp (sig_token):
    if(sig_token == '&&' or sig_token == ')' or sig_token == ',' or sig_token == ':' or sig_token == ';'):
        parser_out.write('26 ')
        pila.pop()
        bor_pila(sig_token)
    elif(sig_token == '>='):
        parser_out.write('25 ')
        pila.append("H")
        pila.append(">=")
        if(pila[-1] == sig_token):
            sig_token=act_pila()
        p_H(sig_token)
    elif(sig_token == "$"):
        pila.pop()
        bor_pila(sig_token)
def p_H (sig_token):
    if(sig_token == '(' or sig_token == 'cadena' or sig_token == 'cteEntera' or sig_token == 'id'):
        parser_out.write('27 ')
        pila.pop()
        pila_atr.pop()
        pila.append(27.2)
        pila.append("-")
        pila.append("Hp")
        pila.append("-")
        pila.append(27.1)
        pila.append("-")
        pila.append("J")
        pila.append("-")
        p_J(sig_token)
def p_Hp (sig_token):
    if(sig_token == '&&' or sig_token == ')' or sig_token == ',' or sig_token == ':' or sig_token == ';' or sig_token == '>='):
        parser_out.write('29 ')
        pila.pop()
        bor_pila(sig_token)
    elif(sig_token == '+'):
        parser_out.write('28 ')
        pila.append("J")
        pila.append("+")
        if(pila[-1] == sig_token):
            sig_token=act_pila()
        p_J(sig_token)
    elif(sig_token == "$"):
        pila.pop()
        bor_pila(sig_token)
def p_I (sig_token):
    if(sig_token == 'if'):
        parser_out.write('30 ')
        pila.pop()
        pila.append("Ip")
        pila.append(")")
        pila.append("E")
        pila.append("(")
        pila.append("if")
        if(pila[-1] == sig_token):
            sig_token=act_pila()
        p_E(sig_token)

def p_Ip (sig_token):
    if(sig_token == 'alert' or sig_token == 'id' or sig_token == 'input' or sig_token == 'let' or sig_token == 'return'):
        parser_out.write('31 ')
        pila.pop()
        pila.append("B")
        p_B(sig_token)
    elif(sig_token == "{"):
        parser_out.write('32 ')
        pila.pop()
        pila.append("Ipp")
        pila.append("}")
        pila.append("C")
        pila.append("{")
        if(pila[-1] == sig_token):
            sig_token=act_pila()
        p_C(sig_token)
        
def p_Ipp(sig_token):
    if(sig_token == 'else'):
        parser_out.write('33 ')
        pila.pop()
        pila.append("}")
        pila.append("C")
        pila.append("{")
        pila.append("else")
        if(pila[-1] == sig_token):
            sig_token=act_pila()
        p_C(sig_token)
    elif(sig_token == 'alert' or sig_token == 'break' or sig_token == 'case' or sig_token == 'default' or sig_token == 'function' or sig_token == 'id' or sig_token == 'if' or sig_token == 'input' or sig_token == 'let' or sig_token == 'return' or sig_token == 'switch' or sig_token == '}' or sig_token == '$'):
        parser_out.write('34 ')
        pila.pop()
        bor_pila(sig_token)

def p_J(sig_token):
    if(sig_token =='('):
        parser_out.write('35 ')
        pila.pop()
        pila.append(")")
        pila.append("E")
        pila.append("(")
        if (pila[-1]==sig_token):
            sig_token = act_pila()
        p_E(sig_token)
    elif (sig_token=='cadena'):
        parser_out.write('37 ')
        pila.pop()
        pila.append("cadena")
        if (pila[-1]==sig_token):
            sig_token = act_pila()
        bor_pila(sig_token)
    elif (sig_token=='cteEntera'):
        parser_out.write('36 ')
        pila.pop()
        pila_atr.pop()
        pila.append(36.2)
        pila.append("-")
        pila.append("cteEntera")
        if (pila[-1]==sig_token):
            sig_token = act_pila()
        bor_pila(sig_token)
    elif (sig_token== 'id'):
        parser_out.write('38 ')
        pila.pop()
        pila.append("Jp")
        pila.append("id")
        if (pila[-1]==sig_token):
            sig_token = act_pila()
        p_Jp(sig_token)

def p_Jp(sig_token):
    if (sig_token=='&&' or sig_token==')' or sig_token==';' or sig_token==':' or sig_token=='+' or sig_token==',' or sig_token=='>='):
        parser_out.write('40 ')
        pila.pop()
        bor_pila(sig_token)
    elif(sig_token=='('):
        parser_out.write('39 ')
        pila.pop()
        pila.append(")")
        pila.append("K")
        pila.append("(")
        if (pila[-1]==sig_token):
            sig_token = act_pila()
        p_K(sig_token)
    elif(sig_token == "$"):
        pila.pop()
        bor_pila(sig_token)
def p_K(sig_token):
    if (sig_token=='('):
        parser_out.write('41 ')
        pila.pop()
        pila.append("L")
        pila.append("E")
        p_E(sig_token)
        
    elif (sig_token=='cadena'):
        parser_out.write('41 ')
        pila.pop()
        pila.append("L")
        pila.append("E")
        p_E(sig_token)
    elif (sig_token=='cteEntera'):
        parser_out.write('41 ')
        pila.pop()
        pila.append("L")
        pila.append("E")
        p_E(sig_token)
    elif (sig_token=='id'):
        parser_out.write('41 ')
        pila.pop()
        pila.append("L")
        pila.append("E")
        bor_pila(sig_token)
    elif (sig_token==')'):
        parser_out.write('42 ')
        bor_pila(sig_token)
def p_L(sig_token):
    if (sig_token==')'):
        pila.pop()
        parser_out.write('44 ')
        if (pila[-1]==sig_token):
            sig_token = act_pila()
        bor_pila(sig_token)
    elif(sig_token==','):
        parser_out.write('43 ')
        pila.append("E")
        pila.append(",")
        if (pila[-1]==sig_token):
            sig_token = act_pila()
        bor_pila(sig_token)
def p_M(sig_token):
    if(sig_token =='boolean' or sig_token=='number' or sig_token=='string'):
        parser_out.write('45 ')
        pila.pop()
        pila.append("D")
        bor_pila(sig_token)
    elif(sig_token== 'id'):
        pila.pop()
        parser_out.write('46 ')
        if (pila[-1]==sig_token):
            sig_token = act_pila()
        
        bor_pila(sig_token)
def p_N(sig_token):
    if (sig_token==')'):
        parser_out.write('48 ')
        bor_pila(sig_token)
    elif (sig_token =='boolean' or sig_token=='number' or sig_token=='string'):
        parser_out.write('47 ')
        pila.pop()
        pila.append("O")
        pila.append("id")
        pila.append("D")
        p_D(sig_token)
def p_O(sig_token):
    if(sig_token==')'):
        pila.pop()
        parser_out.write('50 ')
        sig_token=act_pila()
        p_C(sig_token)
    elif(sig_token ==',') : 
        parser_out.write('49 ')
        pila.append("id")
        pila.append("D")
        pila.append(",")
        if (pila[-1]==sig_token):
            sig_token = act_pila()
        p_D(sig_token)
def p_Q(sig_token):
    if (sig_token==')' or sig_token=='id' or sig_token== 'cteEntera'
       or sig_token== 'cadena'):
        parser_out.write('51 ')
        pila.pop()
        pila.append("E")
        bor_pila(sig_token)
    elif(sig_token==';'):
        pila.pop()
        parser_out.write('52')
        if (pila[-1]==sig_token):
            sig_token = act_pila()
        bor_pila(sig_token)
        
def p_R(sig_token):
    if(sig_token=='break'):
        parser_out.write('60 ')
        pila.append(";")
        pila.append("break")
        if (pila[-1]==sig_token):
            sig_token = act_pila()
        p_R(sig_token)  
    elif(sig_token=='}'):
        parser_out.write('61 ')
        bor_pila(sig_token)
def p_Y(sig_token):
    if(sig_token=='case'):
        parser_out.write('54 ')
        pila.pop()
        pila.append("Yp")
        pila.append("C")
        pila.append(":")
        pila.append("E")
        pila.append("case")
        if (pila[-1]==sig_token):
            sig_token = act_pila()
        p_E(sig_token) 
    elif(sig_token=='}'):
        parser_out.write('55 ')
        bor_pila(sig_token)
    elif(sig_token=='default'):
        parser_out.write('58 ')
        pila.pop()
        pila.append("R")
        pila.append("C")
        pila.append(":")
        pila.append("default")
        if (pila[-1]==sig_token):
            sig_token = act_pila()
        p_C(sig_token)
def p_Yp(sig_token):
    if(sig_token== 'break'):
        parser_out.write('57 ')
        pila.append(";")
        pila.append("break")
        if (pila[-1]==sig_token):
            sig_token = act_pila()
        bor_pila(sig_token)
    elif(sig_token=='case'):
        parser_out.write('56 ')
        pila.append("C")
        pila.append(":")
        pila.append("E")
        pila.append("case")
        if (pila[-1]==sig_token):
            sig_token = act_pila()
        bor_pila(sig_token)
    elif(sig_token=='}'):
        pila.pop()
        parser_out.write('59 ')
        if (pila[-1]==sig_token):
            sig_token = act_pila()
        bor_pila(sig_token)
def p_Z(sig_token):
    if(sig_token=='switch'):
        parser_out.write('53 ')
        pila.pop()
        pila.append("}")
        pila.append("Y")
        pila.append("{")
        pila.append(")")
        pila.append("E")
        pila.append("(")
        pila.append("switch")
        if (pila[-1]==sig_token):
            sig_token = act_pila()
            p_E(sig_token)



for line in lista_tokens:
    tokens_actual.append(equipara(line))
tokens_actual.append("$")
p_A(tokens_actual[0])

# Imprimir tabla de símbolos.
# Tabla principal
ts_out.write("Tabla Principal #0:\n")
for lexem in ts_types:
    s_type = ts_types[lexem]
    ts_out.write("\t*'" + str(lexem) + "'\n")
    ts_out.write("\t+Tipo:\t\t'" + str(s_type) + "'\n")
    if s_type != "func":
        ts_out.write("\t+Despl:\t\t" + str(ts_displacements[lexem]) + "\n")
    else:
        parameters = ts_func_parameters[lexem]
        ts_out.write("\t+TipoRetorno:\t\t'" + str(ts_func_return_types[lexem]) + "'\n")
        ts_out.write("\t+numParam:\t\t" + str(len(parameters)) + "\n")
        param_index = 1
        for param in parameters:
            ts_out.write("\t+TipoParam" + str(param_index) + ":\t\t'" + str(parameters[param]) + "'\n")
            ts_out.write("\t+ModoParam" + str(param_index) + ":\t\t1\n")
            param_index += 1
        ts_out.write("\t+EtiqFuncion:\t\t'" + str(ts_func_tags[lexem]) + "'\n")
    ts_out.write("\n")

# Tablas de símbolos de cada función.
ts_index = 1
for f_lexem in ts_func_tags:
    ts_out.write("Tabla de la función " + str(f_lexem) + " #" + str(ts_index) + ":\n")
    symbols = ts_func_symbols[f_lexem]
    if symbols != 0:
        for s_lexem in symbols:
            ts_out.write("\t*'" + str(s_lexem) + "'\n")
            ts_out.write("\t+Tipo:\t\t'" + str(symbols[s_lexem][0]) + "'\n")
            ts_out.write("\t+Despl:\t\t" + str(symbols[s_lexem][1]) + "\n\n")
        ts_out.write("\n")
        ts_index += 1
   