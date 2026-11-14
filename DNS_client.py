import socket
client_sock = socket.socket()

def send_data(client, data_len_byte, data):
    """
    sends data to the client with its length
    :param client: where to send
    :param data_len_byte: number of digits for the length
    :param data: the data to send
    :return: None
    """
    if type(data) == str:
        data = data.encode()

    try:
        client.sendall(str(len(data)).zfill(data_len_byte).encode())
        client.sendall(data)
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

ip_to_name ={
    "1.1.1.1": "youtube.com",
    "2.2.2.2": "dominos.com",
    "3.3.3.3": "google.com"
    }

try:
    client_sock.connect(("127.0.0.1",53))
except Exception as e:
    print("error didnt connect to server " + str(e))
    client_sock.close()
    exit("The server is down")

while True:
    inp_user = input("press 1 to translate ip into name\npress 2 to translate nome into ip\npress 3 to exit program\n")
    if inp_user =="1":
        inp_user = input("enter the ip you want to translate")
        if inp_user in ip_to_name:
            print(ip_to_name[inp_user])
        else:
            print("information not available locally")
            try:
                send_data(client_sock, 4, inp_user)
                data = recv_data(client_sock, 4)
                if data is None:
                    break
                answer = data.decode()
                print(answer)
            except Exception as e:
                print("communication error: " + str(e))
                break

            if answer != "not found in central server":
                ip_to_name[inp_user] = answer

    elif inp_user =="2":
        inp_user = input("enter the name you want to translate")
        # searches for the name for the ip in ip_to_name
        found = False
        for ip, name in ip_to_name.items():
            if name == inp_user:
                print(ip)
                found = True
                break
        if not found:
            print("information not available locally")
            try:
                send_data(client_sock, 4, inp_user)
                data = recv_data(client_sock, 4)
                if data is None:
                    break
                answer = data.decode()
                print(answer)
            except Exception as e:
                print("communication error: " + str(e))
                break
            if answer != "not found in central server":
                ip_to_name[answer] = inp_user

    elif inp_user =="3":
        break
    else:
        print("illegal input please try again")
client_sock.close()