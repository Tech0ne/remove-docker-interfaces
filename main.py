import os
import sys
import subprocess

import netifaces

if os.geteuid() != 0:
    print("Please run as root")
    sys.exit(1)

print("Before removing docker interfaces, we will need to remove all docker containers running.")
print("Continue ? (CTRL+C to stop)")

try:
    input()
except KeyboardInterrupt:
    print("Aborted")
    sys.exit(1)

def docker_ps():
    containers = subprocess.check_output(["docker", "ps", "-aq"]).decode()[:-1].split('\n')
    if len(containers) == 1 and containers[0] == '':
        return []
    return containers

if len(docker_ps()):
    os.system("docker stop $(docker ps -aq)")
    print("Stoped dockers")
if len(docker_ps()):
    os.system("docker rm $(docker ps -aq)")
    print("Removed dockers")

for iface in netifaces.interfaces():
    if iface.startswith("br-"):
        print(f"Removing interface {iface}")
        os.system(f"ip link delete {iface}")
        os.system(f"")
        print(f"Interface removed")

print("All good")
