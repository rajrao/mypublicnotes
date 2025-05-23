The following lists the steps I had success with to run the AWS-MWAA-LocalRunner project to get AWS Airflow running locally. Thanks to [@cklimkowski](https://github.com/cklimkowski) for helping troubleshoot and fix all my issues.

**Pre-requisites**

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

**Steps**

1. Open your WSL via Windows terminal and change directory to your home
From command prompt: ```wsl ~```
If you already are in your WSL container, then: ```cd ~```
2. Download the Git Repo (v2.2.2 branch):
```
git clone https://github.com/aws/aws-mwaa-local-runner.git aws-mwaa-local-runner --single-branch --branch
 v2.2.2
```
3. Cd aws-mwaa-local-runner
4. Optional: Repoint the sub-folder dags to a windows folder to allow you to easily edit and change the files for developments
 1. delete the dags folder using the command ```rm -fr dags```
 2. create a symbolink to a dags folder on your c drive ```ln /mnt/c/repos/dags/ dags -s``` (i used a folder under c:\repos called dags)
5. Build the image
```
./mwaa-local-env build-image
```
6. Run the image:
```
./mwaa-local-env start
```

 * If you get the following error: "aws-mwaa-local-runner-2.2 is not a valid project name or aws-mwaa-local-runner-2.0.2" is not a valid project name, then you can fix it by going into Docker Desktop settings and under "General", Uncheck: "Use Docker Compose V2"
 * If you get an error that says something like a folder under docker-desktop-bind-mounts/Ubuntu is not empty, then restart your docker-desktop (shutdown and restart). This worked for me!

7. The airflow instance should start up and you should have access to Airflow via: <a href="http://localhost:8080/" target="_blank">http://localhost:8080/</a>
 
  **You will need to use the following creds:**

    Username: admin
    Password: test

**Running your own DAGs**
   
   You can add more dags or edit the dags directly in your c drive. In my case the files were located at c:\repos\dags. (see step 7.2.)

**Tips:**

1. In your WSL terminal, you can type ```explorer.exe .``` and it will open a windows explorer window to that path. Its a quick way to find out where you are in your WSL container.

**More info:**

1. https://github.com/aws/aws-mwaa-local-runner
2. https://docs.aws.amazon.com/mwaa/latest/userguide/tutorials-docker.html
