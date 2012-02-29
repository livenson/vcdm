import unittest
import struct
import re
from vcdm.server.cdmi.common import generate_guid, generate_guid_b64


class GuidGenTestCase(unittest.TestCase):
    def testGuidIsTimeDependent(self):
        guid1 = generate_guid()
        guid2 = generate_guid()
        self.assertNotEqual(guid1, guid2)

    def testBasic64Conversion(self):
        guid = generate_guid_b64()
        self.assertTrue(re.match('[0-9A-Za-z=\\/\\w]+', guid))
        #self.assertEqual(guid[-2:], '==')

    def testMustBeVendorDependent(self):
        guid1 = generate_guid(entnumber=32012)
        guid2 = generate_guid(entnumber=15232)
        self.assertNotEqual(guid1[0:4], guid2[0:4])

    def testSizeMustReflectTheGuidSize(self):
        guid = generate_guid()
        guiddata = struct.unpack('!LBBH' + 'p' * (len(guid) - 8), guid)
        #print guid[:8].encode('hex'), ' ', guid[8:].encode('hex')
        self.assertEqual(len(guid), guiddata[2])

if __name__ == '__main__':
    unittest.main()
