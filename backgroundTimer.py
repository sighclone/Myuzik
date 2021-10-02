import time

while(True):
  start_time = time.time()
  time.sleep(30)
  end_time = time.time()
  
  # observe if people are in vc here...

  print("timer log: observed time is from " + str(start_time) + " to " + str(end_time) + " totalling " + str(start_time - end_time) +"secs")
