# Program to split URL into 4 components

url = input("Enter a URL: ")

# Step 1: Split protocol and the rest
protocol_split = url.split("://")
protocol = protocol_split[0]
remaining = protocol_split[1]

# Step 2: Split domain/port and path
if '/' in remaining:
    domain_port, path = remaining.split('/', 1)
    path = '/' + path
else:
    domain_port = remaining
    path = ''

# Step 3: Split domain and port if present
if ':' in domain_port:
    domain, port = domain_port.split(':')
else:
    domain = domain_port
    port = 'Default'

# Step 4: Display results
print("Protocol:", protocol)
print("Domain:", domain)
print("Port:", port)
print("Path:", path)
