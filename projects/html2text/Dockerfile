# Copyright 2023 Google LLC
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
#
##########################################################################
FROM gcr.io/oss-fuzz-base/base-builder-python
RUN pip3 install --upgrade pip
RUN git clone https://github.com/Alir3z4/html2text html2text
COPY *.sh *py $SRC/
WORKDIR $SRC/html2text

RUN git fetch --depth=1 origin 8917f5c83d8cf013110124a6b37331b2c29a0fff
RUN git reset --hard 8917f5c83d8cf013110124a6b37331b2c29a0fff

