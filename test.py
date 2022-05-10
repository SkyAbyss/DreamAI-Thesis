import bluetooth

target_name = "My Phone"
target_address = None

nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices:
    if target_name == bluetooth.lookup_name( bdaddr ):
        target_address = bdaddr
        break

if target_address is not None:
    print("I have found a device nearby. Would you like to connect to it? ", target_address)
else:
    print("I haven't found any devices nearby. Want me to scan again?")