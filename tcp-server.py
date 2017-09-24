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
TIMEOUT = 2

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
        print("SUCCESS! Server created and listening for requests...", "\n")

        # Step 4: Prepare requests for processing using select module
        inputs = [tcp_soc_obj]

        # Step 5: Process each request
        while True:
            inready, outready, excready = select.select(inputs, [], [])

            for sock in inready:
                conn, addr = sock.accept()
                print('\n', '*** NEW CONNECTION ***********************************', '\n')
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
        data = recv_data(conn)
        print(' SUCCESS! Server received: ', data)
        print('From: ', addr)

        print('Sending to Client: ', do_biz_logic(data), '\n')
        conn.sendall(do_biz_logic(data))
        time.sleep(SLEEPYTIME)
        conn.close()


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


def current_time():
    return time.ctime(time.time())


def do_biz_logic(data):
    """
    Manipulates data and then returns a response
    :param data: a string of letters
    :return: a string a of letters
    """
    return data

    # Step 1: declare and initialize the response in the same form as the request
    # first two bytes=number of answers; second two bytes=length of answer;next X bytes is the string rep of the answer

    # Step 2: Get the first two bytes and determine number of expressions to evaluate

    # Step 3: Establish a location marker of current pos in the byte struct


if __name__ == "__main":
    main()

main()
