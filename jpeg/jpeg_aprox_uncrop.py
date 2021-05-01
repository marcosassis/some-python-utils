# jpeg lossless (aprox.) crop and "uncrop" using jpegtran
# with workaround to 9d version to make "reflect" or "flatten" effects also on y axis / height
# 
# use with this version of the jpegtran executable:
# Independent JPEG Group's JPEGTRAN, version 9d  12-Jan-2020
# 
# uncrop options:
#	gray wipe: 	''	# no mod
#	flatten:	'f'	# same as force modifier (why?)
#	reflect:	'r'	
# 
# you can use the same options to the height modifier!
# this interface offers special uncrop options
# it transposes the image twice to do so, so be aware of time implications...
#
# ("uncrop" means the width or height parameters are larger than the source image)

import jpegtran_run as jtran
import jpeg_get_size as jsize

def jpeg_aprox_uncrop(in_path, out_path, w, h, x, y, w_mod='', h_mod='', opt_list=jtran._defaul_options):
	in_w, in_h = jsize.jpeg_get_size(in_path)
	
	if h <= in_h or h_mod=='':
		# ok, jpegtran 9d can handle this...
		jtran.jpegtran_crop(in_path, out_path, w, h, x, y, w_mod, h_mod, opt_list)
	else:
		# first we (un)crop the width
		jtran.jpegtran_crop(in_path, out_path, w, in_h, x, 0, w_mod, h_mod if h_mod=='f' else '', opt_list)
		# then we transpose
		jtran.jpegtran_transpose(out_path, out_path, perfect=True, trim=False, opt_list=opt_list)
		# then we uncrop the height
		jtran.jpegtran_crop(out_path, out_path, h, w, y, 0, h_mod, w_mod, opt_list)
		# then we transpose again...
		jtran.jpegtran_transpose(out_path, out_path, perfect=True, trim=False, opt_list=opt_list)

# TODO make commands to minimize jpegtran calls (and compare time)
