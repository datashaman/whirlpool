import tuplespace

ts = tuplespace.TupleSpace()

print ts.set('event:1', 'some event')
print ts.set('event:2', 'some event')

while True:
    print ts.take('event*')
