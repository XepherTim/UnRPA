# UnRPA Copyright (c) X@MPP 2012
#
# This Tool is Granted to you AS IS, without any implied support or warranty
# The Author of this tool is not Responsible for any misuse or loss of information
# that may be caused by this tool, use at your own discretion
#
# This Tool is For Personal Use only, You Hear By Agree that you will not distribute, 
# Nor Modify and redistribute Extracted content without Prior consent from the Owner of said content.
#
# If you Do not Agree to these Terms, Do not Download this Tool

# 
# Usage: python unrpa.py /path/to/data.rpa
#

import os.path
from pickle import loads
from cStringIO import StringIO
import sys
import types
import time

## == Vars == ##
Path = ""
Map = { }

def UnRPA(_Path,_Dest):
	Map.clear()
	Map[_Path.lower()] = _Path
	fn = transfn(_Path)
	try:
		fn = transfn(_Path)
		fi = file(fn, "rb")
		line = fi.readline()
		if line.startswith("RPA-3.0"):
			print "[*] File Archive is a RenPy 3.0 RPA"
			print "[*] %s" % line
			print "[*] Getting Offset"
			Offset = int(line[8:24], 16)
			print "[*] Offset: %s" % Offset
			print "[*] Getting Key "
			Key = int(line[25:33], 16)
			print "[*] Key: %s " % Key
			print "[*] Seeking Offset"
			fi.seek(Offset)
			print "[*] Loading Index"
			index = loads(fi.read().decode("zlib"))
			print "[*] Deobfuscateing Index..."
			keys_ = 0
			for _key in index.keys():
				if len(index[_key][0]) == 2:
					index[_key] = [(Offset^Key, dlen^Key) for Offset, dlen in index[_key]]
				else:
					index[_key] = [(Offset^Key, dlen^Key,Start) for Offset,dlen,Start in index[_key]]
				keys_ += 1
			print "[*] %s Index Keys Processed" % keys_
			print "[*] Closing File"
			fi.close()
		if line.startswith("RPA-2.0"):
			print "[*] File Archive is a RenPy 2.0 RPA"
			print "[*] %s" % line
			print "[*] Getting Offset"
			Offset = int(line[8:],16)
			print "[*] Offset: %s" % Offset
			print "[*] Seeking Offset"
			fi.seek(Offset)
			print "[*] Loading Index"
			index = loads(fi.read().decode("zlib"))
			print "[*] Closing File"
			fi.close()
		print "[*] Riping Files"
		if not os.path.isdir(_Dest):
			os.mkdir(_Dest)
		f = file(transfn(_Path), "rb")
		t1 = time.time()
		for name, data in index.iteritems():
			print "[*] Extracting %s" % _Dest+"/"+name
			if len(data[0]) == 2:
				offset, dlen = data[0]
				start = ''
			else:
				offset, dlen, start = data[0]
			with open(_Path, "rb") as f:
				f.seek(offset)
				raw_file = start + f.read(dlen - len(start))
			try:
				os.makedirs(os.path.dirname(_Dest+"/"+name))
			except:
				pass
			fi = open(_Dest+"/"+name, 'wb')
			fi.write(raw_file)
			fi.close()
		f.close()
		t2 = time.time()
		print "[*] Done! This Unpacking  took %0.3f milliseconds" % ((t2-t1)*1000.0)
	except:
		print "[*] Failure, Aborting"
		pass
def transfn(name):
    name = Map.get(name.lower(), name) 
    if isinstance(name, unicode):
        name = name.encode("utf-8")
    fn = os.path.join(name)
    if os.path.exists(fn):
        return fn
    raise Exception("Couldn't find file '%s'." % name)
def main():
	print "[*] UnRPA Version 0.1"
	if len(sys.argv) < 2:
		print "[*] Usage: %s /path/to/data.rpa" % sys.argv[0]
		sys.exit()
	else:
		Path = sys.argv[1]
		if os.path.isfile(Path):
			print "[*] all good, UnRPAing to same directory"
			UnRPA(Path,os.path.dirname(Path)+"/UnRPA")
		else:
			print "[*] '%s' Needs to be a file " % Path
			print "[*] Usage: %s /path/to/data.rpa" % sys.argv[0]
			sys.exit()

if __name__ == "__main__":
	main()