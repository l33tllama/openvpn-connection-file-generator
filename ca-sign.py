from http import server
from sys import argv
from subprocess import call
from configparser import ConfigParser
import os

def import_sign_resend():
    config = ConfigParser()
    config.read(os.path.expanduser('~') + "/config.cfg")
    server_username = config["VPN Server"]["vpn_server_ssh_username"]
    server_name = config["VPN Server"]["vpn_server_hostname"]
    server_port = config["VPN Server"]["vpn_server_ssh_port"]
    server_home = os.path.expanduser('~')
    easy_rsa_dir = server_home + "/easy-rsa"
    if len(argv) > 1:
        client_name = argv[1]
        # Step 1 - import .req file from VPN server (scp)
        cmd1 = ["scp",  "-P", str(server_port), server_username + "@" + server_name + ":"  + easy_rsa_dir +"/pki/reqs/" + \
                client_name + ".req", "/tmp"]
        # Step 2 - import into this EasyRSA server
        cmd2 = ["./easyrsa", "import-req", "/tmp/" + client_name + ".req", client_name]
        # Step 3 - Sign certificate!
        cmd3 = ["./easyrsa", "sign-req", "client", client_name]
        # Step 4 - Send back to server (scp)
        cmd4 = ["scp", "-P", str(server_port), easy_rsa_dir + "/pki/issued/" + client_name + ".crt", \
            server_username + "@" + server_name + ":/tmp"]
        print("1. Copy - Calling: " + str(cmd1))
        call(cmd1)
        print("2. Import Calling: " + str(cmd2))
        call(cmd2, cwd=easy_rsa_dir)
        print("3. Sign - Calling " + str(cmd3))
        call(cmd3, cwd=easy_rsa_dir)
        print("4. Send back - Calling: " + str(cmd4))
        call(cmd4)
    else:
        print("No client name specified.")

if __name__ == "__main__":
    import_sign_resend()