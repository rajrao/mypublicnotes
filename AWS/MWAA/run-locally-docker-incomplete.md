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
This part of the process might take some time to complete (15 to 20 minutes)





