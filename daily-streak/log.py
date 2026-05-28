import json
import sys
from datetime import datetime

def log(level, *args):
  message = args
  if len(args) == 1:
    message = args[0]

  log_data = {
    "timestamp": datetime.now().isoformat(),
    "type": level,
    "message": message
  }
  
  sys.stdout.write(json.dumps(log_data) + "\n")
  sys.stdout.flush()

def info(*args):
  log("info", *args)

def error(*args):
  log("error", *args)