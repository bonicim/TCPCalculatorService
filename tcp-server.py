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
TIMEOUT = 2

def main():
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
                    print('\n', '*** NEW CONNECTION ***********************************', '\n')
                    print('SUCCESS! Server connected to: ', addr, ' at ', current_time())
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
    data = recv_data_v2(client_socket)
    print('SUCCESS! Server received: ', data)

    # Step 2: Process and send the received data
    do_biz_logic(data, client_socket)

    # Step 3: Close the client socket
    time.sleep(SLEEPYTIME)
    client_socket.close()


def recv_data_v2(conn):
    buf_counter = 1
    total_data = []

    count_total_expr = recv_two_byte_chunk(conn)
    print('Received very first chunk #', buf_counter, ': ', count_total_expr,'\n')
    total_data.append(count_total_expr)
    print('Total data received is: ', total_data, '\n')
    buf_counter += 1

    len_expr = recv_two_byte_chunk(conn)
    print('Received length of expr #', buf_counter, ': ', len_expr, '\n')
    total_data.append(len_expr)
    print('Total data received is: ', total_data, '\n')
    buf_counter += 1

    str_expr = recv_len_byte_chunk(conn, len_expr)
    print('Received string expr ', buf_counter, ': ', str_expr, '\n')
    total_data.append(str_expr)
    print('Total data received is: ', total_data, '\n')
    buf_counter += 1

    return total_data


def recv_len_byte_chunk(conn, length):
    data = ''
    for x in range(0, length):
        print('Reading byte number: ', x, '\n')
        chunk = conn.recv(1)
        unpacked = struct.unpack('!c', chunk)[0]
        unpacked = unpacked.decode('utf-8')
        print('Unpacked is: ', unpacked, '\n')
        data += unpacked
        print('The current unpacked chunk is: ', unpacked, '\n')

    print('The final unpacked chunk is: ', data, '\n')
    return data


def recv_two_byte_chunk(conn):
    chunk = conn.recv(2)  # returns a bytes object
    unpacked = struct.unpack('!h', chunk)[0]
    return unpacked


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
