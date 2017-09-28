import socket
import time
import struct

# TCP Client that connects to the local machine's TCP server

# constants
BUFSIZE = 16
HOST_NAME = socket.gethostname()
HOST_IP = socket.gethostbyname(HOST_NAME)
HOST_PORT = 8888
SLEEPYTIME = 3
EXPR_COUNT_FMT = '!h'
EXPR_SIZE_FMT = '!h'
MAX_EXPR_COUNT = 2
MAX_EXPR_SIZE = 2
CODING = 'utf-8'


def main():
    create_client_socket()


def create_client_socket():
    """
    Creates a TCP client and performs a defined action on its behalf.
    :return: response from the server
    """
    # Step 0: Opening message
    greetings()

    # Step 1: Create a TCP socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Step 2: Connect to the TCP server
    client_socket.connect((HOST_NAME, HOST_PORT))
    print('SUCCESS! Connected to host server: ', HOST_NAME, 'at IP Address: ',
          HOST_IP, ' on port ', HOST_PORT, '\n')

    # Step 3: Get total number of expressions
    req_final = get_expression_qty()

    # Step 4: Get all the expressions
    req_final = get_expressions_actual(req_final)

    # Step 5: Send final message to the TCP server
    print('SENDING REQUEST (APPROX 3 SEC):  ', req_final, '\n')
    time.sleep(SLEEPYTIME)
    client_socket.sendall(req_final)

    # Step 6: Receive response
    resp = recv_resp(client_socket)
    print('RECEIVED RESPONSE: ', resp, '\n')
    print('ORIGINAL REQUEST: ', req_final, '\n')

    # Step 7: Close the socket
    print('*** CLOSING CONNECTION TO SERVER **********************', '\n')
    client_socket.close()


def greetings():
    print('\n', '*** TCP CLIENT FOR CALCULATOR SERVICE')
    print('\n', '*** CONNECTING TO THE TCP SERVER (APPROX 3 SEC) *************************', '\n')
    time.sleep(SLEEPYTIME)


def get_expression_qty(msg_final=b''):
    print('Welcome to Mark\'s Calculator Service', '\n')
    print('How many expressions do you need calculated?')
    print('(Enter a number between 0 and 65,536)')
    msg = input('==> ')
    print('You entered: ', msg, '\n')
    msg = int(msg)
    msg = struct.pack(EXPR_COUNT_FMT, msg)
    msg_final += msg
    return msg_final


def get_expressions_actual(msg_final):
    count = struct.unpack(EXPR_COUNT_FMT, msg_final)[0]
    while count > 0:
        print('Working on expression #: ', count)
        print('Enter the expression you want evaluated (e.g., 2+2*74/42): ')
        msg = input('==> ')
        print('You entered: ', msg, '\n')
        msg = msg.encode(CODING)
        length = len(msg)
        length = struct.pack(EXPR_SIZE_FMT, length)
        msg_final += length
        msg_final += msg
        count -= 1
    print('You have finished entering all the expressions.')
    return msg_final


def recv_resp(client_socket):
    total_data = []
    print('*** WAITING FOR RESPONSE ************************', '\n')

    # get the total number of expressions to read
    count_answers = recv_qty_answr(client_socket)
    print('Total answers: ', count_answers, '\n')
    total_data.append(count_answers)

    # start the while loop
    while count_answers > 0:
        # get the size of the current expression
        print('Receiving answer #', count_answers)
        time.sleep(SLEEPYTIME)
        expr_size = recv_size_expr(client_socket)
        print('The size of answer is: ', expr_size)
        total_data.append(expr_size)

        # get the actual expression
        expr_str = recv_length_expr(client_socket, expr_size)
        print('Actual answer: ', expr_str, '\n')
        total_data.append(expr_str)

        count_answers -= 1
    return total_data


def recv_qty_answr(client_socket):
    count = client_socket.recv(MAX_EXPR_COUNT)
    return struct.unpack('!h', count)[0]


def recv_size_expr(client_socket):
    size = client_socket.recv(MAX_EXPR_SIZE)
    return struct.unpack('!h', size)[0]


def recv_length_expr(client_socket, length):
    """
    Read exactly length bytes from client_socket
    Raise RuntimeError if the connection closed
    before length bytes were read

    * Note that socket is limited to read up to a max size of BUFSIZE
    :param client_socket:
    :param length:
    :return: a string decoded version of the received bytes object
    """
    buf = b''
    bytes_to_read = 0
    while length > 0:
        if length < BUFSIZE:
            bytes_to_read = length
        else:
            bytes_to_read = BUFSIZE

        chunk = client_socket.recv(bytes_to_read)
        if chunk == '':
            raise RuntimeError('unexpected connection close')

        buf += chunk
        length -= len(chunk)
    return buf.decode(CODING)


if __name__ == "__main":
    main()

main()
