


import math

def convertir_choice_diccionario(valor:any,choice:tuple):
    for x in choice:
        resultado = list(x)
        if resultado[0] == valor:
            d = dict()
            d['nombre']=resultado[1] 
            d['valor'] =resultado[0] 
            return d
    
    return None

def redondear_al_50Cercano(valor:float):
    if valor%50 == 0:
        return valor
    else:
        
        return (math.floor(valor/50)+1)*50
    


