from scapy.all import sniff, ARP

# Define a function to handle ARP packets
def arp_display(packet):
    if ARP in packet:
        print(packet.summary())

# Define a function to start ARP monitoring
def arp_monitor(interface):
    print(f"Monitoring ARP traffic on interface {interface}...")
    sniff(iface=interface, filter="arp", prn=arp_display)

# Start ARP monitoring on interface enp5s0
arp_monitor('enp5s0')
