from apps.stock.models import *
from .models import *
from datetime import datetime
import base64
import xml.etree.cElementTree as ET


class tiposMercancia():

    valor:float
    valor_ingreso:float
    tipoDeProducto:tipoProducto
    cuenta:any


    def __init__(self,tipo,cuenta,valor,valor_ingreso):

        self.tipoDeProducto = tipo
        self.cuenta         = cuenta
        self.valor          = valor
        self.valor_ingreso  = valor_ingreso

class pagosCuentas():

    valor:float
    cuenta:any


    def __init__(self,cuenta,valor):
        self.cuenta         = cuenta
        self.valor          = valor

class GenerateRequestFE():
    factura      : CxcMovi
    username     : str = "901648084"
    password     : str = "7c2e86b304545a4f4cd6b3a299514c87996d1794dd17b35ecb639d2eb91e230d"
    transaccionID: str
    prefijo      : str
    folio        : str
    xmlBase64    : str


    def __init__(self,factura:CxcMovi):
        self.factura = factura
    
    
        
    
    def documentStatusFile(self):
        
        soap = f"""<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                            <soap:Body>
                                <documentStatusFile xmlns="http://webservice.facturatech.co/">
                                    <username>{self.username}</username>
                                    <password>{self.password}</password>
                                    <transaccionID>{self.factura.transaccionID}</transaccionID>
                                </documentStatusFile>
                            </soap:Body>
                            </soap:Envelope>"""
        
        return soap
          
    def uploadInvoiceFile(self,xml:str):
        xmlbase = ""
        # with open("facturas/"+self.factura.numero+".xml", "rb") as file:
        #     encoded = base64.encodebytes(file.read()).decode("utf-8")
        #     xmlbase = encoded
        
        soap = f"""<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                            <soap:Body>
                                <uploadInvoiceFile xmlns="http://webservice.facturatech.co/">
                                <username>{self.username}</username>
                                <password>{self.password}</password>
                                <xmlBase64>{xml}</xmlBase64>
                                </uploadInvoiceFile>
                            </soap:Body>
                    </soap:Envelope>"""
        return soap
    
    def documentStatusFile(self):
        soap = f"""<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                            <soap:Body>
                                <documentStatusFile xmlns="http://webservice.facturatech.co/">
                                    <username>{self.username}</username>
                                    <password>{self.password}</password>
                                    <transaccionID>{self.factura.transaccionID}</transaccionID>
                                </documentStatusFile>
                            </soap:Body>
                    </soap:Envelope>"""
        return soap
        
    def downloadCUFEFile(self):
        soap = f"""<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                            <soap:Body>
                                <downloadCUFEFile xmlns="http://webservice.facturatech.co/">
                                    <username>{self.username}</username>
                                    <password>{self.password}</password>
                                    <prefijo>{self.factura.prefijo}</prefijo>
                                    <folio>{str(self.factura.consecutivo)}</folio>
                                </downloadCUFEFile>
                            </soap:Body>
                    </soap:Envelope>"""
        print(soap)
        return soap
    
    def downloadPDFFile(self):
        soap = f"""<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                            <soap:Body>
                                <downloadPDFFile xmlns="http://webservice.facturatech.co/">
                                    <username>{self.username}</username>
                                    <password>{self.password}</password>
                                    <prefijo>{self.factura.prefijo}</prefijo>
                                    <folio>{self.factura.consecutivo}</folio>
                                </downloadPDFFile>
                            </soap:Body>
                    </soap:Envelope>"""
        return soap
        
    def downloadQRFile(self):
        soap = f"""<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                            <soap:Body>
                                <downloadQRFile xmlns="http://webservice.facturatech.co/">
                                    <username>{self.username}</username>
                                    <password>{self.password}</password>
                                    <prefijo>{self.factura.prefijo}</prefijo>
                                    <folio>{str(self.factura.consecutivo)}</folio>
                                </downloadQRFile>
                            </soap:Body>
                    </soap:Envelope>"""
        return soap
    
    def downloadQRImageFile(self):
        soap = f"""<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                            <soap:Body>
                                <downloadQRImageFile xmlns="http://webservice.facturatech.co/">
                                    <username>{self.username}</username>
                                    <password>{self.password}</password>
                                    <prefijo>{self.factura.prefijo}</prefijo>
                                    <folio>{str(self.factura.consecutivo)}</folio>
                                </downloadQRImageFile>
                            </soap:Body>
                    </soap:Envelope>"""
        return soap
        
    def downloadXMLFile(self):
        soap = f"""<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                            <soap:Body>
                                <uploadInvoiceFile xmlns="http://webservice.facturatech.co/">
                                    <username>{self.username}</username>
                                    <password>{self.password}</password>
                                    <prefijo>{self.factura.prefijo}</prefijo>
                                    <folio>{str(self.factura.consecutivo)}</folio>
                                </uploadInvoiceFile>
                            </soap:Body>
                    </soap:Envelope>"""
        return soap
    
    def crear_xml_factura(self):
        try:
        
        
            # llamada de todos los datos relacionados ala factura de venta

            # primero llamamos a la clase cxcmovi donde se contiene la factura 
            cxc = self.factura

            # luego llamados al detalle de esa factura 

            listaDetalle = CxcMoviDetalle.objects.filter(factura__id = cxc.id)

            # luego llamamos a los posibles impuestos de esa factura 
            impuestos  = ImpuestoCxc.objects.filter(factura__id = cxc.id)

            # luego llamamos a las posibles retenciones que tenga dicha factura

            retenciones = RetencionCxc.objects.filter(factura__id = cxc.id)

            print(cxc.valorIva)
            print("detalle")
            print(*listaDetalle)
            print("impuestos")

            print(*impuestos)
            print("retenciones")

            print(*retenciones)


            factura = ET.Element('FACTURA')
            factura.set("xmlns:xsd","http://www.w3.org/2001/XMLSchema")  
            factura.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")  

            ENC   = ET.SubElement(factura,'ENC')
            # Identificador del tipo de documento. INVOICE,ND,NC
            ENC_1 = ET.SubElement(ENC,'ENC_1').text="INVOIC"
            # Identificación del obligado a facturar electrónico - NIT. 
            ENC_2 = ET.SubElement(ENC,'ENC_2',).text="901648084"
            # Identificación del adquiriente - NIT. 
            ENC_3 = ET.SubElement(ENC,'ENC_3',).text=str(cxc.cliente.documento)
            # Versión del esquema UBL USAR UBL 2.1
            ENC_4 = ET.SubElement(ENC,'ENC_4',).text="UBL 2.1"
            # Identificación del adquiriente - NIT. DIAN 2.1
            ENC_5 = ET.SubElement(ENC,'ENC_5',).text="DIAN 2.1"
            #Número de documento (factura o factura cambiaria, nota crédito, nota débito). Incluye prefijo + consecutivo de factura autorizados por la DIAN.         
            #No se permiten caracteres adicionales como espacios o guiones
            ENC_6 = ET.SubElement(ENC,'ENC_6',).text=str(cxc.prefijo+str(cxc.consecutivo))
            # Fecha de emisión de la factura/nota. Formato AAAA-MM-DD
            ENC_7 = ET.SubElement(ENC,'ENC_7',).text=cxc.fecha.strftime("%Y-%m-%d")
            # Formato: HH:MM:SSdhh:mm
            ENC_8 = ET.SubElement(ENC,'ENC_8',).text=str(cxc.hora.strftime("%H:%M:%S")+'-05:00')
            # ver nota 35 01 lo tienen los EJEMPLOS
            # FACTURA ES 01 NC ES 91 ND ES 92
            ENC_9 = ET.SubElement(ENC,'ENC_9',).text="01"
            # carrer 6 ENTRE 11 - 34
            # M0NEDA LOCAL
            ENC_10 = ET.SubElement(ENC,'ENC_10',).text="COP"

            # Número total de líneas en el documento.
            ENC_15 = ET.SubElement(ENC,'ENC_15',).text=str(len(listaDetalle))
            # FECHA DE VENCIMIENTO DE LA FACTURA
            ENC_16 = ET.SubElement(ENC,'ENC_16',).text=cxc.fecha.strftime("%Y-%m-%d")
            # VALIDACION DE AMBIENTE PRODUCCION 1 PRUEBAS 2
            ENC_20 = ET.SubElement(ENC,'ENC_20',).text="1"
            # Indicador del tipo de operación 10 ES Estándar
            ENC_21 = ET.SubElement(ENC,'ENC_21',).text="10"
            
            EMI   = ET.SubElement(factura,'EMI')
            # tipo de IDENTIFICACION 1 Persona Jurídica y asimiladas   2 Persona Natural y asimiladas
            EMI_1 = ET.SubElement(EMI,'EMI_1').text="1"
            # NIT DE EMISOR SIN DIGITO NI PUNTOS
            EMI_2 = ET.SubElement(EMI,'EMI_2').text="901648084"
            # DEBE SER 31
            EMI_3 = ET.SubElement(EMI,'EMI_3').text="31"
            # 48	Impuestos sobre la venta del IVA
            # 49	No responsables del IVA
            EMI_4 = ET.SubElement(EMI,'EMI_4').text="48"
            # NOMBRE  DE LA RAZON SOCIAL DEL EMISOR
            EMI_6 = ET.SubElement(EMI,'EMI_6').text="SUMIPROD DE LA COSTA S.A.S."
            EMI_7 = ET.SubElement(EMI,'EMI_7').text="SUMIPROD DE LA COSTA S.A.S."
            # DIRECCION SIN CIUDAD Y DEPARTAMENTO
            EMI_10 = ET.SubElement(EMI,'EMI_10').text="Calle 44B #21G-11 URB Santa Cruz"
            # CODIGO DEL DEPARTAMENTO MAGDALENA ES 47 
            EMI_11 = ET.SubElement(EMI,'EMI_11').text="47"

            # NOMBRE DE LA CUIDAD DEL EMISOR
            EMI_13 = ET.SubElement(EMI,'EMI_13').text="SANTA MARTA"

            # CODIGO POSTAL  santa marta 470001

            EMI_14 = ET.SubElement(EMI,'EMI_14').text="470001"
            # CODIGO DEL PAIS ALFA-2 ES: CO
            EMI_15 = ET.SubElement(EMI,'EMI_15').text="CO"

            #NOMBRE DEL DEPARTAMENTO Magdalena
            EMI_19 = ET.SubElement(EMI,'EMI_19').text="Magdalena"


            #NOMBRE DEL PAIS Colombia

            EMI_21 = ET.SubElement(EMI,'EMI_21').text="Colombia"

            #DIGITO DE VERIFICACION DEL NIT - 5
            EMI_22= ET.SubElement(EMI,'EMI_22').text="9"

            #CODIGO DEL MUNICIPIO 47001
            EMI_23 = ET.SubElement(EMI,'EMI_23').text="47001"
            # NOMBRE REGISTRADO EN EL RUT  <EMI_7> LEYZA ANDREA PEREZ MASS
            EMI_24 = ET.SubElement(EMI,'EMI_24').text="SUMIPROD DE LA COSTA S.A.S."
            # ACTIVIDAD ECONOMICA CODIGO 
            # EMI_25 = ET.SubElement(EMI,'EMI_25').text="4645"

            TAC   = ET.SubElement(EMI,'TAC')
            # OBLIGACIONES DEL CONTRIBUYENTE
            TAC_1 = ET.SubElement(TAC,'TAC_1').text="R-99-PN"

            DFE   = ET.SubElement(EMI,'DFE')
            # CODIGO DEL MUNICIPIO
            DFE_1 = ET.SubElement(DFE,'DFE_1').text="47001"
            # CODIGO DEL DEPARTAMENTO MAGDALENA ES 47
            DFE_2 = ET.SubElement(DFE,'DFE_2').text='47'
            # CODIGO IDENTIFICADOR DEL PAIS ES: CO
            DFE_3 = ET.SubElement(DFE,'DFE_3').text='CO'
            # CODIGO POSTAL SANTA MARTA 470001
            DFE_4 = ET.SubElement(DFE,'DFE_4').text='470001'
            # NOMBRE DEL PAIS Colombia
            DFE_5 = ET.SubElement(DFE,'DFE_5').text='Colombia'
            # NOMBRE DEL departamento 
            DFE_6 = ET.SubElement(DFE,'DFE_6').text='Magdalena'
            # NOMBRE DE LA CIUDAD DEL EMISOR SANTA MARTA
            DFE_7 = ET.SubElement(DFE,'DFE_7').text='SANTA MARTA'
            # DIRECCION DEL EMISOR SIN CIUDAD NI DEPA
            DFE_8 = ET.SubElement(DFE,'DFE_8').text='Calle 44B #21G-11 URB Santa Cruz'

            # NUMERO DE REGISTRO MERCANTIL 184312
            ICC   = ET.SubElement(EMI,'ICC')
            ICC_1 = ET.SubElement(ICC,'ICC_1').text='262150'
            #  PREFIJO 
            ICC_9 = ET.SubElement(ICC,'ICC_9').text='SUM'

            CDE   = ET.SubElement(EMI,'CDE')
            # TIPO DE CONTACTO, DEL EMISOR PERSONA DE  CONTACTO
            CDE_1 = ET.SubElement(CDE,'CDE_1').text='1'
            # NOMBRE Y CARGO DE LA PERSONA DE CONTACTO 
            CDE_2 = ET.SubElement(CDE,'CDE_2').text='Enrique de jesus rosado navarro'
            # TELEFONO DE LA PERSONA DE CONTACTO
            CDE_3 = ET.SubElement(CDE,'CDE_3').text='(5) 4327722-Cel: 3013022986'
            # CORREO ELECTRONICO DE LA PERSONA DE CONTACTO
            CDE_4 = ET.SubElement(CDE,'CDE_4').text='SUMIPRODELACOSTA@GMAIL.COM'

            GTE   = ET.SubElement(EMI,'GTE')
            # CODIGO DE IVA ES 01
            GTE_1 = ET.SubElement(GTE,'GTE_1').text='01'
            # NOMBRE DEL TRIBUTO ES IVA
            GTE_2 = ET.SubElement(GTE,'GTE_2').text='IVA'


            ADQ   = ET.SubElement(factura,'ADQ')
            # 1   PERSONA JURIDICA Y ASIMILADAS
            # 2   PERSONA NATURAL  Y ASIMILADAS
            ADQ_1 = ET.SubElement(ADQ,'ADQ_1').text=str(cxc.cliente.tipoPersona)

            # NIT DEL ADQUIRIENTE SIN . NI -  SOLO VALIDO PARA FACTURAS
            ADQ_2 =ET.SubElement(ADQ,'ADQ_2').text=str(cxc.cliente.documento)
            # TIPO DE DOCUMENTO DE IDENTIFICACION FISCAL DE LA PERSONA 31 = NIT 13 = CEDULA
            if cxc.cliente.tipoDocumento == 'NIT':
                ADQ_3 =ET.SubElement(ADQ,'ADQ_3').text='31'
            else:
                ADQ_3 =ET.SubElement(ADQ,'ADQ_3').text='13'
                
            # REGIMENN AL Q PERTENECE  
            # IMPUESTO SOBRE LA VENTADEL IVA
            # CAMPO OPCIONAL
            if cxc.cliente.regimen == 'Responsable del IVA':
                ADQ_4 =ET.SubElement(ADQ,'ADQ_4').text='48'
            else:
                ADQ_4 =ET.SubElement(ADQ,'ADQ_4').text='49'

            # RAZON SOCIAL DEL CLIENTE REGISTRADO EN EL RUT
            ADQ_6 =ET.SubElement(ADQ,'ADQ_6').text=str(cxc.cliente.nombreComercial)

            # NOMBRE COMERCIAL DEL ADQUIRIENTE
            ADQ_7 =ET.SubElement(ADQ,'ADQ_7').text=str(cxc.cliente.nombreComercial)

            tipoPersona = cxc.cliente.tipoPersona
            if tipoPersona == '2':
                print("el tipo de persona es:")
                print(tipoPersona)
                # NOMBRE DEL ADQUIRIENTE
                # OBLIGATORIO SI ES ADQ_1 = 2 
                ADQ_8 = ET.SubElement(ADQ,'ADQ_8').text=str(cxc.cliente.nombreComercial)
                # APELLIDO
                # OBLIGATORIO SI ADQ_8 SE INFORRMO
                ADQ_9 = ET.SubElement(ADQ,'ADQ_9').text=str(cxc.cliente.nombreComercial)

            # EL EMISOR PUEDE USAR PARA SU DIRECCION (TEXTO LIBRE)
            ADQ_10 = ET.SubElement(ADQ,'ADQ_10').text=str(cxc.cliente.direccion)

            # CODIGO DEL DEPARTAMENTO MAGADALE ES 47
            ADQ_11 = ET.SubElement(ADQ,'ADQ_11').text=str(cxc.cliente.departamento.codigo.replace(".", ""))

            # NOMBRE DE LA CIUDAD DEL ADQ
            ADQ_13 = ET.SubElement(ADQ,'ADQ_13').text=str(cxc.cliente.municipio.municipio)

            # validar codigo postal
            if cxc.cliente.codigoPostal:
                ADQ_14 = ET.SubElement(ADQ,'ADQ_14').text=str(cxc.cliente.codigoPostal)
            #CODIGO IDENTIFICADOR DEL PAIS ES CO
            ADQ_15 = ET.SubElement(ADQ,'ADQ_15').text='CO'
            #NOMBRE DEL DEPARTAMENTO
            ADQ_19 = ET.SubElement(ADQ,'ADQ_19').text=str(cxc.cliente.departamento.departamento)
            # NOMBRE DEL PAIS es Colombia
            ADQ_21 = ET.SubElement(ADQ,'ADQ_21').text='Colombia'
            #DIGITO DE VERIFICACION DEL CLIENTE SI ESTA IDENTIFICADO POR NIT
            if cxc.cliente.tipoDocumento == 'NIT':
                ADQ_22 = ET.SubElement(ADQ,'ADQ_22').text=str(cxc.cliente.dv)
            # CODIGO DEL MUNICIPIO SANTA MARTA ES 47001
            print(cxc.cliente.municipio.codigo.replace(".", ""))
            ADQ_23 = ET.SubElement(ADQ,'ADQ_23').text=str(cxc.cliente.municipio.codigo.replace(".", ""))
            #IDENTIFICAION DEL ADQUIRIENTE 
            #SE GENERA SI EL VALOR DE ADQ_1 = "2" Y ESTE NO ES MENCIONADO
            #DUDAD EN CUAL ES EL VALOR DE ESTE CAMPO
            # ADQ_24 = ET.SubElement(ADQ,'ADQ_24').text='1'

            TCR   = ET.SubElement(ADQ,'TCR')
            #OBLIGACIONES DEL CONTRIBUYENTE O-05;O-48;O-52
            #SI DESCONOCE USE O-99
            TCR_1 = ET.SubElement(TCR,'TCR_1').text='R-99-PN'

            ILA   = ET.SubElement(ADQ,'ILA')
            #NOMBRE REGISTRADO EN EL RUT DEL CLIENTE
            ILA_1 = ET.SubElement(ILA,'ILA_1').text=str(cxc.cliente.nombreComercial)
            #IDENTIFICADOR DEL ADQUIERIENTE
            ILA_2 = ET.SubElement(ILA,'ILA_2').text=str(cxc.cliente.documento)
            # TIPO DE DOCUMENTO DE IDENTIFICAION 13 = CEDULA 31 ES = NIT
            if cxc.cliente.tipoDocumento == 'NIT':
                ILA_3 = ET.SubElement(ILA,'ILA_3').text='31'
            else:
                ILA_3 = ET.SubElement(ILA,'ILA_3').text='13'
                
            if cxc.cliente.tipoDocumento == 'NIT':
            #DIGITO DE VERIFICACION DEL ADQUIRIENTE SI SE IDENTIFICA CON NIT
                ILA_4 = ET.SubElement(ILA,'ILA_4').text=str(cxc.cliente.dv)
        
            DFA   = ET.SubElement(ADQ,'DFA')
            # CODIGO INDICADOR DEL PAIS CO
            DFA_1 = ET.SubElement(DFA,'DFA_1').text='CO'
            # CODIGO DEL DEPARTAMENTO DEL CLIENTE
            DFA_2 = ET.SubElement(DFA,'DFA_2').text=str(cxc.cliente.departamento.codigo.replace(".", ""))
            # CODIGO POSTAL
            DFA_3 = ET.SubElement(DFA,'DFA_3').text=str(cxc.cliente.codigoPostal)
            # CODIGO DEL MUNICIPIO
            DFA_4 = ET.SubElement(DFA,'DFA_4').text=str(cxc.cliente.municipio.codigo.replace(".", ""))
            # NOMBRE DEL PAIS DEL CIENTE Colombia
            DFA_5 = ET.SubElement(DFA,'DFA_5').text='Colombia'
            # NOMBRE DEL DEPARTAMENTO DEL CIENTE
            DFA_6 = ET.SubElement(DFA,'DFA_6').text=str(cxc.cliente.departamento.departamento)
            # NOMBRE DE LA CIUDAD DEL CIENTE
            DFA_7 = ET.SubElement(DFA,'DFA_7').text=str(cxc.cliente.municipio.municipio)
            # DIRECCION DEL CLIENTE TEXTO LIBRE
            DFA_8 = ET.SubElement(DFA,'DFA_8').text=str(cxc.cliente.direccion)

            
            if tipoPersona == 1:
                ICR   = ET.SubElement(ADQ,'ICR')
                #NUMERO DE MATRICULA MERCANTIL SI ADQ_1 ES 1                    
                #184312 ES DE LEYZA DEBE SER DEL CLIENTE SI ADQ ES 1
                ICR_1 = ET.SubElement(ICR,'ICR_1').text=str(cxc.cliente.matriculaMercantil)
            
            CDA   = ET.SubElement(ADQ,'CDA')
            #TIPO DE CONTACTO DEL ADQUIRIENTE ESCOJO 1
            CDA_1 = ET.SubElement(CDA,'CDA_1').text='1'
            # NOMBRE DE LA PERSONA DE CONTACTO
            CDA_2 = ET.SubElement(CDA,'CDA_2').text=str(cxc.cliente.nombreContacto)
            # TELEFONO DE LA PERSONA DE CONTACTO
            CDA_3 = ET.SubElement(CDA,'CDA_3').text=str(cxc.cliente.telefonoContacto)
            #CORREO DE CONTACTO DE QUIEN VA A RECIBIR LA FACTURA
            CDA_4 = ET.SubElement(CDA,'CDA_4').text=str(cxc.cliente.correoFacturas)

            GTA   = ET.SubElement(ADQ,'GTA')
            # IDENTIFICADOR DEL TRIBUTO
            # CODIGO DE IVA ES 01
            # CODIGO DE IC IMPUESTO AL CONSUMO ES 02
            # CODIGO DE ICA ES 03
            # CODIGO DE INC ES 04
            # CODIGO DE RETEIVA ES 05
            # CODIGO DE RETEFUENTE ES 06
            # CODIGO DE RETEICA ES 07

            GTA_1 = ET.SubElement(GTA,'GTA_1').text='01'
            # NOMBRE DEL TRIBUTO ES IVA DEPENDE DEL CODIGO EN GTA_1
            GTA_2 = ET.SubElement(GTA,'GTA_2').text='IVA'

            TOT   = ET.SubElement(factura,'TOT')
            # VALOR BRUTO O SUBTOTAL DE LA FACTURA 
            TOT_1 = ET.SubElement(TOT,'TOT_1').text=str(cxc.subtotal-cxc.descuento)
            # MONEDA USADA
            TOT_2 = ET.SubElement(TOT,'TOT_2').text='COP'
            if impuestos:
                imp = impuestos[0]
            # BASES IMPONIBLES PARA CALCULAR LOS TRIBUTOS OSEA EL SUBTOTAL QUE SE LE APLICA EL IVA Y LA RETEFUENTE ETC...
                TOT_3 = ET.SubElement(TOT,'TOT_3').text=str(imp.base)
            else:
                TOT_3 = ET.SubElement(TOT,'TOT_3').text=str(0)
            # MONESDA USADA
            TOT_4 = ET.SubElement(TOT,'TOT_4').text='COP'
            # VALOR TOTAL DE LA FACTURA
            TOT_5 = ET.SubElement(TOT,'TOT_5').text=str(cxc.valor+cxc.valorReteFuente)
            # MONESDA USADA
            TOT_6 = ET.SubElement(TOT,'TOT_6').text='COP'
            #VALOR TOTAL DE LA FACTURA
            TOT_7 = ET.SubElement(TOT,'TOT_7').text=str(cxc.valor+cxc.valorReteFuente)
            # MONEDA USADA
            TOT_8 = ET.SubElement(TOT,'TOT_8').text='COP'


            # SI EL IVA  ES 0 ENTONCES TIM NO APLICA 
            if cxc.valorIva > 0:
                print("el valor del iva entro")

                for x in impuestos:
                    print("impuesto")
                    TIM   = ET.SubElement(factura,'TIM')

                    # true o false si somos autoretenedores
                    TIM_1 = ET.SubElement(TIM,'TIM_1').text='false'
                    # VALOR DEL IVA
                    TIM_2 = ET.SubElement(TIM,'TIM_2').text=str(x.total)
                    # MONEDA LOCAL
                    TIM_3 = ET.SubElement(TIM,'TIM_3').text='COP'

                    IMP   = ET.SubElement(TIM,'IMP')
                    # 01 ES EL IDENTIFICADOR DEL TRIBUTO IVA
                    IMP_1 = ET.SubElement(IMP,'IMP_1').text='01'

                    # BASE IMPONIBLE PARA CALCULAR EL TRIBUTO
                    IMP_2 = ET.SubElement(IMP,'IMP_2').text=str(x.base)

                    # MONEDA LOCAL ES COP
                    IMP_3 = ET.SubElement(IMP,'IMP_3').text='COP'

                    # VALOR DEL TRIBUTO IVA IMP_4 * IMP_6
                    IMP_4 = ET.SubElement(IMP,'IMP_4').text=str(x.total)

                    # MONEDA LOCAL ES COP
                    IMP_5 = ET.SubElement(IMP,'IMP_5').text='COP'

                    # porcentaje del iva
                    IMP_6 = ET.SubElement(IMP,'IMP_6').text=str(x.procentaje)

            # CIERRE DEL TIMBRE DEL IVA


            # RETEFUENTE


            for x in retenciones:
                print("retenciones")
                TIM   = ET.SubElement(factura,'TIM')

                # true o false si somos autoretenedores
                TIM_1 = ET.SubElement(TIM,'TIM_1').text='true'
                # VALOR DEL IVA
                TIM_2 = ET.SubElement(TIM,'TIM_2').text=str(x.total)
                # MONEDA LOCAL
                TIM_3 = ET.SubElement(TIM,'TIM_3').text='COP'

                IMP   = ET.SubElement(TIM,'IMP')
                # 01 ES EL IDENTIFICADOR DEL TRIBUTO 
                IMP_1 = ET.SubElement(IMP,'IMP_1').text=x.retencion.tipoRetencion

                # BASE IMPONIBLE PARA CALCULAR EL TRIBUTO
                IMP_2 = ET.SubElement(IMP,'IMP_2').text=str(x.base)

                # MONEDA LOCAL ES COP
                IMP_3 = ET.SubElement(IMP,'IMP_3').text='COP'

                # VALOR DEL TRIBUTO IVA IMP_4 * IMP_6
                IMP_4 = ET.SubElement(IMP,'IMP_4').text=str(x.total)

                # MONEDA LOCAL ES COP
                IMP_5 = ET.SubElement(IMP,'IMP_5').text='COP'

                # porcentaje del iva
                IMP_6 = ET.SubElement(IMP,'IMP_6').text=str(x.procentaje)
            
            DRF   = ET.SubElement(factura,'DRF')
            # NUMERO DE AUTORIZACION O RESOLUCION OTORGADO PARA FAC ELECTRONICA
            DRF_1 = ET.SubElement(DRF,'DRF_1').text=str(cxc.numeracion.resolucion)
            # FECHA DE INICIO DEL PERIODO DE RESOLUCION OTORGADO
            DRF_2 = ET.SubElement(DRF,'DRF_2').text=cxc.numeracion.fecha_inicio.strftime("%Y-%m-%d")
            # FECHA DE FINAL DEL PERIODO DE RESOLUCION OTORGADO
            DRF_3 = ET.SubElement(DRF,'DRF_3').text=cxc.numeracion.fecha_vencimiento.strftime("%Y-%m-%d")
            # PREFIJO DEL RANGO RESOLUCION OTORGADO
            DRF_4 = ET.SubElement(DRF,'DRF_4').text=str(cxc.numeracion.prefijo)
            # RANGO DE NUMERACION MINIMO
            DRF_5 = ET.SubElement(DRF,'DRF_5').text=str(cxc.numeracion.desde)
            # RANGO DE NUMERACION MAXIMO
            DRF_6 = ET.SubElement(DRF,'DRF_6').text=str(cxc.numeracion.hasta)

            # NOTAS DE LA FACTURA / ORSERVACIONES
            NOT   = ET.SubElement(factura,'NOT')
            NOT_1 = ET.SubElement(NOT,'NOT_1').text=str(cxc.observacion)

            # 1 ES INSTRUMENTO NO DEFINIDO
            # CODIGO DEL MEDIO DE PAGO 10 es EFECTIVO
            # 47 TRASNFERENCIA DEBITO BANCARIA

            MEP   = ET.SubElement(factura,'MEP')
            MEP_1 = ET.SubElement(MEP,'MEP_1').text='1'

            # METODO DE PAGO 1 CONTADO 2 CREDITO
            if cxc.formaPago.nombre == 'CONTADO':
                MEP_2 = ET.SubElement(MEP,'MEP_2').text='1'
            else:
                MEP_2 = ET.SubElement(MEP,'MEP_2').text='2'
                # EN CASO DE QUE EL METODO DE PAGO SEA CREDITO
                MEP_3 = ET.SubElement(MEP,'MEP_3').text=cxc.fechaVencimiento.strftime("%Y-%m-%d")


            index   = 0
            for x in listaDetalle:
                print("entro a la lista detalle")
                index+=1

                ITE   = ET.SubElement(factura,'ITE')
                # NUMERO EN ORDEN SECUENCIAL 1,2,3,4,5 ETC
                ITE_1 = ET.SubElement(ITE,'ITE_1').text=str(index)
                # CANTIDAD DEL PRODUCTO POR ITEM
                ITE_3 = ET.SubElement(ITE,'ITE_3').text=str(x.cantidad)
                # IDENTIFICACION DE LA MEDIDAD DE LA CANTIDAD  94 ES unidad
                ITE_4 = ET.SubElement(ITE,'ITE_4').text='94'
                # SUBTOTAL DE LA LINEA ITE_7 * ITE_27
                ITE_5 = ET.SubElement(ITE,'ITE_5').text=str(x.subtotal-(x.descuento*x.cantidad))

                ITE_6 = ET.SubElement(ITE,'ITE_6').text='COP'
                # VALOR UNITARIO DEL PRODUCTO
                ITE_7 = ET.SubElement(ITE,'ITE_7').text=str(x.valor)
                # MONEDA
                ITE_8 = ET.SubElement(ITE,'ITE_8').text='COP'
                # NOMBRE DEL PRODUCTO
                ITE_11 = ET.SubElement(ITE,'ITE_11').text=str(x.producto.nombreymarcaunico+' Lote:'+x.lote+' Vence:')+ str(x.vence)
                # CODIGO DEL PRODCUTO OJO PUEDE SER ITE_18
                ITE_18 = ET.SubElement(ITE,'ITE_18').text=x.producto.codigoDeBarra
                # SUBTOTAL  - DESCUENTOS
                ITE_19 = ET.SubElement(ITE,'ITE_19').text=str(x.subtotal-(x.descuento*x.cantidad))
                # MONEDA LOCAL
                ITE_20 = ET.SubElement(ITE,'ITE_20').text='COP'
                # SUBTOTAL CON IVA INCLUIDO
                ITE_21 = ET.SubElement(ITE,'ITE_21').text=str(x.subtotal-(x.descuento*x.cantidad)+(x.iva*x.cantidad))
                # MONEDA LOCAL
                ITE_22 = ET.SubElement(ITE,'ITE_22').text='COP'
                # CANTIDAD DEL PRODUCTO
                ITE_27 = ET.SubElement(ITE,'ITE_27').text=str(x.cantidad)
                # IDENTIFICACION DE LA MEDIDAD DE LA CANTIDAD  94 ES unidad
                ITE_28 = ET.SubElement(ITE,'ITE_28').text='94'


                IAE   = ET.SubElement(ITE,'IAE')
                # CODIGO DE BARRA
                IAE_1 = ET.SubElement(IAE,'IAE_1').text=x.producto.codigoDeBarra
                IAE_2 = ET.SubElement(IAE,'IAE_2').text='001'

                if x.descuento > 0:
                    IDE   = ET.SubElement(ITE,'IDE')
                    # DESCUENTO ES FALSE
                    IDE_1 = ET.SubElement(IDE,'IDE_1').text='false'
                    # VALOR DEL DESCUENTO 
                    IDE_2 = ET.SubElement(IDE,'IDE_2').text=str(round(x.descuento*x.cantidad, 2))
                    # MONEDA 
                    IDE_3 = ET.SubElement(IDE,'IDE_3').text='COP'
                    # 
                    IDE_5 = ET.SubElement(IDE,'IDE_5').text='Descuento por pago de contado'
                    # DESCUENTO %
                    IDE_6 = ET.SubElement(IDE,'IDE_6').text=str((x.descuento * x.cantidad) / x.subtotal * 100)
                    # SUBTOTAL
                    IDE_7 = ET.SubElement(IDE,'IDE_7').text=str(x.subtotal)
                    # MONEDA
                    IDE_8 = ET.SubElement(IDE,'IDE_8').text='COP'
                    # ROW
                    IDE_10 = ET.SubElement(IDE,'IDE_10').text=str(index)
                
                if x.iva > 0:
                    TII  = ET.SubElement(ITE,'TII')
                    # VALOR DEL IVA POR ITEM
                    print('El inva')
                    print(x.iva*x.cantidad)
                    TII_1 = ET.SubElement(TII,'TII_1').text=str(x.iva*x.cantidad)
                    # MODEDA LOCAL DE COLOMBIA
                    TII_2 = ET.SubElement(TII,'TII_2').text='COP'
                    # true para autoretenedores
                    TII_3 = ET.SubElement(TII,'TII_3').text='false'

                    IIM   = ET.SubElement(TII,'IIM')
                    # CODIGO EQUIVALENTE AL IVA 
                    IIM_1 = ET.SubElement(IIM,'IIM_1').text='01'
                    # VALOR TOTAL DEL IVA POR ITEM 
                    IIM_2 = ET.SubElement(IIM,'IIM_2').text=str(x.iva*x.cantidad)
                    # MODEDA LOCAL DE COLOMBIA
                    IIM_3 = ET.SubElement(IIM,'IIM_3').text='COP'
                    # BASE IMPONIBLE SUBTOTAL
                    IIM_4 = ET.SubElement(IIM,'IIM_4').text=str(x.subtotal-(x.descuento*x.cantidad))
                    # MODEDA LOCAL DE COLOMBIA
                    IIM_5 = ET.SubElement(IIM,'IIM_5').text='COP'
                    # PORCENTAJE DEL IVA APLICADO
                    IIM_6 = ET.SubElement(IIM,'IIM_6').text="19.00"
                
                for j in retenciones:
                    print(f"retenciones: {x.subtotal * j.procentaje / 100}")
                
                    TII  = ET.SubElement(ITE,'TII')
                    # VALOR DEL IVA POR ITEM
                    TII_1 = ET.SubElement(TII,'TII_1').text=str((x.subtotal-(x.descuento*x.cantidad))  * j.procentaje / 100)
                    # MODEDA LOCAL DE COLOMBIA
                    TII_2 = ET.SubElement(TII,'TII_2').text='COP'
                    # true para autoretenedores
                    TII_3 = ET.SubElement(TII,'TII_3').text='true'

                    IIM   = ET.SubElement(TII,'IIM')
                    # CODIGO EQUIVALENTE AL IVA 
                    IIM_1 = ET.SubElement(IIM,'IIM_1').text=str(j.retencion.tipoRetencion)
                    # VALOR TOTAL DEL IVA POR ITEM 
                    IIM_2 = ET.SubElement(IIM,'IIM_2').text=str((x.subtotal-(x.descuento*x.cantidad)) * j.procentaje / 100)
                    # MODEDA LOCAL DE COLOMBIA
                    IIM_3 = ET.SubElement(IIM,'IIM_3').text='COP'
                    # BASE IMPONIBLE SUBTOTAL
                    IIM_4 = ET.SubElement(IIM,'IIM_4').text=str(x.subtotal-(x.descuento*x.cantidad))
                    # MODEDA LOCAL DE COLOMBIA
                    IIM_5 = ET.SubElement(IIM,'IIM_5').text='COP'
                    # PORCENTAJE DEL IVA APLICADO
                    IIM_6 = ET.SubElement(IIM,'IIM_6').text=str(j.procentaje)

            # archivo = ET.ElementTree(factura)
            # archivo.write('facturas/'+cxc.numero+'.xml')

            xml_string = ET.tostring(factura, encoding="utf-8", method="xml")

            # Convertir la cadena XML a base64
            base64_xml = base64.b64encode(xml_string).decode("utf-8")

            # Devolver la cadena base64
            return base64_xml
       
        except Exception as ex:
            print(ex)
            return False

    


