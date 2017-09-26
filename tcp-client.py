import socket
import time
import struct

# TCP Client that connects to the local machine's TCP server

# constants
BUFSIZE = 16
HOST_NAME = socket.gethostname()
HOST_IP = socket.gethostbyname(HOST_NAME)
HOST_PORT = 8888
TIMEOUT = 2


def main():
    """
    Creates a TCP client and performs a defined action on its behalf.
    :return: response from the server
    """

    # Step 1: Create a TCP socket object
    tcp_soc_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Step 2: Connect to the TCP server
    tcp_soc_obj.connect((HOST_NAME, HOST_PORT))
    print('\n', '*** WE ARE CONNECTED TO THE TCP SERVER *************************', '\n')
    print('\n', 'SUCCESS! Connected to host server: ', HOST_NAME, '\n')

    # Step 3: Send a message to the TCP server via the socket object
    send(tcp_soc_obj)

    # Step 3a: Receive response
    recv_data_v2(tcp_soc_obj)

    # Step 4: Close the socket object
    print('\n', '*** CLOSING CONNECTION TO SERVER **********************', '\n')
    tcp_soc_obj.close()


def send(soc_obj):
    # message = '243+1261+12/343+12'
    # make string, encode string, pack string, send string

    count_expr = 2
    count_expr_packed = struct.pack('!h', count_expr)
    print('Sending number of expressions: ', count_expr,'\n')
    print('with byte size: ', count_expr_packed, '\n')
    soc_obj.sendall(count_expr_packed)

    count_expr = 4
    count_expr_packed = struct.pack('!h', count_expr)
    print('Sending length of expression: ', count_expr,'\n')
    print('with byte size: ', count_expr_packed, '\n')
    soc_obj.sendall(count_expr_packed)

    expr = b'3+12'
    count_expr_packed = struct.pack('!4s', expr)
    print('Sending expression: ', expr,'\n')
    print('with byte size: ', count_expr_packed, '\n')
    soc_obj.sendall(count_expr_packed)

    # print('Sending msg: ', message, '\n')
    # soc_obj.sendall(str.encode(message))  # encodes string into a bytes object


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


if __name__ == "__main":
    main()

main()
