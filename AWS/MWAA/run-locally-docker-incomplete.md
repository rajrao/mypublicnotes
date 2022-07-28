Pre-requisites:

1. Install Windows Subsytem for Linux: https://code.visualstudio.com/blogs/2020/03/02/docker-in-wsl2#_getting-set-up
1. Install Docker Desktop: https://docs.docker.com/desktop/windows/wsl/
1. Make sure you have Ubuntu installed as part of WSL: https://ubuntu.com/wsl
```
wsl -l
```
**Output**
```
Windows Subsystem for Linux Distributions:
Ubuntu (Default)
docker-desktop
docker-desktop-data
```

1. Open your WSL via Windows terminal and change directory to your home
```wsl ~```
2. Download the Git Repo (v2.2.2 branch):
```
git clone https://github.com/aws/aws-mwaa-local-runner.git aws-mwaa-local-runner --single-branch --branch
 v2.2.2
```
5. Edit the docker/docker-compose-local.yml file
change the line:
- "${PWD}/db-data:/var/lib/postgresql/data"
to
- postgres-db-volume:/var/lib/postgresql/data

6. Cd aws-mwaa-local-runner
7. Build the image
```
./mwaa-local-env build-image
```
8. Run the image:
```
./mwaa-local-env start
```
* If you get the following error: "aws-mwaa-local-runner-2.2 is not a valid project name or aws-mwaa-local-runner-2.0.2" is not a valid project name, then you can fix it by going into Docker Desktop settings and under "General", Uncheck: "Use Docker Compose V2"
* If your postgresql container does not start up with an error like this: "chmod: /var/lib/postgresql/data: Operation not permitted", then do the following:
Change the following line in "docker\docker-compose-local.yml":
```
"- ${PWD}/db-data:/var/lib/postgresql/data"
```
to
```
- postgres-db-volume:/var/lib/postgresql/data
```
Also, at the end of the file, add the following line:
```
volumes:
  postgres-db-volume:    
```
This uses a named volume. I believe the error occurs because I am using a linked folder on the Windows desktop and the postgresql container has a script that attempts to take ownership of that folder.

9. The airflow instance should start up and you should have access to Airflow via:http://localhost:8080/
You will need to use the following creds:

Username: admin

Password: test

7. Running your DAGs
You can add your dags to the Dags subfolder of aws-mwaa-local-runner.

Tips:
1. In your WSL terminal, you can type ```explorer.exe .``` and it will open a windows explorer window to that path. Its a quick way to find out where you are in your WSL container.
2. Instead of 

More info:
1. https://github.com/aws/aws-mwaa-local-runner
2. https://docs.aws.amazon.com/mwaa/latest/userguide/tutorials-docker.html



