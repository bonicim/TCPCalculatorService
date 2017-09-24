import socket
import time

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
    send_and_receive(tcp_soc_obj)

    # Step 4: Close the socket object
    print('\n', '*** CLOSING CONNECTION TO SERVER **********************', '\n')
    tcp_soc_obj.close()


def send_and_receive(soc_obj):
    message = '243+1261+12/343+12'
    print('Sending msg: ', message, '\n')
    soc_obj.sendall(str.encode(message))  # encodes string into a bytes object
    data = soc_obj.recv(4096)
    print('SUCCESS! Received from server: ', data, '\n')


def recv_data(conn):
    # conn.setblocking(0)
    conn.settimeout(5)
    buf_counter = 1
    data = bytearray()
    begin = time.time()
    while True:
        if data and time.time() - begin > TIMEOUT:
            print("we got all the data; time to process it.", '\n')
            break
        elif time.time() - begin > TIMEOUT + 2:
            print("client didn't send shit; get out", '\n')
            break
        # with data, break after X seconds
        # with no data, break after X seconds
        try:
            print('Receiving chunk # ', buf_counter)
            chunk = conn.recv(BUFSIZE)
            if chunk:
                data.extend(chunk)
                print('Received chunk #', buf_counter, ': ', chunk, '\n')
                print('extended msg is now: ', data, '\n')
                buf_counter += 1
                begin = time.time()
            else:
                time.sleep(5)
        except (socket.timeout, socket.error, Exception) as e:
            print(str(e))
            return data


if __name__ == "__main":
    main()

main()
