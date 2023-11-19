import socket
import datetime
import random
import logging
import os

IP = '0.0.0.0'
PORT = 8820
QUEUE_LEN = 1

LOG_FORMAT = '%(levelname)s | %(asctime)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/lucky.log'

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def protocol_send(what_to_send):
    """
    gets my message
    :return the message combined with my protocol
    """
    my_len = len(what_to_send)
    final = str(my_len) + '$' + what_to_send
    logging.debug(final)
    return final


def protocol_receive(client_socket):
    """
    gets a message combined with the protocol
    :return: my message seprated from my protocol
    """
    char = ''
    resived_len = ''
    while char != '$':
        char = client_socket.recv(1).decode()
        resived_len += char
    resived_len = resived_len[:-1]
    logging.debug(resived_len)
    return client_socket.recv(int(resived_len)).decode()


def TIME():
    """
    :return: the current time in str
    """
    return datetime.datetime.now().strftime("%H:%M:%S")


def NAME():
    """
    :return: the name of my server
    """
    return 'iftach sever'


def RAND():
    """
    :return: a random number between 1 and 10
    """
    temp = random.randint(1, 10)
    return str(temp)


def what_to_ret(client_socket):
    """
    :param client_socket:
    :return: 4 answers according to the request
    """
    while 1:
        try:
            request = protocol_receive(client_socket)
            logging.info('server received ' + request)
            if request == 'TIME':
                client_socket.send(protocol_send(TIME()).encode())

            elif request == 'NAME':
                client_socket.send(protocol_send(NAME()).encode())

            elif request == 'RAND':
                client_socket.send(protocol_send(RAND()).encode())

            elif request == 'EXIT':
                client_socket.close()
                return
        except socket.error as err:
            print('received socket error on client socket' + str(err))
            logging.info('received socket error on client socket' + str(err))
            return


def main():
    try:
        logging.debug(IP)
        logging.debug(PORT)
        logging.debug(QUEUE_LEN)
        my_socket.bind((IP, PORT))
        my_socket.listen(QUEUE_LEN)

        while 1:
            client_socket, client_address = my_socket.accept()

            what_to_ret(client_socket)

    except socket.error as err:

        print('received socket error on server socket' + str(err))
        logging.info('received socket error on client socket' + str(err))

    finally:
        my_socket.close()


if __name__ == '__main__':
    assert TIME() == datetime.datetime.now().strftime("%H:%M:%S")
    assert NAME() == 'iftach sever'
    assert 1 <= int(RAND()) <= 10
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)
    main()
