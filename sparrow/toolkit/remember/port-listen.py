import psutil

# Get all network connections with kind 'inet' (IPv4/IPv6)
connections = psutil.net_connections(kind='inet')

# Filter connections that are in LISTEN state and get their local port
listening_ports = [conn.laddr.port for conn in connections if conn.status == psutil.CONN_LISTEN]

# Remove duplicates and sort the ports
unique_ports = sorted(set(listening_ports))

print("Listening TCP ports:")
for port in unique_ports:
    print(port)
