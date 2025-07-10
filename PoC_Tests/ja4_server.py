import scapy.all as scapy
from ja4 import generate_ja4

# Function to process TLS packets and generate JA4 hash
def process_packet(packet):
    if packet.haslayer(scapy.TCP) and packet.haslayer(scapy.TLS):
        tls_payload = packet[scapy.TLS].payload

        # Check if it's a TLS Client Hello message
        if tls_payload.startswith(b'\x16\x03\x01\x00'):
            try:
                # Generate the JA4 hash
                ja4_hash = generate_ja4(tls_payload)
                print(f"JA4 Hash: {ja4_hash}")

            except Exception as e:
                print(f"Error processing packet: {e}")

# Sniff TLS packets on port 443
scapy.sniff(prn=process_packet, filter="tcp port 8585", store=False)

