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
    print('\n', '*** WE ARE CONNECTED TO THE TCP SERVER *************************', '\n')
    print('\n', 'SUCCESS! Connected to host server: ', HOST_NAME, '\n')

    # Step 3: Send a message to the TCP server via the socket object
    send_and_receive(tcp_soc_obj)

    # Step 4: Close the socket object
    print('\n', '*** CLOSING CONNECTION TO SERVER **********************', '\n')
    tcp_soc_obj.close()


def send_and_receive(soc_obj):
    message = ['Sup Bitches!', 'Love, Tupac']
    counter = 1;
    for line in message:
        soc_obj.sendall(str.encode(line))
        data = soc_obj.recv(BUFSIZE)
        print(counter, 'SUCCESS! Received from server: ', data, '\n')
        counter += 1


if __name__ == "__main":
    main()

main()
