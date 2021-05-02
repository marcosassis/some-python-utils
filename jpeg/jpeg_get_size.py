# use these:
# jpeg_get_dimensions(img_path)
# jpeg_get_resolution(img_path) # JFIF only

import os
import io

# to check file format
# b = f.read(11) # from the begining
# b[0:4]!=b'\xff\xd8\xff\xe0' or b[-5:]!=b'JFIF\0'

def jpeg_parse_file_signature(f):
	b = f.read(4)
	if not b or len(b)<4 or b[0:3]!=b'\xff\xd8\xff':
		raise Exception("not a JPEG file")
	return b[3]

def jpeg_parse_block_size(f):
	b = f.read(2)
	if not b or len(b)<2:
		raise Exception("error parsing JPEG file")
	return b[0]*256+b[1]

def jpeg_jump_block(f):
	block_size = jpeg_parse_block_size(f)
	if block_size<2:
		raise Exception("error parsing JPEG file")
	f.seek(block_size-2,os.SEEK_CUR)

def jpeg_parse_marker(f):
	b = f.read(1)
	if not b or len(b)<1 or b[0]!=0xff:
		raise Exception("error parsing JPEG file")
	
	while b[0]==0xff:
		b = f.read(1)
		if not b or len(b)<1:
			raise Exception("error parsing JPEG file")
	return b[0]

def jpeg_parse_dimensions(f):
	f.seek(3,os.SEEK_CUR)
	b = f.read(4)
	return b[2]*256+b[3], b[0]*256+b[1]

def jpeg_get_dimensions(img_path):
	with io.open(img_path, "rb") as f:
		jpeg_parse_file_signature(f)
		m = 0
		while not(m>=0xc0 and m<=0xc3):
			jpeg_jump_block(f)
			m = jpeg_parse_marker(f)
		else:
			w,h = jpeg_parse_dimensions(f)
	return w,h

def jpeg_parse_resolution(f):
	if jpeg_parse_file_signature(f) != 0xe0:
		raise Exception("cannot parse non JFIF file yet")
	f.seek(13)
	b = f.read(5)
	return b[0], b[1]*256+b[2], b[3]*256+b[4] # unit, x res, y res

def jpeg_res_in_ppi(unit, xres, yres):
	if unit==0: raise Exception("density units = no units. can't convert to physical size") 
	if unit==1: return xres, yres
	return xres/2.54, yres/2.54

def jpeg_get_resolution(img_path):
	with io.open(img_path, "rb") as f:
		return jpeg_res_in_ppi(*jpeg_parse_resolution(f))

# TODO tests comparing to: $ identify -format "%w %h" a.jpg
