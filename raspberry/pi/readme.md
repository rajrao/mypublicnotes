1. Install Raspberyy Pi Imager on Windows machine
2. Pick the Raspberry Pi Os image
3. add ssh.txt to the root of the SD card
4. ping the addresss (eg:raspberrypi2.local)
5. ssh (ssh admin@raspberrypi2.local) [where admin is the username you picked]
6. sudo raspi-config [allows you to update the pi]

Model:  
cat /sys/firmware/devicetree/base/model;echo




Speedtest [https://pimylifeup.com/raspberry-pi-internet-speed-monitor/]  
1. sudo apt install speedtest-cli

Lan info: 
1. ifconfig
2. mii-tool

