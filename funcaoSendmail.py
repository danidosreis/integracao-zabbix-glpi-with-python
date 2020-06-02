import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(chamado, cliente, alerta, hostname):

	# Informações do Servidor SMTP e autenticaçao
	smtp_ssl_host = 'outlook.office365.com'
	smtp_ssl_port = 587
	username = 'email@dominio.com.br'
	password = 'senha'

	# De, Para, Assunto
	from_addr = 'email@dominio.com.br'
	to_addrs = ['grupo@dominio.com.br']
	assunto = f'{cliente} | {alerta} [ASGS #{chamado}] '

	# Informações que completarão o template
	dic_template = {
			'CLIENTE': cliente,
			'ALERTA': alerta,
			'HOSTNAME': hostname
		}

	# Abre template de e-mail e insere as informações de usuario e senha
	with open('template-notificacao.html', 'r') as file:
		arquivo = file.read()
		body_message = arquivo.format(**dic_template)
	mail_content = body_message

	# E-mail
	message = MIMEMultipart()
	message['from'] = from_addr
	message['to'] = ', '.join(to_addrs)
	message['Subject'] = assunto
	message.attach(MIMEText(mail_content, 'html'))

	# Conexão com o smtp e envio do e-mail
	print('1. Conectando ao SMTP...')
	server = smtplib.SMTP(smtp_ssl_host, smtp_ssl_port)
	server.ehlo()
	server.starttls()
	server.login(username, password)
	server.sendmail(from_addr, to_addrs, message.as_string())
	server.quit()
