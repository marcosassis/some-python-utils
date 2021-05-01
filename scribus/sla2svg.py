import os
import subprocess

VERBOSE = True

# TODO generalize units and res
res_mm = 47.244094 # 1200dpi
pt2mm = 0.352778

n_pages = pageCount()
doc_path = getDocName()
doc_folder = os.path.dirname(doc_path)
crop_to_frame_folder = doc_folder+"/jpeg_crop_to_frame"

# TODO file dialog?
if os.path.exists(crop_to_frame_folder):
	raise Exception("jpeg_crop directory already exists")
else:
	os.makedirs(crop_to_frame_folder)


def jpegtran_crop_to_frame(img_path, w, h, x, y, force=False, progressive=True):
	
	img_name = os.path.basename(img_path)
	out_path = crop_to_frame_folder + "/" + img_name
	
	cmd_str = "jpegtran -outfile '" + out_path + "' "
	if progressive: cmd_str += "-progressive "
	cmd_str += "-crop "
	cmd_str += str(w) + "f"
	if force: cmd_str += "f"
	cmd_str += "x" + str(h) + "f"
	if force: cmd_str += "f"
	cmd_str += "+" + str(x) + "+" + str(y) + " '" + img_path + "'"
		
	if VERBOSE: print(cmd_str)
	#subprocess.check_output(["jpegtran", cmd_str]).decode('utf-8')
	#subprocess.check_output(["ls", "--version"]).decode('utf-8')
	result = subprocess.run(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	print(result.stdout.decode('utf-8'))
	print(result.stderr.decode('utf-8'))


# check if it is image frame
# check if it is jpg/jpeg


for page in range(1,2):
	gotoPage(page)
	if VERBOSE: print("page",page)
	items = scribus.getPageItems()
	for item in items:
		item = item[0]
		if getObjectType(item)!="ImageFrame": break
		
		img_path = getImageFile(item)
		offX_pt, offY_pt = getImageOffset(item)
		offX_mm = offX_pt * pt2mm
		offY_mm = offY_pt * pt2mm
		offX_px = round(offX_mm * res_mm)
		offY_px = round(offY_mm * res_mm)
		frame_w_mm, frame_h_mm = getSize(item)
		frame_w_px = round(frame_w_mm * res_mm)
		frame_h_px = round(frame_h_mm * res_mm)
		
		if VERBOSE:
			print(img_path)
			print("offset from frame in points: ", offX_pt, offY_pt)
			print("offset from frame in milimeters: ", offX_mm, offY_mm)
			print("offset from frame in pixels: ", offX_px, offY_px)
			print("frame size in milimeters: ", frame_w_mm, frame_h_mm)
			print("frame size in pixels: ", frame_w_px, frame_h_px)
		
		jpegtran_crop_to_frame(img_path, frame_w_px, frame_h_px, offX_px, offY_px)
		
		
		break
		pw_pt, ph_pt = getPageSize()
		
		print(pw, ph)
		print(round(pw*res_mm), round(ph*res_mm))
		
		print(getImageScale(item[0]))
		
		posX, posY = getPosition(item[0])
		print(posX, posY)
		print(round(posX*res_mm), round(posY*res_mm))
		
		cropX = posX*res_mm+offX*res_mm*pt2mm
		cropY = posY*res_mm+offY*res_mm*pt2mm
		print(-round(cropX), -round(cropY))

a="""
for page in range(1,n_pages+1):
	print(page)
	gotoPage(page)
	items = scribus.getPageItems()
	for item in items:
		print(getObjectType(item[0]))
		print(getImageFile(item[0]))
		offX, offY = getImageOffset(item[0])
		print(offX*pt2mm, offY*pt2mm)
		print(round(offX*res_mm*pt2mm), round(offY*res_mm*pt2mm))
		
		pw, ph = getPageSize()
		print(pw, ph)
		print(round(pw*res_mm), round(ph*res_mm))
		
		print(getImageScale(item[0]))
		
		posX, posY = getPosition(item[0])
		print(posX, posY)
		print(round(posX*res_mm), round(posY*res_mm))
		
		cropX = posX*res_mm+offX*res_mm*pt2mm
		cropY = posY*res_mm+offY*res_mm*pt2mm
		print(-round(cropX), -round(cropY))
		
		
		print(getSize(item[0]))



out_file = open(os.path.dirname(os.path.abspath(getDocName()))+"/01.svg",'w')

out_file.writelines('<svg height="150" width="480"><path d="m0 35.5l6.5-13 9.5 14.5 7-13 11.8 19.7 7.7-13.7 7.8 17 9.4-19.3 9.3 19.3 16-29.3 13.3 21.3 14.7-29.3 14.7 32.6 8.6-18.6 10.7 20.6 11.3-24 12 20 7.4-14.6 12 17.3 10-22 8 14 11.3-24 14 26 7.3-13.3 10.7 19.3 12-24.7 9.7 15 10.3-23.3 12 22.3 6.3-9.3 10.4 14 12-29.3 15.6 31.3 7-13.3 10 16.6 13.4-27.3 6.6 10.7 7.7-16.7 9 19.3 7.3-9.3 11.4 19.3 9.3-17.3 13.3 22 10.7-18 8 11.3 11.3-18 11.9 22 3.8-6.8v181.5h-480v-179.5z" fill="#175720"/></svg>')

out_file.close()

"""		