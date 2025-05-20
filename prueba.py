import smtplib
from email.mime.text import MIMEText

# Detalles de la cuenta de Gmail
smtp_servidor = "smtp.gmail.com"
smtp_puerto = 465  # Puerto seguro SSL para Gmail
tu_correo_gmail = "darau2746@gmail.com"  # Reemplaza con tu dirección de Gmail
tu_contrasena_gmail = "urzm djun suek htmz"  # Reemplaza con tu contraseña de Gmail (ver paso 2 y 3)

# Detalles del correo electrónico
remitente_email = tu_correo_gmail
destinatario_email = "bineo5555@gmail.com"  # Reemplaza con una dirección de prueba
asunto_email = "Prueba de Notificación Gmail SMTP"
cuerpo_email = "Este es un correo electrónico de prueba enviado a través de Gmail SMTP."

mensaje = MIMEText(cuerpo_email)
mensaje['Subject'] = asunto_email
mensaje['From'] = remitente_email
mensaje['To'] = destinatario_email

try:
    with smtplib.SMTP_SSL(smtp_servidor, smtp_puerto) as servidor:
        servidor.login(tu_correo_gmail, tu_contrasena_gmail)
        servidor.sendmail(remitente_email, [destinatario_email], mensaje.as_string())
    print(f"Correo electrónico enviado exitosamente a {destinatario_email} a través de Gmail")
except smtplib.SMTPAuthenticationError as e:
    print(f"Error de autenticación SMTP (Gmail): {e}")
except smtplib.SMTPConnectError as e:
    print(f"Error al conectar al servidor SMTP de Gmail: {e}")
except Exception as e:
    print(f"Ocurrió un error: {e}")