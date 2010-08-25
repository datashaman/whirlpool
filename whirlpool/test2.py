import tuplespace, time

ts = tuplespace.TupleSpace()

index = 0
while True:
    index += 1
    ts.set('event:%d' % index, 'some event')
    time.sleep(0.001)
