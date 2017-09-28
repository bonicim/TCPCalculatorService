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
    req = recv_data(client_socket)
    print('REQUEST RECEIVED: ', req, '\n')

    # Step 2: Process and send the received data
    resp = evaluate_expr(req, client_socket)

    # Step 3: Send the response
    send_response(resp, client_socket)

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
    resp = ''

    # TODO: Do business logic

    # count_expr = req[0]
    # count_expr_packed = struct.pack('!h', count_expr)
    # print('Sending number of expressions: ', count_expr,'\n')
    # print('with byte size: ', count_expr_packed, '\n')
    # client_socket.sendall(count_expr_packed)
    #
    # count_expr = req[1]
    # count_expr_packed = struct.pack('!h', count_expr)
    # print('Sending length of expression: ', count_expr,'\n')
    # print('with byte size: ', count_expr_packed, '\n')
    # client_socket.sendall(count_expr_packed)
    #
    # expr = req[2]
    # expr = expr.encode('utf-8')
    # count_expr_packed = struct.pack('!4s', expr)
    # print('Sending expression: ', expr,'\n')
    # print('with byte size: ', count_expr_packed, '\n')
    # client_socket.sendall(count_expr_packed)

    return resp

def send_response(resp, client_socket):
    # TODO: Write business logic
    client_socket.sendall(resp)


if __name__ == "__main":
    main()

main()
