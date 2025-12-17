**Using PdfPlumber in an AWS Lambda**

PDFPlumber is an excellent library to parse and extract data (especially in tables) from PDF documents. Here is how you can use it in an AWS Lambda. Learn more at https://github.com/jsvine/pdfplumber

1. **Layer**  
   To use PDFPlumber, you first need to create a layer that can be used to import the library.
   a. I like to do this in a Virtual Env  
   ```
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
   b.Download the PDFPlumber files  
   ```
   python -m pip install pdfplumber==0.11.8 --platform manylinux2014_x86_64 --only-binary=:all: -t python/ --no-user
   ```
   c. Create a zip file which will be used as the layer
   ```
   Compress-Archive -Path .\python\ -DestinationPath test.zip
   ```
   Important: the zip file should have a subfolder named "python" with all the files within it.  
   d. Create the layer in AWS  
   In the AWS Lambda Console, go to the Layer option and create a new layer and add the file using the Upload option. Set the architecture to x86_64 and pick the compatiable runtimes for python.  
   Hit Create!  
2. **Test Code:**  
   
```python
import json
import logging
import os
import requests
from io import BytesIO
import pdfplumber

log_level_str = os.environ.get("log_level", "WARNING").upper()
log_level = logging.getLevelName(log_level_str)
if (isinstance(log_level,str)):
    print(f"Invalid log_level {log_level_str}")
    log_level = logging.WARNING
else:
    print(f"logging at level {log_level_str} {log_level}")
    
default_log_args = {
    "level": log_level,
    "format": "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    "datefmt": "%y-%b-%d %H:%M",
    "force": True,
}
logging.basicConfig(**default_log_args)
_logger = logging.getLogger(__name__)
_logger.setLevel("DEBUG")


def lambda_handler(event, context):
    
    url = event.get("url")
    if url is None:
        _logger.error("No url provided")
        return {"returnData":"No url provided"}

    _logger.debug(f'retrieving {url}')
    response = requests.get(url)
    bytes_io = BytesIO(response.content)

    _logger.debug(f'processing document')
    with pdfplumber.open(bytes_io) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            _logger.info(f'Text: {text[:100]}')

            tables = page.extract_tables()
            _logger.info(f'Found: {len(tables)} tables')
            _logger.info(f'First table: {tables[0][0]} ')

    _logger.info("test successfull")
    return {"returnData":"test successfull"}
```  
3. **Test it!**  
   Run the code using the following test event  
```
{
  "url": "https://github.com/jsvine/pdfplumber/blob/6ebc549888ed435c43691439e76df8a18ea2cf81/examples/pdfs/background-checks.pdf?raw=true"
}
```
