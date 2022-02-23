from http import client
import socket
import threading

cliente_apelido = input('Escolha um apelido para voce: ')

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 3001))


def receive():
    while True:
        try:
            mensagem = cliente.recv(1024).decode('ascii')
            # Checando se é o apelido ou se é outra coisa
            if mensagem == 'NICK':
                cliente.send(cliente_apelido.encode('ascii'))
            else:
                print(mensagem)
        
        except:
            print('Ocorreu um erro')
            cliente.close()
            break


def escreve():
    while True:
        mensagem = f'{cliente_apelido}: {input("")}'
        cliente.send(mensagem.encode('ascii'))


recebe_thread = threading.Thread(target=receive)
recebe_thread.start()

escreve_thread = threading.Thread(target=escreve)
escreve_thread.start()