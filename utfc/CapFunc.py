from scapy.all import *

'''
g = []
pkt = rdpcap('pcap')
for i in pkt:
 if i[ICMP].type == 8:
  g.append(i[IP].ttl)
print ''.join([chr(x) for x in g])

def processCap(fileName):
    packet=rdpcap(fileName)
    res_key=os.path.basename(fileName)
    res={}
    extenList=[]
    #only process client hello packet
    for item in packet:
        if item.haslayer(TLSClientHello):
            clienthello = item.getlayer(TLSClientHello)
            if clienthello.haslayer(TLSExtension):
                extnum=len(clienthello.extensions)
                #print "clienthello:"
                #print clienthello.show()
                for i in range(1,extnum+1):
                    extension = clienthello.getlayer(TLSExtension,i)
                    #print "extension:"
                    #print extension.show()
                    exten = '{:04x}'.format(extension.type)
                    extenList.append(exten)
                    #only process the first client hello
            break
    res[res_key] = extenList
    return res 
'''


class CapF:
    pkt = None

    def __init__(self, fn):
        self.pkt = rdpcap(fn)
        print('FileName:', fn)
        print('Records:', len(self.pkt))
        self.pkt.summary()

    pass
