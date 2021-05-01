# jpeg lossless (aprox.) crop using jpegtran

import subprocess

_defaul_options = ["-progressive", "-copy", "all"] # -optimize can go here

def jpegtran_run(in_path, out_path, par_list, opt_list=_defaul_options):
	cmd_list = ["jpegtran", "-outfile", out_path]
	cmd_list.extend(opt_list)
	cmd_list.extend(par_list)
	cmd_list.append(in_path)
	result = subprocess.run(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	print(result.stdout.decode('utf-8'))
	print(result.stderr.decode('utf-8'))

def jpegtran_crop_cmd(w, h, x, y, w_mod='', h_mod=''):
	return ["-crop","{}{}x{}{}+{}+{}".format(w, w_mod, h, h_mod, abs(x), abs(y))]

def jpegtran_transpose_cmd(perfect=True, trim=False):
	par_list = ["-transpose"]
	if perfect: par_list.append("-perfect")
	if trim: par_list.append("-trim")
	return par_list

def jpegtran_crop_flatten_cmd(w, h, x, y):
	par_list = jpegtran_crop_cmd(w, h, x, y, 'f')
	par_list.extend(jpegtran_transpose_cmd(True,False))

def jpegtran_crop(in_path, out_path, w, h, x, y, w_mod='', h_mod='', opt_list=_defaul_options):
	jpegtran_run(in_path, out_path, jpegtran_crop_cmd(w, h, x, y, w_mod, h_mod), opt_list)

def jpegtran_transpose(in_path, out_path, perfect=True, trim=False, opt_list=_defaul_options):
	jpegtran_run(in_path, out_path, jpegtran_transpose_cmd(perfect, trim), opt_list)

