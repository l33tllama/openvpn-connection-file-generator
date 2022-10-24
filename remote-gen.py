import configparser
from pydoc import cli
from subprocess import call
from sys import argv
from configparser import ConfigParser

class RemoteVPNGen:
    vpn_hostname = ""
    vpn_username = ""
    vpn_ssh_port = ""
    vpn_homedir = ""
    ca_hostname = ""
    ca_username = ""
    ca_ssh_port = ""
    ca_homedir = ""

    def __init__(self) -> None:
        self.load_config("config.cfg")
        client_name = ""
        if len(argv) > 0:
            client_name = argv[1]
            self.make_ovpn_file(client_name)
        else:
            print("Usage: remote-gen.py <client_name>")
        
    def make_ovpn_file(self, client_name):
        print("Generating OVPN file: " + client_name + ".ovpn")
        self.sync_code()
        self.gen_cert_vpn(client_name)
        self.sign_cert_ca(client_name)
        self.import_and_build(client_name)
        self.copy_here(client_name)
        print("All done, enjoy your .ovpn file!")

    def load_config(self, config_filename):
        config = ConfigParser()
        config.read(config_filename)
        # VPN server details
        self.vpn_hostname = config["VPN Server"]["vpn_server_hostname"]
        self.vpn_ssh_port = config["VPN Server"]["vpn_server_ssh_port"]
        self.vpn_ssh_username = config["VPN Server"]["vpn_server_ssh_username"]
        self.vpn_homedir = config["VPN Server"]["vpn_server_home_dir"]
        # TODO: public key enabled

        # CA server details
        self.ca_hostname = config["CA Server"]["ca_server_hostname"]
        self.ca_username = config["CA Server"]["ca_server_ssh_username"]
        self.ca_homedir = config["CA Server"]["ca_server_home_dir"]
        self.ca_ssh_port = config["CA Server"]["ca_server_ssh_port"]
        # TODO: public key enabled

    # 1. Sync code
    def sync_code(self):
        print("1/5: Uploading Python gen and sign files to vpn and ca server.")
        vpn_dest = self.vpn_ssh_username + "@" + self.vpn_hostname + ":" + self.vpn_homedir + "/client-configs"
        ca_dest = self.ca_username + "@" + self.ca_hostname + ":" + self.ca_homedir + "/"
        # Python files
        cmd1 = ["scp", "-P", self.vpn_ssh_port, "client-gen.py", vpn_dest]
        cmd2 = ["scp", "-P", self.ca_ssh_port, "ca-sign.py", ca_dest]
        # Config file
        cmd3 = ["scp", "-P", self.vpn_ssh_port, "config.cfg", vpn_dest]
        cmd4 = ["scp", "-P", self.ca_ssh_port, "config.cfg", ca_dest]
        call(cmd1)
        call(cmd2)
        print("Sent Python files.")
        call(cmd3)
        call(cmd4)
        print("Sent config files.")

    # 2. Generate Certificate
    def gen_cert_vpn(self, client_name):
        exec_command = "python3 " + self.vpn_homedir + "/client-configs/client-gen.py gen " + client_name
        print("2/5: Running generate cert script on VPN server.")
        cmd = ["ssh", "-p", self.vpn_ssh_port, self.vpn_ssh_username + "@" + self.vpn_hostname, exec_command]
        call(cmd)
        print("Done")
    
    # 3. Sign cert on CA machine
    def sign_cert_ca(self, client_name):
        exec_command = "python3 " + self.ca_homedir + "/ca-sign.py " + client_name
        print("3/5: Signing cert on CA machine.")
        cmd = ["ssh", "-p", self.ca_ssh_port, self.ca_username + "@" + self.ca_hostname, exec_command]
        call(cmd)
        print("Done")

    # 4. Import cert and build files on VPN server
    def import_and_build(self, client_name):
        exec_command = "python3 " + self.vpn_homedir + "/client-configs/client-gen.py import " + client_name
        print("4/5: Importing cert and generating ovpn file on VPN server.")
        cmd = ["ssh", "-p", self.vpn_ssh_port, self.vpn_ssh_username + "@" + self.vpn_hostname, exec_command]
        call(cmd)
        print("Done")

    # 5. Copy built .ovpn file back to local machine
    def copy_here(self, client_name):
        # Copy .ovpn file here!
        ovpn_loc = self.vpn_homedir + "/client-configs/files/" + client_name + ".ovpn"
        print("5/5: Copying .ovpn file here.")
        cmd = ["scp", "-P", self.vpn_ssh_port, self.vpn_ssh_username + "@" + self.vpn_hostname + ":" + ovpn_loc, "." ]
        call(cmd)
        print("Done")


if __name__ == "__main__":
    gen = RemoteVPNGen()