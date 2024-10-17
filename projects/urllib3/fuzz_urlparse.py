#!/usr/bin/python3
# Copyright 2021 Google LLC
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

import os
import sys
import atheris
import urllib3

import time
from datetime import datetime
import json
import threading

# coverage is in the format {(filename, lineno): (first-hit time, current fuzzing iteration, input, [traced_functions], [traced_filenames])}
curr_input = None
curr_traced_filenames = set()
curr_traced_functions = []
total_coverage_info = {}
delta_coverage_info = {}
coverage_info_lock = threading.Lock()
START_TIME = None
START_TIME_FLOAT = None
curr_iter = 0

def ignore_file(filename: str) -> bool:
    return any(substring in filename for substring in ['bootstrap', 'construction', 'site-packages']) or 'urllib3' not in filename

def trace_lines(frame, event, arg):
    if event == 'call':
        function_name = frame.f_code.co_name
        filename = frame.f_code.co_filename
        curr_traced_functions.append(function_name)
        curr_traced_filenames.add(filename)
    elif event == 'line':
        lineno = frame.f_lineno
        filename = frame.f_code.co_filename
        filename = os.path.abspath(filename)

        if ignore_file(filename):
            return trace_lines

        if (filename, lineno) not in total_coverage_info:
            delta_coverage_info[(filename, lineno)] = ((datetime.now() - START_TIME), curr_iter, curr_input, curr_traced_functions, list(curr_traced_filenames))

    return trace_lines

def  save_coverage_info():
    global total_coverage_info, delta_coverage_info

    timestamp = datetime.now() 
    with coverage_info_lock:
        serializable_coverage_info = {}
        for key, value in delta_coverage_info.items():
            filename, lineno = key
            first_hit_time, iteration, input_data, traced_functions, traced_filenames = value
            key_str = f"{filename}:{lineno}"
            serializable_coverage_info[key_str] = {
                "first_hit_time": first_hit_time.total_seconds(),
                "iteration": iteration,
                "input_data": input_data,
                "traced_functions": traced_functions,
                "traced_filenames": traced_filenames,
            }
    snapshot = {
        "fuzzing_time": str(timestamp - START_TIME),
        "delta_coverage_info": serializable_coverage_info
    }

    output_file = '/out/delta_coverage_info.jsonl'
    
    with coverage_info_lock:
        with open(output_file, 'a') as f:
            json.dump(snapshot, f)
            f.write('\n')

    total_coverage_info.update(delta_coverage_info)
    delta_coverage_info = {}

def save_coverage_info_periodically():
    interval = 60 * 60

    while True:
        time.sleep(interval)
        save_coverage_info()


def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    original = fdp.ConsumeUnicode(sys.maxsize)

    global curr_input, curr_traced_functions, curr_traced_filenames
    try:
        # We have to call this via .url because of limitations
        # in PyCG analysis
        curr_input = original
        response = urllib3.util.url.parse_url(original)
        response.hostname
        response.request_uri
        response.authority
        response.netloc
        response.url
    except urllib3.exceptions.LocationParseError:
        None

    curr_input = None
    curr_traced_functions = []
    curr_traced_filenames = set()

    global curr_iter
    curr_iter += 1

    return

def main():
    try:
        global START_TIME, START_TIME_FLOAT
        START_TIME = datetime.now()
        START_TIME_FLOAT = time.time()
        sys.settrace(trace_lines)

        # Start the background thread to save coverage info periodically
        save_thread = threading.Thread(target=save_coverage_info_periodically, daemon=True)
        save_thread.start()

        atheris.Setup(sys.argv, TestOneInput)
        atheris.Fuzz()
    except KeyboardInterrupt:
        pass
    finally:
        sys.settrace(None)
        save_coverage_info()

if __name__ == "__main__":
    atheris.instrument_all()
    main()

