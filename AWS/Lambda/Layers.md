Creating a layer file to satisfy a package requirement:

1. Install the package to a specific folder:
    ```pip install {package} --target ./package ```
    
    **examples**: 
    
    ```pip install boto3 --target python/. ```
    
    ```pip install msal --target ./package ```
    
2. Zip the contents of package so that the contents are in a subfolder called "python".
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
3. Create the lazer in lambda: https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2#/layers
    * Set the Runtime to Python.
    * In the description include the version
    * upload the zip file
4. Specify the layer in the lambda function


Note: see https://docs.aws.amazon.com/textract/latest/dg/lambda.html for an example


need to test this to see if it can be a cleaner solution: pip install --upgrade --only-binary=:all: --platform manylinux2014_x86_64 package -t .
