# Importando bibliotecas
import socket
import threading

# Definindo IP do host e o número da porta do servidor
host = '127.0.0.1' #localhost
port = 3001

# Preparando o servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Socket de internet, Adota TCP
server.bind((host, port)) # Travando a relação do IP e da porta
server.listen() # Servidor em modo de escuta - Aguardando conexão


clientes = []
clientes_apelidos = []

# Função para enviar mensagem para todos os clientes que estão conectados ao servidor
def mandaMensagemTodos(mensagem):
    for client in clientes:
        client.send(mensagem)


# Tratando mensagem do cliente (cliente único)
def processaMensagemCliente(cliente):
    while True:
        try:
            mensagem = cliente.recv(1024) # Quando receber uma mensagem, mandamos para todos os outros clientes
            mandaMensagemTodos(mensagem)
        except: # Em caso de erro
            # Se houver erro com o cliente, o loop vai acabar e o cliente será removido da lista
            index = clientes.index(cliente)
            clientes.remove(cliente)
            cliente.close()
            cliente_apelido = clientes_apelidos[index]
            mandaMensagemTodos(f'{cliente_apelido} saiu da conversa'.encode('ascii'))
            clientes_apelidos.remove(cliente_apelido)
            break

# Juntando as funções acima para criar o método receive
def receive():
    while True:
        # Permite a conexão
        # A função fica rodando constantemente e retorna um cliente e seu endereço quando alguém se conecta
        cliente, endereco = server.accept() 
        print(f'Conectado com str({endereco})')

        # Tratamento da conexão do cliente - Apelido, verifica e colocamos nos arrays dos conectados e dos apelidos
        cliente.send('Apelido'.encode('ascii'))
        cliente_apelido = cliente.recv(1024).decode('ascii')
        clientes_apelidos.append(cliente_apelido)
        clientes.append(cliente)

        print(f'Apelido = {cliente_apelido}')

        mandaMensagemTodos(f'{cliente_apelido} acabou de entrar na conversa'.encode('ascii'))

        #cliente.send('Conectado na conversa'.encode('ascii'))

        thread = threading.Thread(target=processaMensagemCliente, args=(cliente,))
        thread.start()

print('Server is listening...')
receive()