#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'
PORT = 4711

with socket.socket(socket.AF_INET, # address family: IPv4
                   socket.SOCK_STREAM # socket type: TCP
                   ) as s: # no need to call s.close()
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept() # blocking
    # addr: address of client, tuple (host, port)
    # conn: NEW socket object representing the connection (distinct from the listening socket that the server is using to accept new connections)
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024) # blocking, reads whatever data the client sends
            if not data:
                # If conn.recv() returns an empty bytes object, b'', that signals that the client closed the connection
                break
            conn.sendall(data)

#The .send() method behaves this way: It returns the number of bytes sent, which may be less than the size of the data passed in. You’re responsible for checking this and calling .send() as many times as needed to send all of the data. In the example above, you avoided having to do this by using .sendall()

#This is why you need to define an application-layer protocol. What’s an application-layer protocol? Put simply, your application will send and receive messages. The format of these messages are your application’s protocol.
#In other words, the length and format that you choose for these messages define the semantics and behavior of your application. This is directly related to what you learned in the previous paragraph regarding reading bytes from the socket. When you’re reading bytes with .recv(), you need to keep up with how many bytes were read, and figure out where the message boundaries are.
#How can you do this? One way is to always send fixed-length messages. If they’re always the same size, then it’s easy. When you’ve read that number of bytes into a buffer, then you know you have one complete message.
#However, using fixed-length messages is inefficient for small messages where you’d need to use padding to fill them out. Also, you’re still left with the problem of what to do about data that doesn’t fit into one message.
#In this tutorial, you’ll learn a generic approach, one that’s used by many protocols, including HTTP. You’ll prefix messages with a header that includes the content length as well as any other fields you need. By doing this, you’ll only need to keep up with the header. Once you’ve read the header, you can process it to determine the length of the message’s content. With the content length, you can then read that number of bytes to consume it.
