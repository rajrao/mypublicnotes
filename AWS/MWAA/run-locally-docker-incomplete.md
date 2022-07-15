Pre-requisites:

1. Install Windows Subsytem for Linux: https://code.visualstudio.com/blogs/2020/03/02/docker-in-wsl2#_getting-set-up
1. Install Docker Desktop: https://docs.docker.com/desktop/windows/wsl/

**Important: dont do the following by going to your local drive (eg: mnt/c/....). This will cause a lot of problems!!!**

1. Open your WSL via Windows terminal.
2. Download the Git Repo:
```
git clone https://github.com/aws/aws-mwaa-local-runner.git
```
3. Cd aws-mwaa-local-runner
3. Build the image
```
./mwaa-local-env build-image
```

If the command fails with the error "Bash script and /bin/bash^M: bad interpreter: No such file or directory", then you are likely trying to run from your windows drive. Dont do it!. But if you must fix the error, then run the following to see if the issue is because of windows new-line characters (it worked for me!)
```
sed -i -e 's/\r$//' mwaa-local-env
sed -i -e 's/\r$//' docker/script/*.*
```
4. Run the image:
```
./mwaa-local-env start
```
If you get the following error: "aws-mwaa-local-runner-2.0.2" is not a valid project name, then you can fix it by editing the mwaa-local-env file and changing:
```
AIRFLOW_VERSION=2.0.2
```
To: 
```
AIRFLOW_VERSION=2_0_2
```
This part of the process might take some time to complete.

5. Connect to the environment:
After MWAA has started, you can access it by visiting: http://localhost:8080/
You will need to use the following creds:

Username: admin

Password: test

7. Running your DAGs
You need to copy your code to the "Dags" folder. If you need to do this from Windows, you can get to your home dir in WSL by going to: \\wsl$\Ubuntu\home\%USERNAME%




More info:
1. https://github.com/aws/aws-mwaa-local-runner
2. https://docs.aws.amazon.com/mwaa/latest/userguide/tutorials-docker.html



