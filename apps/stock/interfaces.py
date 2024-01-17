from .models import *

class tiposMercancia():

    valor:float
    tipoDeProducto:tipoProducto
    cuenta:any


    def __init__(self,tipo,cuenta,valor):

        self.tipoDeProducto = tipo
        self.cuenta         = cuenta
        self.valor          = valor

class pagosCuentas():

    valor:float
    cuenta:any


    def __init__(self,cuenta,valor):
        self.cuenta         = cuenta
        self.valor          = valor