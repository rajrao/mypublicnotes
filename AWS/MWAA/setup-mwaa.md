EC2:

mwaa local runner set up:
sudo yum install docker
pip3 install docker-cli
pip3 install docker-compose
pip3 install docker-compose
sudo yum install git
git clone
https://github.com/aws/aws-mwaa-local-runner.git
--branch v2.7.2
sudo usermod -a -G docker ec2-user
newgrp docker
sudo systemctl enable docker.service
sudo systemctl start docker.service
sudo ./mwaa-locl-env build-image
sudo ./mwaa-local-env build-image
./mwaa-local-env package-requirements
