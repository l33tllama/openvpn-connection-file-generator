# openvpn-connection-file-generator
Generates OpenVPN files from one machine with minimal key presses.

## Usage:
`python3 remote-gen.py <cient name>`  
  
It will step you through the process of generating a `.ovpn` file, which involves several scp and ssh commands to the VPN anc CA servers. All going well, it should send you back an `.ovpn` file in the root directory of this project.

## Requirements
First you must have set up an OpenVPN server and signing server. A great tutorial on how to do that, is here: [https://www.digitalocean.com/community/tutorials/how-to-set-up-and-configure-an-openvpn-server-on-ubuntu-20-04](https://www.digitalocean.com/community/tutorials/how-to-set-up-and-configure-an-openvpn-server-on-ubuntu-20-04).  
I then highly recommend adding your public key to both the OpenVPN server and CA server's `authorized_keys` files. Then this script will be even easier.

## Buy me a coffee ☕️
Did this save you time? You can buy me a coffee: [https://www.buymeacoffee.com/leofebey](https://www.buymeacoffee.com/leofebey)
