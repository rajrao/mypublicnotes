```
import logging
#_logger = logging.getLogger(__name__)

class MyBestClass:
  
  def my_method():
    _logger.debug("debug")
    _logger.info("info")
    
    #always use format, as its more performant
    #when logging is not enabled
    _logger.info("Some number or data: {}".format(data))
