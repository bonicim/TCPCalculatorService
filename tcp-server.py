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
SLEEPYTIME = 10
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

    try:
        # Step 1: Create TCP socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Step 2: Bind socket to IP and Port
        server_socket.bind((HOST_IP, HOST_PORT))

        # Step 3: Listen for incoming requests and store in backlog
        server_socket.listen(BACKLOG)
        print("SUCCESS! Server created and listening for requests...", "\n")

        # Step 4: Prepare requests for processing using select module
        inputs = [server_socket]

        # Step 5: Process each request
        while True:
            read_sockets, write_sockets, err_sockets = select.select(inputs, [], [])

            print('Connection List: ', read_sockets, '\n')
            for sock in read_sockets:
                if sock == server_socket:
                    client_socket, addr = sock.accept() # Creates CLIENT sockets
                    read_sockets.append(client_socket)
                    print('*** NEW CONNECTION ***********************************', '\n')
                    print('SUCCESS! Server connected to: ', addr, ' at ', current_time(), '\n')
                else:
                    _thread.start_new_thread(handler, (sock,))

        server_socket.close()

    except IOError as err:
        print("I/O error: {0}".format(err))
    except ValueError:
        print("Could not convert data to an integer.")


def handler(client_socket):
    """
    Processes a socket connection; performs simple calculations and returns results
    Does not wait for another request

    :param client_socket: socket object
    :return: calculation for a set of numbers
    """
    # Step 1: Receive all the data
    data = recv_data(client_socket)
    print()
    print('SUCCESS! Server received: ', data, '\n')

    # Step 2: Process and send the received data
    do_biz_logic(data, client_socket)
    # send the data

    # Step 3: Close the client socket
    time.sleep(SLEEPYTIME)
    client_socket.close()


def recv_data(client_socket):
    expr_counter = 1
    total_data = []
    print('******** RECEIVING data **************', '\n')

    # get the total number of expressions to read
    count_expr = recv_count_expr(client_socket)
    print('The number of expressions: ', count_expr)
    total_data.append(count_expr)

    # start the while loop
    while count_expr > 0:
        # get the size of the expression
        expr_size = recv_size_expr(client_socket)
        print('The size of expression is: ', expr_size)
        total_data.append(expr_size)

        # get the next expr_size bytes of the expression
        expr_str = recv_length_expr(client_socket, expr_size)
        print('The expression string is: ', expr_str)
        total_data.append(expr_str)

        # update expressions left to read
        count_expr -= 1

    return total_data


def recv_count_expr(client_socket):
    """
    Get the total number of expressions
    :param client_socket:
    :return:
    """
    count = client_socket.recv(MAX_EXPR_COUNT)
    return struct.unpack('!h', count)[0]


def recv_size_expr(client_socket):
    """
    Get the size of the incoming expression
    :param client_socket:
    :return:
    """
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
    return buf.decode('utf-8')


def current_time():
    return time.ctime(time.time())


def do_biz_logic(data, soc_obj):
    """
    Manipulates data and then returns a response
    :param data: a string of letters
    :param soc_obj: client socket
    :return: a string a of letters
    """

    count_expr = data[0]
    count_expr_packed = struct.pack('!h', count_expr)
    print('Sending number of expressions: ', count_expr,'\n')
    print('with byte size: ', count_expr_packed, '\n')
    soc_obj.sendall(count_expr_packed)

    count_expr = data[1]
    count_expr_packed = struct.pack('!h', count_expr)
    print('Sending length of expression: ', count_expr,'\n')
    print('with byte size: ', count_expr_packed, '\n')
    soc_obj.sendall(count_expr_packed)

    expr = data[2]
    expr = expr.encode('utf-8')
    count_expr_packed = struct.pack('!4s', expr)
    print('Sending expression: ', expr,'\n')
    print('with byte size: ', count_expr_packed, '\n')
    soc_obj.sendall(count_expr_packed)


if __name__ == "__main":
    main()

main()
