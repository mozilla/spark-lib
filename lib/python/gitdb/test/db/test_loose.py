from lib import *
from gitdb.db import LooseObjectDB
from gitdb.exc import BadObject
from gitdb.util import bin_to_hex
		
class TestLooseDB(TestDBBase):
	
	@with_rw_directory
	def test_basics(self, path):
		ldb = LooseObjectDB(path)
		
		# write data
		self._assert_object_writing(ldb)
		self._assert_object_writing_async(ldb)
	
		# verify sha iteration and size
		shas = list(ldb.sha_iter())
		assert shas and len(shas[0]) == 20
		
		assert len(shas) == ldb.size()
		
		# verify find short object
		long_sha = bin_to_hex(shas[-1])
		for short_sha in (long_sha[:20], long_sha[:5]):
			assert bin_to_hex(ldb.partial_to_complete_sha_hex(short_sha)) == long_sha
		# END for each sha
		
		self.failUnlessRaises(BadObject, ldb.partial_to_complete_sha_hex, '0000')
		# raises if no object could be foudn
		
