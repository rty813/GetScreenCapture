# -*- coding: cp936 -*-
from socket import *
import struct, os
from PIL import Image

HOST = '10.22.51.193'
PORT = 12345
BUFSIZE = 1024
ADDR = (HOST, PORT)

client = socket(AF_INET, SOCK_STREAM)
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

im = Image.open(filename)
im.show()