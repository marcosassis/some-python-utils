import sys
sys.path.append('..') # que gamibarra hein
from jpeg import jpeg_aprox_uncrop as juncrop

def jpeg_crop_to_frame(item):
	if getObjectType(item)!="ImageFrame":
		raise Exception("not ImageFrame")
	
	img_path = getImageFile(item)
	offX_pt, offY_pt = getImageOffset(item)
	offX_mm = offX_pt * pt2mm
	offY_mm = offY_pt * pt2mm
	offX_px = round(offX_mm * res_mm)
	offY_px = round(offY_mm * res_mm)
	frame_w_mm, frame_h_mm = getSize(item)
	frame_w_px = round(frame_w_mm * res_mm)
	frame_h_px = round(frame_h_mm * res_mm)
