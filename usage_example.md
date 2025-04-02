from veryyip import VeryyIP

ip = VeryyIP()

# Get local IP address
print(ip.get('private'))

# Get public IP address
print(ip.get('public'))

