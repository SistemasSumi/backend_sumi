def update_factura_pago(sender,instance,**kwargs):
    print("entro")
    print(instance)
    instance.pago.total  += instance.totalAbono
    instance.pago.save()


    
def delete_factura_pago(sender,instance,**kwargs):
    instance.pago.total  -= instance.totalAbono
    instance.pago.save()