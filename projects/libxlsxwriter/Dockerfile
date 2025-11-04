# Copyright 2024 Google LLC
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
################################################################################

FROM gcr.io/oss-fuzz-base/base-builder
RUN apt-get update && apt-get install -y cmake make zlib1g-dev

RUN git clone --depth 1 https://github.com/jmcnamara/libxlsxwriter.git libxlsxwriter \
        && cp libxlsxwriter/dev/fuzzing/build.sh $SRC/
WORKDIR libxlsxwriter

RUN git fetch --depth=1 origin f0647157ba70d3b9372e5eef05ed489c73107b62
RUN git reset --hard f0647157ba70d3b9372e5eef05ed489c73107b62
