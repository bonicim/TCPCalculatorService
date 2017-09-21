import socket
import _thread
import time
import select

# Multithreaded TCP server that performs simple calculation

# Constants
BUFSIZE = 16
HOST_NAME = socket.gethostname()
HOST_IP = socket.gethostbyname(HOST_NAME)
HOST_PORT = 8888
BACKLOG = 10
SLEEPYTIME = 10

def main():
    """
    Creates and starts the TCP server

    Raises:
        Socket error if socket creation failed

    """

    try:
        # Step 1: Create TCP socket object
        tcp_soc_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Step 2: Bind socket to IP and Port
        tcp_soc_obj.bind((HOST_IP, HOST_PORT))

        # Step 3: Listen for incoming requests and store in backlog
        tcp_soc_obj.listen(BACKLOG)
        print("SUCCESS! Server created and listening for requests...")

        # Step 4: Prepare requests for processing using select module
        inputs = [tcp_soc_obj]

        # Step 5: Process each request
        while True:
            inready, outready, excready = select.select(inputs, [], [])

            for sock in inready:
                conn, addr = sock.accept()
                print('SUCCESS! Server connected to: ', addr, ' at ', current_time())
                _thread.start_new_thread(handler, (conn, addr))

        tcp_soc_obj.close()

    except IOError as err:
        print("I/O error: {0}".format(err))
    except ValueError:
        print("Could not convert data to an integer.")
    else:
        print('SUCCESS! Server created and running.')


def handler(conn, addr):
    """
    Processes a socket connection; performs simple calculations and returns results

    :param conn: socket object
    :param addr: address that is bound to the 'conn' socket object
    :return: calculation for a set of numbers
    """

    while True:
        # do some calc
        data = conn.recv(BUFSIZE)
        if not data: break

        print('SUCCESS! Server received: ', data, '\n')
        print('From: ', addr, '\n')

        reply = data.upper()
        print('Sending to Client: ', reply)
        conn.sendall(reply)
        time.sleep(SLEEPYTIME)

    conn.close()


def current_time():
    return time.ctime(time.time())


if __name__ == "__main":
    main()

main()
