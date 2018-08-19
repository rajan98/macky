import subprocess
import argparse
import re


def find_mac(interface):
    try:
        result = subprocess.check_output(['ifconfig', interface])
    except:
        print('[-] Device Not found')
        exit()
    all_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(result))
    if not all_mac:
        return None
    return all_mac.group(0)


def change_mac(interface, new_mac):
    print('[+] Changing MAC of {0} to {1}'.format(interface, new_mac))
    oldMac = find_mac(interface)
    if oldMac:
        print('old MAC: {0}'.format(oldMac))
        subprocess.call(['ifconfig', interface, 'down'])
        subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
        subprocess.call(['ifconfig', interface, 'up'])

        newMac = find_mac(interface)
        if newMac:
            if newMac == oldMac:
                print('[-] Unable to change the MAC address')
            else:
                print('[+] MAC address was changed Successfully to {0}'.format(newMac))
    else:
        print('[-] Could not Find MAC address for specified interface')


def main():
    parser = argparse.ArgumentParser(
        description='This script is used to change the Mac address of any network card',
        epilog= 'This is how you use this script'
    )
    parser.add_argument('interface', help='Enter the name of the interface')
    parser.add_argument('mac', help='Enter new MAC address')

    args = parser.parse_args()

    change_mac(args.interface, args.mac)


if __name__ == "__main__":
    main()
