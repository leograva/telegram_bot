import telebot
from pycep_correios import get_address_from_cep, WebService, exceptions

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

        try:#requisição pycep_correios
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
        except exceptions.InvalidCEP as eic:
            bot.send_message(mensagem.chat.id,'O cep digitado é inválido')

        except exceptions.CEPNotFound as ecnf:
            bot.send_message(mensagem.chat.id,'O CEP digitado não foi encontrado')

        except exceptions.ConnectionError as errc:
            bot.send_message(mensagem.chat.id,'Erro de conexão')

        except exceptions.Timeout as errt:
            bot.send_message(mensagem.chat.id,'Erro de timeout')

        except exceptions.HTTPError as errh:
            bot.send_message(mensagem.chat.id,'Erro HTTP')

        except exceptions.BaseException as e:
            bot.send_message(mensagem.chat.id,'Erro')

    
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
     /cep - Para pesquisar CEP's digite /cep cep_a_consultar
Responder qualquer outra coisa não vai funcionar, clique em uma das opções"""
    bot.reply_to(mensagem, texto)

bot.polling()