import os
import io

def jpeg_parse_file_signature(f):
	b = f.read(10)
	if not b or len(b)<10 or b[0:4]!=b'\xff\xd8\xff\xe0' or b[-4:]!=b'JFIF':
		raise Exception("not a JPEG file")
	
	block_size = b[4]*256+b[5]
	f.seek(block_size+4)

def jpeg_parse_marker(f):
	b = f.read(1)
	if not b or len(b)<1 or b[0]!=0xff:
		raise Exception("error parsing JPEG file")
	
	while b[0]==0xff:
		b = f.read(1)
		if not b or len(b)<1:
			raise Exception("error parsing JPEG file")
	return b[0]
	
def jpeg_jump_block(f):
	b = f.read(2)
	if not b or len(b)<2:
		raise Exception("error parsing JPEG file")
	
	block_size = b[0]*256+b[1]
	if block_size<2:
		raise Exception("error parsing JPEG file")
	
	f.seek(block_size-2,os.SEEK_CUR)

def jpeg_parse_dimensions(f):
	f.seek(3,os.SEEK_CUR)
	b = f.read(4)
	return b[2]*256+b[3], b[0]*256+b[1]

def jpeg_get_size(img_path):
	with io.open(img_path, "rb") as f:
		jpeg_parse_file_signature(f)
		m = jpeg_parse_marker(f)
		while not(m>=0xc0 and m<=0xc3):
			jpeg_jump_block(f)
			m = jpeg_parse_marker(f)
		else:
			w,h = jpeg_parse_dimensions(f)
	return w,h

# TODO tests comparing to: $ identify -format "%w %h" a.jpg
