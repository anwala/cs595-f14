#Hash URIs function
def getHashFromURI(uri):
	md5hash = ''
	if( len(uri) > 0 ):
		# Assumes the default UTF-8; http://www.pythoncentral.io/hashing-strings-with-python/
		hash_object = hashlib.md5(uri.encode())
		md5hash = hash_object.hexdigest()

	return md5hash