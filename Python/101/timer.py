# https://stackoverflow.com/a/25823885/44815
# https://replit.com/@rajrao2/elapsedTimeTest
def do_work():
  import time
  time.sleep(2.4)
  
def method1():
  """
  recommended approach as default_timer will be best timer on platform
  """
  from timeit import default_timer as timer
  start = timer()
  do_work()
  end = timer()
  print(end - start) #Time in seconds, e.g. 5.38091952400282

def method2():
  """
  default option
  """
  import time

  start = time.time()
  do_work()
  end = time.time()
  print(end - start)
 

method1()
method2()
