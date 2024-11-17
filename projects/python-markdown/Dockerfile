#!/usr/bin/python3
# Copyright 2022 Google LLC
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
FROM gcr.io/oss-fuzz-base/base-builder-python
RUN git clone https://github.com/python-markdown/markdown markdown
COPY *.sh *py $SRC/
WORKDIR $SRC/markdown

RUN git fetch --depth=1 origin 0b5e80efbb83f119e0e38801bf5b5b5864c67cd0
RUN git reset --hard 0b5e80efbb83f119e0e38801bf5b5b5864c67cd0
