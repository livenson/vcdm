##
# Copyright 2002-2012 Ilja Livenson, PDC KTH
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##
import vcdm

backend = vcdm.env['mq']
ds = vcdm.env['ds']


def create(qnm):
    backend.create(qnm)


def delete(qnm):
    backend.delete(qnm)


def enqueue(qnm, value):
    backend.enqueue(qnm, value)


def get(qnm):
    return backend.get(qnm)


def delete_message(qnm):
    backend.delete_message(qnm)
