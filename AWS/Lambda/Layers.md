**Updated 2025-06-02**

1. **Install package** to folder python  
replace package and version  
```pip install {package}=={version} --platform manylinux2014_x86_64 --only-binary=:all: -t python/ --no-user```
eg:  
```pip install paramiko==3.5.1 --platform manylinux2014_x86_64 --only-binary=:all: -t python/ --no-user```

* --platform manylinux2014_x86_64:  
&emsp;Developing on a non-Linux OS (e.g., Windows or macOS) but deploying to Linux (e.g., AWS Lambda, Docker containers): If you pip install a package with compiled extensions on your local machine, it will compile for your local OS. If you then deploy that package to a Linux environment, it will likely fail. By using --platform manylinux2014_x86_64, you tell pip to download the pre-compiled Linux-compatible wheel instead.

* --only-binary=:all:  
&emsp;This additional flag is frequently used with --platform to tell pip only to download binary wheels and not attempt to compile from source if a pre-built wheel isn't found for the specified platform. This helps avoid compilation issues and ensures you get the desired manylinux package.

2. **Zip** the folder so that the zip contains a folder called python. On windows, you will get this if you zip the python folder by right clicking on it and choosing the "Compress to" option.  
eg:  
```
paramkip-3.5.1.zip
|--python (folder)  
       |-- xxxxx
       |-- yyyyy
```



-----

Creating a layer file to satisfy a package requirement:

1. Install the package to a specific folder:
    ```pip install {package} --target ./package ```
    
    **examples**: 
    
    ```pip install boto3 --target python/. ```  
   or  
    ```pip install msal --target ./package ```
   

   **Notes**: if you get the error: **ERROR: Can not combine '--user' and '--target'**, then add the flag **--no-user**
      
3. Zip the contents of package so that the contents are in a subfolder called "python".  
   Example folder structure
    ```
    ZipFile (msal-1.16.0.zip)
    |--python (folder)
       |--contents from package folder
       |--pymysql (folder)
       |--PyMySql-1.0.2.dist-info (folder)
       |--msal (folder)
       |--MSAL-1.16.0.dist-info (folder)
       |--Other folders
    ```
    The zip file should be named with the version of the package.
    Command: ```zip boto3-layer.zip -r python/```

4. Create the lazer in lambda: https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2#/layers
    * Set the Runtime to Python.
    * In the description include the version
    * upload the zip file
5. Specify the layer in the lambda function


Note: see https://docs.aws.amazon.com/textract/latest/dg/lambda.html for an example


need to test this to see if it can be a cleaner solution: pip install --upgrade --only-binary=:all: --platform manylinux2014_x86_64 package -t .
