# sample client of a CDMI service

from vcdm import cdmi

endpoint = "http://localhost:2364/"
credentials = {'user': 'aaa',
               'password': 'aaa'}

localfile = 'test_file.txt'
remoteblob = 'test_file.txt'
remoteblob2 = '/mydata/text_file.txt'

remote_container = '/mydata'
remote_container2 = '/mydata/more'

conn = cdmi.CDMIConnection(endpoint, credentials)

# blob operations
conn.create_blob(localfile, remoteblob, mimetype='text/plain')
conn.update_blob(localfile, remoteblob, mimetype='text/plain')

value = conn.read_blob(remoteblob)
print "=== Value ==\n%s\n" % value

conn.delete_blob(remoteblob)

# container operations
conn.create_container(remote_container)
print conn.read_container('/')
conn.delete_container(remote_container)
print conn.read_container('/')
