import serial.tools.list_ports
ports = list(serial.tools.list_ports.comports())

"""global port_name
for p in ports:
    p=str(p)
    if "USB" in p:
        #print(p.split())
        port_name=p.split()[0]

print(port_name)
"""

for p in ports:
    print(str(p))