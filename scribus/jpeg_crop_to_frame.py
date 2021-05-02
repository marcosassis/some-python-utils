# expect all document units in points.
# 

import os
import sys
sys.path.append('/home/marcos/lab/some-python-utils/') # que gamibarra hein
from jpeg import jpeg_aprox_uncrop as juncr

VERBOSE = True
pt2mm = 0.352778

def jpeg_crop_to_frame(item):
	if getObjectType(item)!="ImageFrame":
		raise Exception("not ImageFrame")
	
	img_path = getImageFile(item)
	xres, yres = juncr.jsize.jpeg_get_resolution(img_path)
	
	offX_pt, offY_pt = getImageOffset(item)
	offX_px = round(offX_pt * xres / 72)
	offY_px = round(offY_pt * yres / 72)
	frame_w_pt, frame_h_pt = getSize(item)
	frame_w_px = round(frame_w_pt * xres / 72)
	frame_h_px = round(frame_h_pt * yres / 72)
	
	if VERBOSE:
		print(img_path)
		print("image resolution in PPI: ", xres, yres)
		print("offset from frame in points: ", offX_pt, offY_pt)
		print("offset from frame in milimeters: ", offX_pt * pt2mm, offY_pt * pt2mm)
		print("offset from frame in pixels: ", offX_px, offY_px)
		print("frame size in points: ", frame_w_pt, frame_h_pt)
		print("frame size in milimeters: ", frame_w_pt * pt2mm, frame_h_pt * pt2mm)
		print("frame size in pixels: ", frame_w_px, frame_h_px)
	
	folder, name = os.path.split(img_path)
	out_path = folder + "/crop-to-frame/"+  name
	juncr.jpeg_aprox_uncrop(img_path, out_path, frame_w_px, frame_h_px, -offX_px, -offY_px)

docUnit = scribus.getUnit()
scribus.setUnit(UNIT_PT)
jpeg_crop_to_frame(scribus.getSelectedObject(0))
scribus.setUnit(docUnit)