import socket
import _thread
import time
import select
import struct

# Multithreaded TCP server that performs simple calculation

# Constants
BUFSIZE = 16
HOST_NAME = socket.gethostname()
HOST_IP = socket.gethostbyname(HOST_NAME)
HOST_PORT = 8888
BACKLOG = 10
SLEEPYTIME = 3
MAX_EXPR_COUNT = 2
MAX_EXPR_SIZE = 2
CODING = 'utf-8'
ANSWR_COUNT_FMT = '!h'

def main():
    startup_server_socket()


def startup_server_socket():
    """
    Creates client sockets. As the server socket, its only job is to create client sockets.
    The server socket does not receive and send data. That is the job of the thread handler.

    Raises:
        Socket error if socket creation failed
    """

    # Step 0: Opening msg
    greetings()

    try:
        # Step 1: Create server
        server_socket = create_and_start_server()
        print("SUCCESS! Server created at IP Address: ", HOST_IP, ' on port: ', HOST_PORT)
        print('Multi-threaded server listening for up to ', BACKLOG, ' connections.', "\n")
        print('Server listening........', '\n')

        # Step 2: Process each request
        process_requests(server_socket)

        # Step 3: Close socket if necessary
        server_socket.close()

    except IOError as err:
        print("I/O error: {0}".format(err))
    except ValueError:
        print("Could not convert data to an integer.")


def greetings():
    print('\n', '*** TCP SERVER FOR CALCULATOR SERVICE')
    print('\n', '*** STARTING SERVER (APPROX 3 SEC) *************************', '\n')
    time.sleep(SLEEPYTIME)


def create_and_start_server():
    # Create TCP socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST_IP, HOST_PORT))
    server_socket.listen(BACKLOG)
    return server_socket


def process_requests(server_socket):
    while True:
        read_sockets, write_sockets, err_sockets = select.select([server_socket], [], [])
        for sock in read_sockets:
            if sock == server_socket:
                client_socket, addr = sock.accept() # Creates CLIENT sockets
                read_sockets.append(client_socket)
                print('*** NEW CONNECTION ***********************************', '\n')
                print('SUCCESS! Server connected to: ', addr, ' at ', current_time(), '\n')
            else:
                _thread.start_new_thread(handler, (sock,))


def handler(client_socket):
    """
    Processes a socket connection; performs simple calculations and returns results
    Does not wait for another request

    :param client_socket: socket object
    :return: calculation for a set of numbers
    """
    # Step 1: Receive the full req
    req = recv_data(client_socket)  # returns an array of ints and strings
    print('REQUEST RECEIVED: ', req, '\n')

    # Step 2: Process and send the received data
    resp = evaluate_expr(req, client_socket)

    # Step 3: Send the response
    print('SENDING RESPONSE: ', resp)
    client_socket.sendall(resp)

    # Step 4: Close the client socket
    client_socket.close()


def recv_data(client_socket):
    total_data = []
    print('*** RECEIVING data ************************', '\n')

    # get the total number of expressions to read
    count_expr = recv_qty_expr(client_socket)
    print('Total expressions to be evaluated: ', count_expr, '\n')
    total_data.append(count_expr)

    # start the while loop
    while count_expr > 0:
        # get the size of the current expression
        print('Receiving expression #', count_expr)
        time.sleep(SLEEPYTIME)
        expr_size = recv_size_expr(client_socket)
        print('The size of expression is: ', expr_size)
        total_data.append(expr_size)

        # get the actual expression
        expr_str = recv_length_expr(client_socket, expr_size)
        print('Actual expression: ', expr_str, '\n')
        total_data.append(expr_str)

        count_expr -= 1
    return total_data


def recv_qty_expr(client_socket):
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


def current_time():
    return time.ctime(time.time())


def evaluate_expr(req, client_socket):
    """
    Manipulates data and then returns a response
    :param req: a string of letters
    :param client_socket: client socket
    :return: a string a of letters
    """
    print('*** EVALUATING EXPRESSIONS (APPROX 3 SEC) ******************')
    time.sleep(SLEEPYTIME)
    print('Original request: ', req, '\n')

    # create an accumulator for the string message to be sent
    resp = b''

    # get the first input and add it to response
    total_answers = req[0]
    print('Number of answers is: ', total_answers, '\n')
    resp += struct.pack(ANSWR_COUNT_FMT, total_answers)

    expr_index = 1
    while expr_index <= total_answers:
        print('Evaluating expression #', expr_index)
        expr_actual = req[expr_index * 2]
        print('The actual expression is: ', expr_actual)

        print('Doing calculation.....')

        print('Converting expression into RPN.....(approx 1 sec)')
        time.sleep(1)
        rpn_expr = convert_to_rpn(expr_actual)
        print('Original expr: ', expr_actual)
        print('RPN expr: ', rpn_expr)

        print('Evaluating the expression.....(1 sec')
        time.sleep(1)
        answer_str = eval_rpn_expr(rpn_expr)
        answer = convert_to_bytes(answer_str)  # answer must be a byte object
        print('Answer: ', answer_str)
        print('Answer in bytes: ', answer)

        length = len(answer)
        resp += length
        resp += answer
        expr_index += 1

    # resp needs to be a bytes object that is really big
    print('Generated response: ', resp)
    print('Original request', req, '\n')
    time.sleep(10)
    return resp


# TODO: Implement
def convert_to_rpn(expr):
    """
    Converts an infix expression (e.g. 2+2)
    into an RPN/postfix expression (e.g  22+)
    :param expr: string expression in infix
    :return: stri   ng rpn expression
    """
    return expr


def eval_rpn_expr(expr):
    """
    Evaluates the mathematical expression. Only operations allowed
    are +, -, *, /
    :param expr: string expression in rpn
    :return: string result
    """
    output = []
    length = len(expr)

    for index in range(length):
        if expr[index].isdigit():
            output.append(expr[index])
        else:
            if expr[index] == '+':
                arg1 = output.pop()
                arg2 = output.pop()
                res = int(arg1) + int(arg2)
                output.append(res)
            elif expr[index] == '*':
                arg1 = output.pop()
                arg2 = output.pop()
                res = int(arg1) * int(arg2)
                output.append(res)
            elif expr[index] == '-':
                arg1 = output.pop()
                arg2 = output.pop()
                res = int(arg2) - int(arg1)
                output.append(res)
            elif expr[index] == '/':
                arg1 = output.pop()
                arg2 = output.pop()
                res = int(arg2) // int(arg1)
                output.append(res)
            else:
                print('Illegal operator: ', expr[index])
    return output[0]


# TODO: Implement
def convert_to_bytes(expr):
    """
    Convert a string into a bytes object
    :param expr: string
    :return:
    """
    return expr


if __name__ == "__main":
    main()

main()
