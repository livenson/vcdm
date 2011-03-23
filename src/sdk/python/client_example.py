
# sample python client
import vcdm

conn = vcdm.CDMIConnection(endpoint, credentials)

# blob operations
vcdm.blob.write(local_file, remote_path)
vcdm.blob.read(remote_file_url)
vcdm.blob.read(remote_file_UID)
vcdm.blob.delete(remote_file, path)
vcdm.blob.update(local_file, remote_path)

# mq operations
vcdm.mq.put(m, channel)
m = vcdm.mq.get(channel)

# searching
vcdm.blob.find(pattern, path)
vcdm.blob.find(user)
vcdm.blob.find(filesize)

