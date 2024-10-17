#!/usr/bin/python3

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
from datetime import datetime
import os
import sys
import json
import threading
import atheris
with atheris.instrument_imports():
  import bleach

# coverage is in the format {(filename, lineno): (first-hit time, current fuzzing iteration)}
total_coverage_info = {}
delta_coverage_info = {}
coverage_info_lock = threading.Lock()
START_TIME = None
START_TIME_FLOAT = None
curr_iter = 0


def ignore_file(filename: str) -> bool:
  return any(substring in filename for substring in ['bootstrap', 'construction', 'site-packages']) or 'bleach' not in filename

def trace_lines(frame, event, arg):
    if event == 'line':
        lineno = frame.f_lineno
        filename = frame.f_code.co_filename
        filename = os.path.abspath(filename)

        if ignore_file(filename):
            return trace_lines

        if (filename, lineno) not in total_coverage_info:
            delta_coverage_info[(filename, lineno)] = ((datetime.now() - START_TIME), curr_iter)

    return trace_lines

def save_coverage_info():
    """Appends the current coverage information to a JSON Lines file."""
    global total_coverage_info, delta_coverage_info
    
    timestamp = datetime.now()
    # Prepare the data to be written
    with coverage_info_lock:
        # Convert delta_coverage_info to a serializable format
        serializable_coverage_info = {}
        for key, value in delta_coverage_info.items():
            filename, lineno = key
            first_hit_time, iter = value
            key_str = f"{filename}:{lineno}"
            serializable_coverage_info[key_str] = {
                "first_hit_time": str(first_hit_time),
                "first_hit_iter": iter
            }

    # Create a JSON object containing the timestamp and coverage info
    snapshot = {
        "fuzzing_time": str(timestamp - START_TIME), # in hours
        "delta_coverage_info": serializable_coverage_info
    }

    output_file = '/out/delta_coverage_info.jsonl'

    # Append the JSON object to the file
    with coverage_info_lock:
        with open(output_file, 'a') as f:
            json.dump(snapshot, f)
            f.write('\n')  # Ensure each JSON object is on a new line


    total_coverage_info.update(delta_coverage_info)
    delta_coverage_info = {}

def save_coverage_info_periodically():
    """Saves coverage information every hour for the first day, then every day."""
    interval = 60 * 60  # 1h interval

    while True:
      time.sleep(interval)

      save_coverage_info()



def TestOneInput(input_bytes):
  fdp = atheris.FuzzedDataProvider(input_bytes)
  data = fdp.ConsumeUnicode(atheris.ALL_REMAINING)

  bleach.clean(data)

  global curr_iter
  curr_iter += 1


def main():
  try: 
    global START_TIME
    START_TIME = datetime.now()
    global START_TIME_FLOAT
    START_TIME_FLOAT = time.time()
    sys.settrace(trace_lines)

    # Start the background thread to save coverage info periodically
    save_thread = threading.Thread(target=save_coverage_info_periodically, daemon=True)
    save_thread.start()

    atheris.Setup(sys.argv, TestOneInput, enable_python_coverage=True)
    atheris.Fuzz()

  except KeyboardInterrupt:
    pass
  finally:
    sys.settrace(None)
    save_coverage_info()

if __name__ == "__main__":
  main()
