# Copyright 2020 Google Inc.
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
RUN apt-get update && apt-get install -y cmake

RUN git clone --depth 1 https://github.com/ninja-build/ninja
WORKDIR ninja

RUN git fetch --depth=1 origin a3fda2b06c027f19c7ec68c08e21859e44c15cde
RUN git reset --hard a3fda2b06c027f19c7ec68c08e21859e44c15cde

RUN mv $SRC/ninja/misc/oss-fuzz/build.sh $SRC/
RUN mv $SRC/ninja/misc/oss-fuzz/sample_ninja_build $SRC/
