"""
Tuplespace implementation for python.

Copyright (c) 2010, Marlin Forbes
All rights reserved.


Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.

    * Neither the name of the Data Shaman nor the names of its contributors
      may be used to endorse or promote products derived from this software
      without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

__author__ = 'Marlin Forbes <marlinf@datashaman.com>'

import time, redis

FETCH_INTERVAL = 0.0001

class Whirlpool(redis.Redis):
    def __init__(self, opts={}):
        self.opts = dict(host='localhost', port=6379, db=0)
        self.opts.update(opts)
        super(Whirlpool, self).__init__(**self.opts)
	 
    def take(self, template):
        while True:
            matches = self.keys(template)

            if len(matches) > 0:
                results = {}
                for match in matches:
                    results[match] = self.get(match)
                    self.delete(match)
                return results

            time.sleep(FETCH_INTERVAL)
         
    def read(self, template):
        result = self.blpop(template)
        print result
        self.lpush(template)
