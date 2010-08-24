import linuxtuples, bottle, hashlib, inspect, simplejson

bottle.debug(True)

@bottle.route('/')
def root():
    conn = linuxtuples.connect('istio.local', 25000)
    key = hashlib.md5(bottle.request.url).hexdigest()
    return dict(t=conn.read(('done', key, None)))

bottle.run(reloader=True)
