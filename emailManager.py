import win32com.client as win32
import os

class EmailManager:
    """
    Manejador para enviar correos electrónicos utilizando Outlook.

    Attributes:
        ruta_archivo_html (str): Ruta al archivo HTML de plantilla.
        contenido_html_base (str): Contenido del archivo HTML leído.
    """
    def __init__(self, ruta_archivo_html):
        """
        Inicializa la clase con la ruta del archivo HTML de plantilla.

        Args:
            ruta_archivo_html (str): Ruta al archivo HTML de plantilla.

        Raises:
            FileNotFoundError: Si el archivo HTML no se encuentra.
        """
        self.ruta_archivo_html = ruta_archivo_html
        self.contenido_html_base = self.leer_contenido_archivo()

    def leer_contenido_archivo(self):
        """
        Lee el contenido del archivo HTML especificado.

        Returns:
            str: Contenido del archivo HTML.

        Raises:
            FileNotFoundError: Si el archivo HTML no se encuentra.
        """
        try:
            with open(self.ruta_archivo_html, 'r', encoding='utf-8') as archivo:
                return archivo.read()
        except FileNotFoundError:
            print(f"El archivo {self.ruta_archivo_html} no se encuentra.")
            raise

    def enviar_correo(self, destinatario, asunto, contenido_html, archivo_adjunto):
        """
        Envía un correo electrónico utilizando Outlook.

        Args:
            destinatario (str): Dirección de correo electrónico del destinatario.
            asunto (str): Asunto del correo electrónico.
            contenido_html (str): Contenido en formato HTML del correo electrónico.
            archivo_adjunto (str): Ruta al archivo que se desea adjuntar.

        Raises:
            Exception: Si ocurre un error al enviar el correo electrónico.
        """
        try:
            outlook = win32.Dispatch('outlook.application')
            mail = outlook.CreateItem(0)
            mail.To = destinatario
            mail.Subject = asunto
            mail.Attachments.Add(archivo_adjunto)
            mail.Body = 'Este es un mensaje en formato HTML. Si no ves el contenido correctamente, usa un cliente de correo que soporte HTML.'
            mail.HTMLBody = contenido_html
            mail.Send()
            print(f"Correo enviado a {destinatario}.")
        except Exception as e:
            print(f"Error al enviar el correo electrónico: {e}")
            raise

    def enviar_correos(self, df_facturacion_comercios):
        """
        Itera sobre el DataFrame y envía correos electrónicos personalizados para cada registro.

        Args:
            df_facturacion_comercios (pd.DataFrame): DataFrame con la información para enviar correos.

        Raises:
            Exception: Si ocurre un error al enviar algún correo electrónico.
        """
        for index, row in df_facturacion_comercios.iterrows():
            correo_destino = f"{row['commerce_email']}" # Ajusta el destinatario según sea necesario

            # Construir la ruta del archivo adjunto
            ruta_relativa = f"./recursos/reportes/{row['commerce_nit']}.zip"  # Ajusta la extensión según el tipo de archivo
            archivo_adjunto = os.path.abspath(ruta_relativa)

            # Personalizar el contenido del correo
            contenido_html = self.contenido_html_base.replace('[id_facturacion]', row['id_facturacion']) \
                                                    .replace('[fecha_facturacion]', row['fecha_facturacion']) \
                                                    .replace('[NOMBRE_DEL_CLIENTE]', row['commerce_name']) \
                                                    .replace('[PERIODO]', 'Últimos 2 Meses') \
                                                    .replace('[VALOR_COMISIONES]', f"{row['comi_con_descuento']}") \
                                                    .replace('[VALOR_IVA]', f"{row['valor_cobrado_por_iva']}") \
                                                    .replace('[TOTAL_FACTURADO]', f"{row['total_facturado']}")

            # Enviar el correo
            self.enviar_correo(correo_destino, 'Factura de Cobro de Comisiones', contenido_html, archivo_adjunto)
