# -*- coding: cp936 -*-
from PIL import ImageGrab
from socket import *
import os,struct


# im = ImageGrab.grab()
# im.save('c:\\Users\\zhang\\Desktop\\1', 'jpeg')

port = 12345
BUFSIZE=1024
s = socket(AF_INET6, SOCK_STREAM)
s.bind(('', port))

s.listen(5)
while True:
    print('waiting for connection')
    tcpClientSock, addr = s.accept()
    print('connect from ', addr)
    while True:
        try:
            data = tcpClientSock.recv(BUFSIZE)
        except:
            print(error)
            tcpClientSock.close()
            break
        if not data:
            break
        print(data.decode('utf8'))
        if 'capture' in data.decode('utf8'):
            im = ImageGrab.grab()
            filename = 'capture.jpeg'
            im.save(filename, 'jpeg')

            BUFSIZE = 1024
            FILEINFO_SIZE = struct.calcsize('128s32sI8s')
            fhead = struct.pack('128s11I', filename, 0, 0, 0, 0, 0, 0, 0, 0, os.stat(filename).st_size, 0, 0)
            tcpClientSock.send(fhead)
            fp = open(filename, 'rb')
            while True:
                filedata = fp.read(BUFSIZE)
                if not filedata:
                    break
                tcpClientSock.send(filedata)
            print "Send Successful!"
            fp.close()



            # lena = mpimg.imread(filename)
            # plt.imshow(lena)
            # plt.axis('off')
            # plt.show()

tcpClientSock.close()
s.close()