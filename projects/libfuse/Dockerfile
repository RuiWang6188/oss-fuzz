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
RUN apt-get update && apt-get install -y \
  make autoconf automake libtool meson ninja-build libudev-dev pkg-config \
  udev
RUN git clone --depth 1 https://github.com/AdaLogics/fuzz-headers fuzz-headers
RUN git clone --depth 1 https://github.com/libfuse/libfuse libfuse
WORKDIR libfuse
COPY build.sh *.c $SRC/

RUN git fetch --depth=1 origin 8a3746fe0efb7485bf521dff89dd7dfc735b6879
RUN git reset --hard 8a3746fe0efb7485bf521dff89dd7dfc735b6879
