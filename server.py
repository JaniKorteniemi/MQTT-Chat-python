import socket
import threading

BYTES = 1024
PORT = 5050
SERVER = '192.168.1.2'
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'

SUBCRIBE_MESSAGE = "!s:"
PUBLISH_MESSAGE = "!p:"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)
server.listen()

clients_list = []
name_list = []
topics = {}

def send_msg(msg, cli):
    if (cli != "!XNO"):
        cut_msg = ""
        name = ""
        for n in name_list:
            #MSG: NAME: MESSAGE
            if n in msg.decode(FORMAT):
                name = n
                name_len = len(n)
                msg_len = len(msg)
                cut_msg = msg.decode(FORMAT)[name_len: msg_len]

        if SUBCRIBE_MESSAGE in cut_msg:
            print("[SUBCRIBE]") 

            m_len = len(cut_msg)
            sub_msg = cut_msg[3:m_len]
            sub = {name: cli}

            if sub_msg in topics:
                print("topic allredy exsist")
                if name in str(topics.get(sub_msg)):
                    print("user allredy exsist in topic")
                else:
                    print("user added to topic " + name)
                    temp = topics.get(sub_msg)
                    temp.append(sub)
            else:
                s = [sub]
                topics.update({sub_msg: s})
                print("[NEW TOPIC]: " + sub_msg)

        elif PUBLISH_MESSAGE in cut_msg:
            print("[PUBLISH]")

            for topic in topics:
                if name in str(topics.get(topic)):
                    for client in clients_list:
                        if str(client) in str(topics.get(topic)):
                            client.send(msg)
                else:
                    print("User not subcriped to this topic")
    else:
        for client in clients_list:
            client.send(msg)

def handel_client(client):
    while True:
        try:
            msg = client.recv(BYTES)
            pMsg = msg.decode(FORMAT)
            print(pMsg)
            send_msg(msg, client)
        except:
            index = clients_list.index(client)
            clients_list.remove(client)
            client.close()
            name = name_list[index]
            print("[Client] {} Disconnected".format(name))
            send_msg('[SERVER] {} left!'.format(name).encode(FORMAT), "!XNO")
            name_list.remove(name)
            break

def receive():
    print("[STARTING] Server is tarting...")
    while True:
        client, address = server.accept()
        print(f"[NEW CONNECTION] {address} connected.")

        client.send('!NEWX_USERX'.encode(FORMAT))
        name = client.recv(BYTES).decode(FORMAT)
        name_list.append(name)
        clients_list.append(client)

        print("[New Client] Name is {}".format(name))
        client.send('[SERVER] Connected to server!'.encode(FORMAT))
        send_msg("[SERVER] {} joined!".format(name).encode(FORMAT), "!XNO")

        thread = threading.Thread(target=handel_client, args=(client,))
        thread.start()

receive()

#topics{
#
#   topicName: [
#       {username1: Client1},
#       {username2: Client2}
#   ],
#
#   topicName2: [
#       {username2: Client2},
#       {username1: Client1},
#       {username3: Client3}
#   ],
#
#   topicName3: [
#       {username3: Client3}
#   ]
#
#}