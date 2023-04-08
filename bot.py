import telebot
from pycep_correios import get_address_from_cep, WebService

CHAVE_API = "6161402251:AAGJhqRmN3xuUxIUFBfdH7rraa4NvTjtaWg"

bot = telebot.TeleBot(CHAVE_API)

def extract_arg(arg):
    return arg.split()[1:]

@bot.message_handler(commands=['cep'])
def yourCommand(mensagem):
    cep = extract_arg(mensagem.text)
    cep = str(cep[0])
    
    #vaidação se é numérico
    if(cep.isnumeric()):

        #requisição pycep_correios
        address = get_address_from_cep(cep, webservice=WebService.APICEP)
        
        #salvando campos em variáveis
        cep = 'CEP: ' + str(address['cep'])
        logradouro = 'Logradouro: ' + str(address['logradouro'])
        bairro = 'Bairro: ' + str(address['bairro'])
        cidade = 'Cidade: ' + str(address['cidade'])
        uf = 'UF: ' + str(address['uf'])
        complemento = 'Complemento: '+ str(address['complemento'])
        
        #concatenando o texto para exibir na mensagem
        texto = logradouro + '\n' + bairro + '\n' + cidade + '\n' + uf + '\n' + complemento

        #enviando mensagem
        bot.send_message(mensagem.chat.id,texto)
    
    #se não for numérico    
    else:
        #apresenta mensagem de que são apenas números
        bot.send_message(mensagem.chat.id, f"Digite apenas números")


def verificar(mensagem):
    return True

@bot.message_handler(func=verificar)
def responder(mensagem):
    texto = """
    Escolha uma opção para continuar (Clique no item):
     /cep - Pesquisa de CEP's
Responder qualquer outra coisa não vai funcionar, clique em uma das opções"""
    bot.reply_to(mensagem, texto)

bot.polling()