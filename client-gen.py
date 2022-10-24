from sys import argv
from subprocess import call
from configparser import ConfigParser
import os

def gen_server():
    #config = ConfigParser()
    #config.read("config.cfg")
    #home_dir = config["VPN Server"]["vpn_server_home_dir"]
    home_dir = os.path.expanduser('~')
    easy_rsa_dir = home_dir + "/easy-rsa"
    
    if argv[2]:
        client_name = argv[2]
        # 1. Generate client key
        cmd1 = ["./easyrsa", "gen-req", client_name, "nopass"]
        # 2. Copy to client-configs
        cmd2 = ["cp", easy_rsa_dir + "/pki/private/" + client_name + ".key", home_dir + "/client-configs/keys"]
        print("1. Generate - Calling: " + str(cmd1))
        call(cmd1, cwd=easy_rsa_dir)
        print("2. Copy - Calling: " + str(cmd2))
        call(cmd2)
    else:
        print("No client name specified")

def import_key():
    print("")
    home_dir = os.path.expanduser('~')
    if argv[2]:
        client_name = argv[2]
        # 1. Copy into client configs folder
        cmd1 = ["cp", "/tmp/" + client_name + ".crt", home_dir + "/client-configs/keys"]
        # 2. Generate .OVPN key file
        cmd2 = ["/bin/bash", home_dir + "/client-configs/make_config.sh", client_name]
        print("1. Copy - Calling: " + str(cmd1))
        call(cmd1)
        print("2 - Generate OVPN - Calling: " + str(cmd2))
        call(cmd2)

if __name__ == "__main__":
    
    if argv[1]:
        command = argv[1]
        if command.lower() == "gen":
            gen_server()
        elif command.lower() == "import":
            import_key()
    else:
        print("Usage: client-gen.py <gen|import> <client_name>")