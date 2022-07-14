Pre-requisites:

1. Install Windows Subsytem for Linux: https://code.visualstudio.com/blogs/2020/03/02/docker-in-wsl2#_getting-set-up
1. Install Docker Desktop: https://docs.docker.com/desktop/windows/wsl/

1. Download the Git Repo:
```
git clone https://github.com/aws/aws-mwaa-local-runner.git
```

2. Run WSL via terminal
3. Build the image
```
./mwaa-local-env build-image
```
If the command fails, then run
```
sed -i -e 's/\r$//' mwaa-local-env
```

You might also have to run
```
sed -i -e 's/\r$//' systemlibs.sh
```
