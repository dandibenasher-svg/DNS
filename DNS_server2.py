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
     recevs recevs the data we got and uses the length we got from send_data
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
    "8.8.8.8": "wordle.com",
    "9.9.9.9": "krillion.com",
}


big_server_soc = socket.socket()
try:
    big_server_soc.bind(("0.0.0.0", 54))  #531
    big_server_soc.listen(3)
except Exception as e:
    print("error starting server: " + str(e))
    big_server_soc.close()
    exit("The server couldn't start")
while True:
    try:
        client_sock, client_address = big_server_soc.accept()
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
            # searches for the name for the ip in ip_to_name
            if data in ip_to_name:
                send_data(client_sock, 4, ip_to_name[data])
            else:
                found = False
                for ip, name in ip_to_name.items():
                    if name == data:
                        send_data(client_sock, 4, ip)
                        found = True
                        break
                if not found:
                    send_data(client_sock, 4, "not found in central server")

        client_sock.close()
        print("closed the connection")
    except Exception as e:
        print("error accepting client: " + str(e))





