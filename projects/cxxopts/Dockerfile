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
################################################################################

FROM gcr.io/oss-fuzz-base/base-builder
RUN apt update && apt install -y python3
RUN git clone --depth 1 https://github.com/jarro2783/cxxopts.git cxxopts
WORKDIR cxxopts
COPY build.sh $SRC/

RUN git fetch --depth=1 origin 10a7a647791fa3a24ec4f572f2573a6e0aaa881b
RUN git reset --hard 10a7a647791fa3a24ec4f572f2573a6e0aaa881b
