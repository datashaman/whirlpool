import time, redis

FETCH_INTERVAL = 0.0001

class TupleSpace(redis.Redis):
    def __init__(self, opts={}):
        self.opts = dict(host='localhost', port=6379, db=0)
        self.opts.update(opts)
        super(TupleSpace, self).__init__(**self.opts)
	 
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
        while self.exists(template) == 0:
            time.sleep(FETCH_INTERVAL)
        return self.get(template)
