import socket

# TCP Client that connects to the local machine's TCP server

# constants
BUFSIZE = 16
HOST_NAME = socket.gethostname()
HOST_IP = socket.gethostbyname(HOST_NAME)
HOST_PORT = 8888


def main():
    """
    Creates a TCP client and performs a defined action on its behalf.
    :return: response from the server
    """

    # Step 1: Create a TCP socket object
    tcp_soc_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Step 2: Connect to the TCP server
    tcp_soc_obj.connect((HOST_NAME, HOST_PORT))
    print('SUCCESS! Connected to host server: ', HOST_NAME)

    # Step 3: Send a message to the TCP server via the socket object
    message = ['Sup Bitches!', 'Love, Tupac']
    for line in message:
        tcp_soc_obj.sendall(str.encode(line))
        data = tcp_soc_obj.recv(BUFSIZE)
        print('SUCCESS! Received from server: ', data)

    # Step 4: Close the socket object
    tcp_soc_obj.close()


if __name__ == "__main":
    main()

main()
