import urllib2
from urllib import addinfourl
req = urllib2.Request('http://localhost:4810/server/info')
req.add_header('content-type' , 'text/xml')
scamXML = '<commands><comment><text>haha</text></comment></commands>'
opener = urllib2.build_opener()
response = opener.open(req)
print response.read()
print response.close()