# Copyright 2019 Google Inc.
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
MAINTAINER guidovranken@gmail.com
RUN apt-get update && apt-get install -y \
  make \
  autoconf \
  automake \
  libtool \
  pkg-config \
  protobuf-compiler \
  libprotobuf-dev \
  libprotoc-dev

RUN git clone --depth 1 https://github.com/protobuf-c/protobuf-c.git -b next
RUN git clone --depth 1 https://github.com/guidovranken/fuzzing-headers.git
RUN git clone --depth 1 https://github.com/RuiWang6188/protobuf-c-fuzzers.git
COPY build.sh $SRC/

WORKDIR $SRC/protobuf-c
RUN git fetch --depth=1 origin e05528c871ef89d6578b9b1b911f0d774de910eb
RUN git reset --hard e05528c871ef89d6578b9b1b911f0d774de910eb

WORKDIR $SRC
