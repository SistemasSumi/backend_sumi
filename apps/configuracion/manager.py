from django.db import models


class ImpuestosEnGeneralManager(models.Manager):
    def create_impuesto(self, tipo, doc_referencia, impuesto,tercero, base, porcentaje, total,fecha, ventas=False, compras=False,):
        """
        Crea un nuevo registro de ImpuestosEnGeneral con los valores proporcionados.

        Parámetros:
        - tipo: Valor del campo tipo.
        - doc_referencia: Valor del campo docReferencia.
        - impuesto: Instancia de la clase Impuestos relacionada.
        - base: Valor del campo base.
        - porcentaje: Valor del campo porcentaje.
        - total: Valor del campo total.
        - ventas: Valor booleano para el campo ventas (opcional, valor predeterminado False).
        - compras: Valor booleano para el campo compras (opcional, valor predeterminado False).

        Ejemplo de uso:
        create_impuesto(tipo=ImpuestosEnGeneral.MOVIMIENTO, doc_referencia='ABC123', impuesto=impuesto, base=100.0, porcentaje=10.0, total=110.0, ventas=True)
        """
        impuesto_en_general = self.create(
            tipo=tipo,
            docReferencia=doc_referencia,
            Impuesto=impuesto,
            tercero=tercero,
            base=base,
            porcentaje=porcentaje,
            ventas=ventas,
            compras=compras,
            total=total,
            fecha = fecha
        )
        return impuesto_en_general

    def delete_impuesto(self, tipo, doc_referencia, base,fecha,impuesto,tercero):
        """
        Elimina los registros de RetencionesEnGeneral según los criterios de búsqueda proporcionados.

        Parámetros:
        - tipo: Valor del campo tipo a buscar.
        - doc_referencia: Valor del campo docReferencia a buscar.
        - base: Valor del campo base a buscar.

        Ejemplo de uso:
        delete_retencion(tipo=RetencionesEnGeneral.MOVIMIENTO, doc_referencia='ABC123', base=100.0)
        """
        impuestos = self.filter(tipo=tipo, docReferencia=doc_referencia, base=base,fecha=fecha,Impuesto = impuesto,tercero= tercero)
        impuestos.delete()
    
    


class RetencionesEnGeneralManager(models.Manager):
    def create_retencion(self, tipo, doc_referencia, retencion,tercero, base, porcentaje, total,fecha, ventas=False, compras=False):
        """
        Crea un nuevo registro de RetencionesEnGeneral con los valores proporcionados.

        Parámetros:
        - tipo: Valor del campo tipo.
        - doc_referencia: Valor del campo docReferencia.
        - retencion: Instancia de la clase Retenciones relacionada.
        - base: Valor del campo base.
        - porcentaje: Valor del campo porcentaje.
        - total: Valor del campo total.
        - ventas: Valor booleano para el campo ventas (opcional, valor predeterminado False).
        - compras: Valor booleano para el campo compras (opcional, valor predeterminado False).

        Ejemplo de uso:
        create_retencion(tipo=RetencionesEnGeneral.MOVIMIENTO, doc_referencia='ABC123', retencion=retencion, base=100.0, porcentaje=10.0, total=110.0, ventas=True)
        """
        retencion_en_general = self.create(
            tipo=tipo,
            docReferencia=doc_referencia,
            retencion=retencion,
            tercero=tercero,
            base=base,
            porcentaje=porcentaje,
            ventas=ventas,
            compras=compras,
            fecha=fecha,
            total=total
        )
        return retencion_en_general

    def update_retencion(self, tipo, doc_referencia, base, **kwargs):
        """
        Actualiza los registros de RetencionesEnGeneral según los criterios de búsqueda proporcionados.

        Parámetros:
        - tipo: Valor del campo tipo a buscar.
        - doc_referencia: Valor del campo docReferencia a buscar.
        - base: Valor del campo base a buscar.
        - kwargs: Pares de clave-valor para actualizar los campos especificados.

        Ejemplo de uso:
        update_retencion(tipo=RetencionesEnGeneral.MOVIMIENTO, doc_referencia='ABC123', base=100.0, total=150.0)
        """
        retenciones = self.filter(tipo=tipo, docReferencia=doc_referencia, base=base)
        retenciones.update(**kwargs)
        return retenciones

    def delete_retencion(self, tipo, doc_referencia, base,fecha,retencion,tercero):
        """
        Elimina los registros de RetencionesEnGeneral según los criterios de búsqueda proporcionados.

        Parámetros:
        - tipo: Valor del campo tipo a buscar.
        - doc_referencia: Valor del campo docReferencia a buscar.
        - base: Valor del campo base a buscar.

        Ejemplo de uso:
        delete_retencion(tipo=RetencionesEnGeneral.MOVIMIENTO, doc_referencia='ABC123', base=100.0)
        """
        retenciones = self.filter(tipo=tipo, docReferencia=doc_referencia, base=base,fecha=fecha,retencion = retencion,tercero= tercero)
        retenciones.delete()
    

    
                    





        
