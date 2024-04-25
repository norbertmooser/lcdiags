import subprocess
import multiprocessing
import os
import signal
from scapy.all import *

class TcpDumpProcess(multiprocessing.Process):
    def __init__(self, interface, pcap_file, filter):
        super().__init__()
        self.interface = interface
        self.pcap_file = pcap_file
        self._stop_event = multiprocessing.Event()
        self.filter = filter
        
    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        # command = ['sudo', 'tcpdump', '-i', self.interface, '-w', self.pcap_file]
        command = ['tcpdump', '-i', self.interface, self.filter, '-U','-w', self.pcap_file]
        self.process = subprocess.Popen(command, preexec_fn=os.setsid)
        self.process.wait()

# Function to read packets from the FIFO
def read_packets_from_fifo(fifo_path):
    with open(fifo_path, 'rb') as fifo:
        for packet in PcapReader(fifo):
            # Process packet as needed
            print(packet.summary())  # Example: Print a summary of the packet

# Example usage
if __name__ == '__main__':
    # Define the path for the FIFO (named pipe)
    fifo_path = 'tcpdump_fifo'

    # Check if the FIFO file exists and remove it if it does
    if os.path.exists(fifo_path):
        os.remove(fifo_path)

    # Create the FIFO
    os.mkfifo(fifo_path)

    # Start tcpdump process to write packets to the pcap file
    tcpdump_process = TcpDumpProcess('enp5s0', fifo_path, "host 13.107.42.14")
    tcpdump_process.start()

    try:
        # Read packets from the FIFO
        read_packets_from_fifo(fifo_path)
    except KeyboardInterrupt:
        # Stop the tcpdump process gracefully
        os.killpg(os.getpgid(tcpdump_process.process.pid), signal.SIGTERM)
        tcpdump_process.join()

    # Clean up
    os.remove(fifo_path)
