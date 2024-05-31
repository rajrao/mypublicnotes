1. Install Raspberyy Pi Imager on Windows machine
2. Pick the Raspberry Pi Os image
3. add ssh.txt to the root of the SD card
4. ping the addresss (eg:raspberrypi2.local)
5. ssh (ssh admin@raspberrypi2.local) [where admin is the username you picked]
6. sudo raspi-config [allows you to update the pi]


Speedtest [https://pimylifeup.com/raspberry-pi-internet-speed-monitor/]  
1. sudo apt install curl
2. curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | sudo bash
3. sudo apt install speedtest-cli

1. sudo apt-get update
2. sudo apt-get upgrade
3. sudo apt install apt-transport-https gnupg1 dirmngr lsb-release
4. 4
