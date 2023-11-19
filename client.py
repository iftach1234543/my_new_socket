"""
Author: iftach
program name: client.py
description: a client that is able to send messages to a server
Date: 19/11/23
"""


import socket
import logging
import os

IP = '127.0.0.1'

PORT = 8820

LOG_FORMAT = '%(levelname)s | %(asctime)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/lucky.log'


def protocol_send(what_to_send):
    """
    gets my message
    :return the message combined with my protocol
    """
    my_len = len(what_to_send)
    final = str(my_len) + '$' + what_to_send
    logging.debug(final)
    return final


def protocol_receive(my_socket):
    """
    gets a message combined with the protocol
    :return: my message seprated from my protocol
    """
    char = ''
    resived_len = ''
    while char != '$':
        char = my_socket.recv(1).decode()
        resived_len += char
    resived_len = resived_len[:-1]
    logging.debug(resived_len)
    return my_socket.recv(int(resived_len)).decode()


def is_legal_message(my_message):
    """

    :param my_message:
    :return: if my message is valid
    """
    return my_message == 'TIME' or my_message == 'NAME' or my_message == 'RAND' or my_message == 'EXIT'


def send_message(my_socket):
    """
    sends a message from the client to the server if the message is valid
    """
    while 1:
        what_to_send = input('What to send: ')
        logging.info(what_to_send)
        if is_legal_message(what_to_send):
            if what_to_send == 'TIME' or what_to_send == 'NAME' or what_to_send == 'RAND':
                my_socket.send(protocol_send(what_to_send).encode())
                print(protocol_receive(my_socket))

            elif what_to_send == 'EXIT':
                my_socket.send(protocol_send('EXIT').encode())
                print('you left the server')
                return
        else:
            print('Illegal message. Please choose between TIME / RAND / NAME / EXIT')


def main():
    logging.debug(IP)
    logging.debug(PORT)
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        my_socket.connect((IP, PORT))
        send_message(my_socket)

    except socket.error as err:
        print('received socket error ' + str(err))
        logging.error('received socket error on client socket' + str(err))

    my_socket.close()


if __name__ == '__main__':
    assert is_legal_message('TIME')
    assert is_legal_message('RAND')
    assert is_legal_message('NAME')
    assert is_legal_message('EXIT')
    assert not is_legal_message('')
    assert not is_legal_message('yoav')
    assert protocol_send('iftach') == '6$iftach'
    assert not protocol_send('yoav') == '7!yoav'
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)
    main()
