# Copyright 2011 Element 34
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
===========
string_data
===========
"""
import random
import string

def random_string(random_length = None):
    """
    A generator for creating random string data of letters plus ' ' (whitespace)
    
    :params random_length: how many characters of random string data. if not provided, will be between 1 - 30
    :returns: String
    """
    choices = string.letters + ' '
    text = []
    if not random_length:
        random_length = random.randint(1, 30)
    for x in range(random_length):
        text.append(random.choice(choices))
    return "".join(text)