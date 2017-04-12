# -*- coding: cp936 -*-
from socket import *
import struct, os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

HOST = 'desktop.rty813.xyz'
PORT = 12345
BUFSIZE = 1024
ADDR = (HOST, PORT)

client = socket(AF_INET6, SOCK_STREAM)
client.connect(ADDR)

data = "capture"
client.send(data.encode('utf8'))
print 'Send Successful'
# conn,addr = client.accept()

BUFSIZE = 1024

FILEINFO_SIZE=struct.calcsize('128s32sI8s')

fhead = client.recv(FILEINFO_SIZE)
filename,temp1,filesize,temp2=struct.unpack('128s32sI8s',fhead)
print filename,temp1,filesize,temp2
filename = 'new_' + 'capture.jpeg'.strip('\00')
fp = open(filename,'wb')
restsize = filesize
while True:
    if restsize > BUFSIZE:
        filedata = client.recv(BUFSIZE)
    else:
        filedata = client.recv(restsize)
    if not filedata:
        break
    fp.write(filedata)
    restsize = restsize - len(filedata)
    if restsize == 0:
        break
print "Received Successful!"
fp.close()
client.close()

lena = mpimg.imread(filename)
plt.imshow(lena)
plt.axis('off')
plt.show()