class GenerateRequestNC():

    nota:NotaCreditoVentas
    username     : str = "901648084"
    password     : str = "7c2e86b304545a4f4cd6b3a299514c87996d1794dd17b35ecb639d2eb91e230d"


    def __init__(self,nota:NotaCreditoVentas):
        self.nota = nota
    
    def crear_xml_nc(self):
        # Crear el elemento raíz <NOTA>

        detalle = DetalleNotaCreditoVentas.objects.filter(nota__numero = self.nota.numero)

        root = ET.Element("NOTA")

        # Añadir los atributos al elemento raíz
        root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")

        # Crear el elemento <ENC>
        enc = ET.SubElement(root, "ENC")

        enc_1 = ET.SubElement(enc, "ENC_1")
        enc_1.text = "NC"
        enc_2 = ET.SubElement(enc, "ENC_2")
        enc_2.text = "901648084"
        enc_3 = ET.SubElement(enc, "ENC_3")
        enc_3.text = str(self.nota.cliente.documento)
        enc_4 = ET.SubElement(enc, "ENC_4")
        enc_4.text = "UBL 2.1"
        enc_5 = ET.SubElement(enc, "ENC_5")
        enc_5.text = "DIAN 2.1"
        enc_6 = ET.SubElement(enc, "ENC_6")
        enc_6.text = self.nota.prefijo+str(self.nota.consecutivo)
        enc_7 = ET.SubElement(enc, "ENC_7")
        enc_7.text = self.nota.fecha.strftime("%Y-%m-%d")
        enc_8 = ET.SubElement(enc, "ENC_8")
        enc_8.text = "14:51:00-05:00"
        enc_9 = ET.SubElement(enc, "ENC_9")
        enc_9.text = "91"
        enc_10 = ET.SubElement(enc, "ENC_10")
        enc_10.text = "COP"
        enc_15 = ET.SubElement(enc, "ENC_15")
        enc_15.text = str(len(detalle))
        enc_20 = ET.SubElement(enc, "ENC_20")
        enc_20.text = "1"
        enc_21 = ET.SubElement(enc, "ENC_21")
        enc_21.text = "20"

        # Crear el elemento <EMI>
        emi = ET.SubElement(root, "EMI")
        emi_1 = ET.SubElement(emi, "EMI_1")
        emi_1.text = "1"
        emi_2 = ET.SubElement(emi, "EMI_2")
        emi_2.text = "901648084"
        emi_3 = ET.SubElement(emi, "EMI_3")
        emi_3.text = "31"
        emi_4 = ET.SubElement(emi, "EMI_4")
        emi_4.text = "48"
        emi_6 = ET.SubElement(emi, "EMI_6")
        emi_6.text = "SUMIPROD DE LA COSTA S.A.S."
        emi_7 = ET.SubElement(emi, "EMI_7")
        emi_7.text = "SUMIPROD DE LA COSTA S.A.S."
        emi_10 = ET.SubElement(emi, "EMI_10")
        emi_10.text = "Dirección: Calle 44B #21G-11 URB Santa Cruz"
        emi_11 = ET.SubElement(emi, "EMI_11")
        emi_11.text = "47"
        emi_13 = ET.SubElement(emi, "EMI_13")
        emi_13.text = "SANTA MARTA"
        emi_14 = ET.SubElement(emi, "EMI_14")
        emi_14.text = "470001"
        emi_15 = ET.SubElement(emi, "EMI_15")
        emi_15.text = "CO"
        emi_19 = ET.SubElement(emi, "EMI_19")
        emi_19.text = "Magdalena"
        emi_21 = ET.SubElement(emi, "EMI_21")
        emi_21.text = "Colombia"
        emi_22 = ET.SubElement(emi, "EMI_22")
        emi_22.text = "9"
        emi_23 = ET.SubElement(emi, "EMI_23")
        emi_23.text = "47001"
        emi_24 = ET.SubElement(emi, "EMI_24")
        emi_24.text = "SUMIPROD DE LA COSTA S.A.S."

        # Crear el elemento <TAC>
        tac = ET.SubElement(emi, "TAC")
        tac_1 = ET.SubElement(tac, "TAC_1")
        tac_1.text = "R-99-PN"

        # Crear el elemento <DFE>
        dfe = ET.SubElement(emi, "DFE")
        dfe_1 = ET.SubElement(dfe, "DFE_1")
        dfe_1.text = "47001"
        dfe_2 = ET.SubElement(dfe, "DFE_2")
        dfe_2.text = "47"
        dfe_3 = ET.SubElement(dfe, "DFE_3")
        dfe_3.text = "CO"
        dfe_4 = ET.SubElement(dfe, "DFE_4")
        dfe_4.text = "470001"
        dfe_5 = ET.SubElement(dfe, "DFE_5")
        dfe_5.text = "Colombia"
        dfe_6 = ET.SubElement(dfe, "DFE_6")
        dfe_6.text = "Magdalena"
        dfe_7 = ET.SubElement(dfe, "DFE_7")
        dfe_7.text = "SANTA MARTA"
        dfe_8 = ET.SubElement(dfe, "DFE_8")
        dfe_8.text = "Dirección: Calle 44B #21G-11 URB Santa Cruz"

        # Crear el elemento <ICC>
        icc = ET.SubElement(emi, "ICC")
        icc_1 = ET.SubElement(icc, "ICC_1")
        icc_1.text = "262150"
        icc_9 = ET.SubElement(icc, "ICC_9")
        icc_9.text = self.nota.prefijo

        # Crear el elemento <CDE>
        cde = ET.SubElement(emi, "CDE")
        cde_1 = ET.SubElement(cde, "CDE_1")
        cde_1.text = "1"
        cde_2 = ET.SubElement(cde, "CDE_2")
        cde_2.text = "Enrique de jesus rosado navarro"
        cde_3 = ET.SubElement(cde, "CDE_3")
        cde_3.text = "(5) 4327722-Cel: 3013022986"
        cde_4 = ET.SubElement(cde, "CDE_4")
        cde_4.text = "SUMIPRODELACOSTA@GMAIL.COM"

        # Crear el elemento <GTE>
        gte = ET.SubElement(emi, "GTE")
        gte_1 = ET.SubElement(gte, "GTE_1")
        gte_1.text = "01"
        gte_2 = ET.SubElement(gte, "GTE_2")
        gte_2.text = "IVA"

        # Crear el elemento <ADQ>
        adq = ET.SubElement(root, "ADQ")
        adq_1 = ET.SubElement(adq, "ADQ_1")
        adq_1.text = str(self.nota.cliente.tipoPersona)
        adq_2 = ET.SubElement(adq, "ADQ_2")
        adq_2.text = str(self.nota.cliente.documento)
        adq_3 = ET.SubElement(adq, "ADQ_3")
        if self.nota.cliente.tipoDocumento == 'NIT':
            adq_3.text='31'
        else:
            adq_3.text='13'
            
        # REGIMENN AL Q PERTENECE  
        # IMPUESTO SOBRE LA VENTADEL IVA
        # CAMPO OPCIONAL
        adq_4 = ET.SubElement(adq, "ADQ_4")
        if self.nota.cliente.regimen == 'Responsable del IVA':
       
            adq_4.text = "48"
        else:
            adq_4.text = "49"
        adq_6 = ET.SubElement(adq, "ADQ_6")
        adq_6.text = str(self.nota.cliente.nombreComercial)
        adq_7 = ET.SubElement(adq, "ADQ_7")
        adq_7.text = str(self.nota.cliente.nombreComercial)
        adq_10 = ET.SubElement(adq, "ADQ_10")
        adq_10.text = str(self.nota.cliente.direccion)
        adq_11 = ET.SubElement(adq, "ADQ_11")
        adq_11.text = str(self.nota.cliente.departamento.codigo.replace(".", ""))
        adq_13 = ET.SubElement(adq, "ADQ_13")
        adq_13.text = str(self.nota.cliente.municipio.municipio)
        adq_14 = ET.SubElement(adq, "ADQ_14")
        adq_14.text = str(self.nota.cliente.codigoPostal)
        adq_15 = ET.SubElement(adq, "ADQ_15")
        adq_15.text = "CO"
        adq_19 = ET.SubElement(adq, "ADQ_19")
        adq_19.text = str(self.nota.cliente.departamento.departamento)
        adq_21 = ET.SubElement(adq, "ADQ_21")
        adq_21.text = "Colombia"
        adq_22 = ET.SubElement(adq, "ADQ_22")
        adq_22.text = str(self.nota.cliente.dv)
        adq_23 = ET.SubElement(adq, "ADQ_23")
        adq_23.text =str(self.nota.cliente.municipio.codigo.replace(".", ""))
        adq_24 = ET.SubElement(adq, "ADQ_24")
        adq_24.text = "1"

        # Crear el elemento <TCR>
        tcr = ET.SubElement(adq, "TCR")
        tcr_1 = ET.SubElement(tcr, "TCR_1")
        tcr_1.text = "R-99-PN"

        # Crear el elemento <ILA>
        ila = ET.SubElement(adq, "ILA")
        ila_1 = ET.SubElement(ila, "ILA_1")
        ila_1.text =str(self.nota.cliente.nombreComercial)
        ila_2 = ET.SubElement(ila, "ILA_2")
        ila_2.text = str(self.nota.cliente.nombreComercial)
        ila_3 = ET.SubElement(ila, "ILA_3")

        if self.nota.cliente.tipoDocumento == 'NIT':
            ila_3.text = "31"
        else:
            ila_3.text='13'
        ila_4 = ET.SubElement(ila, "ILA_4")
        ila_4.text = str(self.nota.cliente.dv)

        # Crear el elemento <DFA>
        DFA   = ET.SubElement(adq,'DFA')
        # CODIGO INDICADOR DEL PAIS CO
        DFA_1 = ET.SubElement(DFA,'DFA_1').text='CO'
        # CODIGO DEL DEPARTAMENTO DEL CLIENTE
        DFA_2 = ET.SubElement(DFA,'DFA_2').text=str(self.nota.cliente.departamento.codigo.replace(".", ""))
        # CODIGO POSTAL
        DFA_3 = ET.SubElement(DFA,'DFA_3').text=str(self.nota.cliente.codigoPostal)
        # CODIGO DEL MUNICIPIO
        DFA_4 = ET.SubElement(DFA,'DFA_4').text=str(self.nota.cliente.municipio.codigo.replace(".", ""))
        # NOMBRE DEL PAIS DEL CIENTE Colombia
        DFA_5 = ET.SubElement(DFA,'DFA_5').text='Colombia'
        # NOMBRE DEL DEPARTAMENTO DEL CIENTE
        DFA_6 = ET.SubElement(DFA,'DFA_6').text=str(self.nota.cliente.departamento.departamento)
        # NOMBRE DE LA CIUDAD DEL CIENTE
        DFA_7 = ET.SubElement(DFA,'DFA_7').text=str(self.nota.cliente.municipio.municipio)
        # DIRECCION DEL CLIENTE TEXTO LIBRE
        DFA_8 = ET.SubElement(DFA,'DFA_8').text=str(self.nota.cliente.direccion)

        # Crear el elemento <ICR>
        if self.nota.cliente.tipoPersona == 1:
            ICR   = ET.SubElement(adq,'ICR')
            #NUMERO DE MATRICULA MERCANTIL SI ADQ_1 ES 1                    
            #184312 ES DE LEYZA DEBE SER DEL CLIENTE SI ADQ ES 1
            ICR_1 = ET.SubElement(ICR,'ICR_1').text=str(self.nota.cliente.matriculaMercantil)
        
        CDA   = ET.SubElement(adq,'CDA')
        #TIPO DE CONTACTO DEL ADQUIRIENTE ESCOJO 1
        CDA_1 = ET.SubElement(CDA,'CDA_1').text='1'
        # NOMBRE DE LA PERSONA DE CONTACTO
        CDA_2 = ET.SubElement(CDA,'CDA_2').text=str(self.nota.cliente.nombreContacto)
        # TELEFONO DE LA PERSONA DE CONTACTO
        CDA_3 = ET.SubElement(CDA,'CDA_3').text=str(self.nota.cliente.telefonoContacto)
        #CORREO DE CONTACTO DE QUIEN VA A RECIBIR LA FACTURA
        CDA_4 = ET.SubElement(CDA,'CDA_4').text=str(self.nota.cliente.correoFacturas)
        
        # Crear el elemento <GTA>
        gta = ET.SubElement(adq, "GTA")
        gta_1 = ET.SubElement(gta, "GTA_1")
        gta_1.text = "01"
        gta_2 = ET.SubElement(gta, "GTA_2")
        gta_2.text = "IVA"

        # Crear el elemento <TOT>
        TOT   = ET.SubElement(root,'TOT')
        # VALOR BRUTO O SUBTOTAL DE LA FACTURA 
        TOT_1 = ET.SubElement(TOT,'TOT_1').text=str(self.nota.subtotal)
        # MONEDA USADA
        TOT_2 = ET.SubElement(TOT,'TOT_2').text='COP'
        if self.nota.iva > 0:
        # BASES IMPONIBLES PARA CALCULAR LOS TRIBUTOS OSEA EL SUBTOTAL QUE SE LE APLICA EL IVA Y LA RETEFUENTE ETC...
            TOT_3 = ET.SubElement(TOT,'TOT_3').text=str(self.nota.iva / 0.19)
        else:
            TOT_3 = ET.SubElement(TOT,'TOT_3').text=str(0)
        # MONESDA USADA
        TOT_4 = ET.SubElement(TOT,'TOT_4').text='COP'
        # VALOR TOTAL DE LA FACTURA
        TOT_5 = ET.SubElement(TOT,'TOT_5').text=str(self.nota.total+self.nota.retencion)
        # MONESDA USADA
        TOT_6 = ET.SubElement(TOT,'TOT_6').text='COP'
        #VALOR TOTAL DE LA FACTURA
        TOT_7 = ET.SubElement(TOT,'TOT_7').text=str(self.nota.total+self.nota.retencion)
        # MONEDA USADA
        TOT_8 = ET.SubElement(TOT,'TOT_8').text='COP'


        # SI EL IVA  ES 0 ENTONCES TIM NO APLICA 
        if self.nota.iva > 0:
            print("el valor del iva entro")

            
            print("impuesto")
            TIM   = ET.SubElement(root,'TIM')

            # true o false si somos autoretenedores
            TIM_1 = ET.SubElement(TIM,'TIM_1').text='false'
            # VALOR DEL IVA
            TIM_2 = ET.SubElement(TIM,'TIM_2').text=str(self.nota.iva)
            # MONEDA LOCAL
            TIM_3 = ET.SubElement(TIM,'TIM_3').text='COP'

            IMP   = ET.SubElement(TIM,'IMP')
            # 01 ES EL IDENTIFICADOR DEL TRIBUTO IVA
            IMP_1 = ET.SubElement(IMP,'IMP_1').text='01'

            # BASE IMPONIBLE PARA CALCULAR EL TRIBUTO
            IMP_2 = ET.SubElement(IMP,'IMP_2').text=str(self.nota.iva / 0.19)

            # MONEDA LOCAL ES COP
            IMP_3 = ET.SubElement(IMP,'IMP_3').text='COP'

            # VALOR DEL TRIBUTO IVA IMP_4 * IMP_6
            IMP_4 = ET.SubElement(IMP,'IMP_4').text=str(self.nota.iva)

            # MONEDA LOCAL ES COP
            IMP_5 = ET.SubElement(IMP,'IMP_5').text='COP'

            # porcentaje del iva
            IMP_6 = ET.SubElement(IMP,'IMP_6').text="19.00"







        # Crear el elemento <DRF>
        DRF   = ET.SubElement(root,'DRF')
        # NUMERO DE AUTORIZACION O RESOLUCION OTORGADO PARA FAC ELECTRONICA
        DRF_1 = ET.SubElement(DRF,'DRF_1').text=str(self.nota.cxc.numeracion.resolucion)
        # FECHA DE INICIO DEL PERIODO DE RESOLUCION OTORGADO
        DRF_2 = ET.SubElement(DRF,'DRF_2').text=self.nota.cxc.numeracion.fecha_inicio.strftime("%Y-%m-%d")
        # FECHA DE FINAL DEL PERIODO DE RESOLUCION OTORGADO
        DRF_3 = ET.SubElement(DRF,'DRF_3').text=self.nota.cxc.numeracion.fecha_vencimiento.strftime("%Y-%m-%d")
        # PREFIJO DEL RANGO RESOLUCION OTORGADO
        DRF_4 = ET.SubElement(DRF,'DRF_4').text=str(self.nota.numeracion.prefijo)
        # RANGO DE NUMERACION MINIMO
        DRF_5 = ET.SubElement(DRF,'DRF_5').text=str(self.nota.numeracion.desde)
        # RANGO DE NUMERACION MAXIMO
        DRF_6 = ET.SubElement(DRF,'DRF_6').text=str(self.nota.numeracion.hasta)

        # Crear el elemento <NOTA>
        nota = ET.SubElement(root, "NOTA")
        nota_1 = ET.SubElement(nota, "NOTA_1")
        nota_1.text = self.nota.observacion





        # Crear el elemento <REF>
        ref = ET.SubElement(root, "REF")
        ref_1 = ET.SubElement(ref, "REF_1")
        ref_1.text = "IV"
        ref_2 = ET.SubElement(ref, "REF_2")
        ref_2.text = self.nota.cxc.prefijo+str(self.nota.cxc.consecutivo)
        ref_3 = ET.SubElement(ref, "REF_3")
        ref_3.text = self.nota.cxc.fecha.strftime("%Y-%m-%d")
        ref_4 = ET.SubElement(ref, "REF_4")
        ref_4.text = self.nota.cxc.cufe
        ref_5 = ET.SubElement(ref, "REF_5")
        ref_5.text = "CUFE-SHA384"

        index   = 0
        for x in detalle:
            print("entro a la lista detalle")
            index+=1

            ITE   = ET.SubElement(root,'ITE')
            # NUMERO EN ORDEN SECUENCIAL 1,2,3,4,5 ETC
            ITE_1 = ET.SubElement(ITE,'ITE_1').text=str(index)
            # CANTIDAD DEL PRODUCTO POR ITEM
            ITE_3 = ET.SubElement(ITE,'ITE_3').text=str(x.cantidad)
            # IDENTIFICACION DE LA MEDIDAD DE LA CANTIDAD  94 ES unidad
            ITE_4 = ET.SubElement(ITE,'ITE_4').text='94'
            # SUBTOTAL DE LA LINEA ITE_7 * ITE_27-(x.descuento*x.cantidad)
            ITE_5 = ET.SubElement(ITE,'ITE_5').text=str(x.subtotal)

            ITE_6 = ET.SubElement(ITE,'ITE_6').text='COP'
            # VALOR UNITARIO DEL PRODUCTO
            ITE_7 = ET.SubElement(ITE,'ITE_7').text=str(x.valorUnidad)
            # MONEDA
            ITE_8 = ET.SubElement(ITE,'ITE_8').text='COP'
            # NOMBRE DEL PRODUCTO
            ITE_11 = ET.SubElement(ITE,'ITE_11').text=x.producto.nombre
            # CODIGO DEL PRODCUTO OJO PUEDE SER ITE_18
            ITE_18 = ET.SubElement(ITE,'ITE_18').text=x.producto.codigoDeBarra
            # SUBTOTAL  - DESCUENTOS-(x.descuento*x.cantidad)
            ITE_19 = ET.SubElement(ITE,'ITE_19').text=str(x.subtotal)
            # MONEDA LOCAL
            ITE_20 = ET.SubElement(ITE,'ITE_20').text='COP'
            # SUBTOTAL CON IVA INCLUIDO-(x.descuento*x.cantidad)
            ITE_21 = ET.SubElement(ITE,'ITE_21').text=str(x.subtotal+(x.iva*x.cantidad))
            # MONEDA LOCAL
            ITE_22 = ET.SubElement(ITE,'ITE_22').text='COP'
            # CANTIDAD DEL PRODUCTO
            ITE_27 = ET.SubElement(ITE,'ITE_27').text=str(x.cantidad)
            # IDENTIFICACION DE LA MEDIDAD DE LA CANTIDAD  94 ES unidad
            ITE_28 = ET.SubElement(ITE,'ITE_28').text='94'


            IAE   = ET.SubElement(ITE,'IAE')
            # CODIGO DE BARRA
            IAE_1 = ET.SubElement(IAE,'IAE_1').text=x.producto.codigoDeBarra
            IAE_2 = ET.SubElement(IAE,'IAE_2').text='001'

           
            if x.iva > 0:
                TII  = ET.SubElement(ITE,'TII')
                # VALOR DEL IVA POR ITEM
                print('El inva')
                print(x.iva*x.cantidad)
                TII_1 = ET.SubElement(TII,'TII_1').text=str(x.iva*x.cantidad)
                # MODEDA LOCAL DE COLOMBIA
                TII_2 = ET.SubElement(TII,'TII_2').text='COP'
                # true para autoretenedores
                TII_3 = ET.SubElement(TII,'TII_3').text='false'

                IIM   = ET.SubElement(TII,'IIM')
                # CODIGO EQUIVALENTE AL IVA 
                IIM_1 = ET.SubElement(IIM,'IIM_1').text='01'
                # VALOR TOTAL DEL IVA POR ITEM 
                IIM_2 = ET.SubElement(IIM,'IIM_2').text=str(x.iva*x.cantidad)
                # MODEDA LOCAL DE COLOMBIA
                IIM_3 = ET.SubElement(IIM,'IIM_3').text='COP'
                # BASE IMPONIBLE SUBTOTAL-(x.descuento*x.cantidad)
                IIM_4 = ET.SubElement(IIM,'IIM_4').text=str(x.subtotal)
                # MODEDA LOCAL DE COLOMBIA
                IIM_5 = ET.SubElement(IIM,'IIM_5').text='COP'
                # PORCENTAJE DEL IVA APLICADO
                IIM_6 = ET.SubElement(IIM,'IIM_6').text="19.00"
            
           
       
        # Crear un árbol XML
        xml_string = ET.tostring(root, encoding="utf-8", method="xml")
        # ET.ElementTree(root).write(self.nota.prefijo+str(self.nota.consecutivo), encoding="utf-8", xml_declaration=True)

        # Convertir la cadena XML a base64
        base64_xml = base64.b64encode(xml_string).decode("utf-8")

        # Devolver la cadena base64
        return base64_xml



    def uploadInvoiceFile(self,xml:str):
        xmlbase = ""
        # with open("facturas/"+self.factura.numero+".xml", "rb") as file:
        #     encoded = base64.encodebytes(file.read()).decode("utf-8")
        #     xmlbase = encoded
        
        soap = f"""<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                            <soap:Body>
                                <uploadInvoiceFile xmlns="http://webservice.facturatech.co/">
                                <username>{self.username}</username>
                                <password>{self.password}</password>
                                <xmlBase64>{xml}</xmlBase64>
                                </uploadInvoiceFile>
                            </soap:Body>
                    </soap:Envelope>"""
        return soap

    def documentStatusFile(self):
        soap = f"""<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                            <soap:Body>
                                <documentStatusFile xmlns="http://webservice.facturatech.co/">
                                    <username>{self.username}</username>
                                    <password>{self.password}</password>
                                    <transaccionID>{self.nota.transaccionID}</transaccionID>
                                </documentStatusFile>
                            </soap:Body>
                    </soap:Envelope>"""
        return soap

    def downloadPDFFile(self):
        soap = f"""<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                            <soap:Body>
                                <downloadPDFFile xmlns="http://webservice.facturatech.co/">
                                    <username>{self.username}</username>
                                    <password>{self.password}</password>
                                    <prefijo>{self.nota.prefijo}</prefijo>
                                    <folio>{self.nota.consecutivo}</folio>
                                </downloadPDFFile>
                            </soap:Body>
                    </soap:Envelope>"""
        return soap   