import socket

def send_data(address, len_data, data):
    """
    sends data to the client after sending length
    :param address: where to send
    :param len_data: amount of digits which is length
    :param data: the data to send
    :return: None
    """
    if type(data) == str:
        data = data.encode()
    try:
        address.sendall(str(len(data)).zfill(len_data).encode())
        address.sendall(data)
    except Exception as e:
        print("error in send try again " + str(e))



def recv_data(client, data_len):
    """
     recevs the data we got and uses the length we got from send_data
    :param client: where to send
    :param len_data: amount of digits which is length
    :return: data
    """
    try:
        length = client.recv(data_len)
        length = int(length.decode())

        data = client.recv(length)
        return data

    except Exception as e:
        print("error in recv try again " + str(e))
        return None

ip_to_name = {
    "1.1.1.1": "youtube.com",
    "2.2.2.2": "dominos.com",
    "3.3.3.3": "google.com",
    "5.5.5.5": "football.com",
    "6.6.6.6": "basketball.com",
    "7.7.7.7": "masterchef.com",
}

central_sock = socket.socket()
try:
    central_sock.connect(("127.0.0.1", 54))
except Exception as e:
    print("error starting server: " + str(e))
    central_sock.close()
    exit("The server couldn't start")

server_soc = socket.socket()
try:
    server_soc.bind(("0.0.0.0", 53))  #531
    server_soc.listen(3)
except Exception as e:
    print("error starting server: " + str(e))
    server_soc.close()
    exit("The server couldn't start")
while True:
    try:
        client_sock, client_address = server_soc.accept()
        print(f"{client_address[0]} - connected")
        while True:
            try:
                data = recv_data(client_sock, 4)
                if data is None:
                    break
                data = data.decode()
            except Exception as e:
                print("error receiving data: " + str(e))
                break
            if not data:
                break
            try:
                if data in ip_to_name:
                    send_data(client_sock, 4, ip_to_name[data])
                else:
                    # searches for the name for the ip in ip_to_name
                    found = False
                    for ip, name in ip_to_name.items():
                        if name == data:
                            send_data(client_sock, 4, ip)
                            found = True
                            break

                    #if ip or name wasnt found in server number one we check if its in the central server
                    if not found:
                         try:
                            send_data(central_sock, 4, data)
                            answer = recv_data(central_sock, 4)

                            if answer is None:
                                break
                            answer = answer.decode()
                            #if answer wasnt found in the central server
                            if answer == "not found in central server":
                                send_data(client_sock, 4, answer)
                            else:
                                is_ip = data.count(".") == 3 #when updating server number one we need to check if what we got was an ip or name
                                if is_ip:
                                    ip_to_name[data] = answer  #if its an ip we insert the name
                                else:
                                    ip_to_name[answer] = data #if its a name we insert the ip

                                send_data(client_sock, 4, answer)
                         except Exception as e:
                            print("communication error: " + str(e))
                            break

            except Exception as e:
                print("error sending response: " + str(e))
                break
        client_sock.close()
        print("closed the connection")
    except Exception as e:
        print("error accepting client: " + str(e))

