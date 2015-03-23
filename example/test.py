class A(object):
    def hha(self):
        print 'nonzero calling'
        return True
    
    def jj(self):
        print 'len calling'
        return False
    
if A():
    print 'OK'
else:
    print 'Not OK'