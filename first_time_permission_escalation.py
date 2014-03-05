# -*- coding: utf-8 -*-
import sys, getopt, re, os, urllib2, hashlib, datetime

def main():	
	try:
		opts, args = getopt.getopt(sys.argv[1:],'htsr:R:x:i:o:c:', ['test_mode','skip_mode','local_path=','url_path=','exclude_file_type=','ifile=','ofile=','cookie_str='])
	except getopt.GetoptError as err:
		print err
		sys.exit(2)

	ifile = 'dir_list.txt'
	ofile = 'result_' + datetime.datetime.now().strftime("%Y%m%d_%H%M") + '.csv'
	local_path = ''
	url_path = 'http://test.com/'
	exclude_file_type='jpg|JPG|gif|GIF|png|PNG|bmp|BMP|tif|TIF|js|css'
	lines=''
	test_mode = False
	skip_mode =False
	test_mode_limit = 10
	cookie_str = ''
	
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			print '********************************************************************************'
			print 'created by likeway, 2014.'
			print 'usage:'
			print '  first_time_permission_escalation.py [-htrRxioc]'
			print '    -h, --help, read me and help you'
			print '    -t, --test_mode, default test '+str(test_mode_limit)+' requests'
			print '    -s, --skip_mode, default is disbaled,'
			print '    -r, --local_path, example C:\dir\\ or /var/web/ ,default ' + local_path
			print '    -R, --url_path, default is ' +url_path
			print '    -x, --exclude_file_type, default is '+exclude_file_type
			print '    -i, --ifile, default is '+ifile
			print '    -o, --ofile, default is '+ofile
			print '    -c, --cookie_str, example "something=abc;anthoer=123", default is '+cookie_str
			print '********************************************************************************'
			sys.exit()
		elif opt in ('-t', '--test_mode'):
			test_mode = True
		elif opt in ('-s', '--skip_mode'):
			skip_mode =True
		elif opt in ('-r', '--local_path'):
			local_path = arg
		elif opt in ('-R', '--url_path'):
			url_path = arg
		elif opt in ('-x', '--exclude_file_type'):
			exclude_file_type = arg
		elif opt in ('-i', '--ifile'):
			ifile = arg
		elif opt in ('-o', '--ofile'):
			ofile = arg
		elif opt in ('-c', '--cookie_str'):
			cookie_str = arg
	print '********************************************************************************'
	print 'local_path is ' + local_path 
	print 'url_path is ' + url_path
	if url_path.find('https') >= 0:
		exclude_file_type = '^[https].*(' + exclude_file_type + ')$'
	else:
		exclude_file_type = '^[http].*(' + exclude_file_type + ')$'
	print 'exclude file types is ' + exclude_file_type
	print 'ifile is ' + ifile
	print 'ofile is ' + ofile
	print 'cookie is ' + cookie_str
	# if test mode is enabled, process only 50 request 
	if test_mode:
		print 'test mode is enabled, process only '+ str(test_mode_limit) + ' http/https requests'
	else :
		print 'test mode is disabled'
	if skip_mode:
		print 'skip_mode is enabled'
	else :
		print 'skip_mode is disabled'
	print '********************************************************************************'	
	# read input cht soc file list
	fr = open(ifile,'r')
	i = 0
	for line in fr.readlines():
		# if ifile is a csv file, only get the first cell of every line
		line_cell = line.split(',')
		if len(line_cell) > 1:
			url = line_cell[0]
		else :
			url = line
		# replace local file path to url path
		url = url.replace(local_path, url_path)
		# replace windows local file path \ to  /
		url = url.replace('\\','/')
		# remove newline /n
		url = url.rstrip('\n')
		
		# exclude not important file types
		if not re.search(exclude_file_type, url):
			# if skip_mode is enabled, jump to next for loop
			if skip_mode:
				lines = lines + url +'\n'
				continue
			# if test mode is enabled, process only 50 request 
			if test_mode and i >= test_mode_limit:
				break
			else:
				print str(i) + '\r',
			i = i + 1
			
			line_http_body_hash=''
			line_http_body_hash_2=''
			line_http_body_lengh=0
			line_http_body_lengh_2=0
			line_http_code=''
			line_http_code_2=''
			# send http/https request
			try:
				if url.find('https') >= 0:
					opener = urllib2.build_opener(urllib2.HTTPSHandler)
					urllib2.install_opener(opener)
				req = urllib2.Request(url)
				response = urllib2.urlopen(req, None, 3)
				line_http_body = response.read()
				line_http_body_hash = hashlib.new("md5", line_http_body).hexdigest()
				line_http_body_lengh = len(line_http_body)
				line_http_code = response.getcode()
			except urllib2.HTTPError , e:
				compare_result = e
			except urllib2.URLError , e:
				compare_result = e
			except Exception, e:
				compare_result = e
			# set cookies send http request
			if not cookie_str == '':
				try:
					req_2 = urllib2.Request(url)
					req_2.add_header('Cookie', cookie_str)
					response_2 = urllib2.urlopen(req_2, None, 3)
					#print response.info()
					line_http_body_2 = response_2.read()
					line_http_body_hash_2 = hashlib.new("md5", line_http_body_2).hexdigest()	
					line_http_body_lengh_2 = len(line_http_body_2)
					line_http_code_2 = response_2.getcode()
				except urllib2.HTTPError , e:
					compare_result_2 = e
				except urllib2.URLError , e:
					compare_result = e
				except Exception, e:
					compare_result = e
				# hash value comparing 
				compare_result = 'different'
				if line_http_body_hash == line_http_body_hash_2:
					compare_result = 'same'	
			#print column name 
			if i==1:
				lines = lines + 'URL, Hash_1, Response_Length_1, Response_Code_1'
				if not cookie_str == '':
					lines = lines + ', Hash_2, Response_Length_2, Response_Code_2, Hash_Comparison \n'
			#print data row
			lines = lines + url 			
			lines = lines + ',' + line_http_body_hash 
			lines = lines + ',' + str(line_http_body_lengh)
			lines = lines + ',' + str(line_http_code).rstrip('\n')
			if not cookie_str == '':
				lines = lines + ',' + line_http_body_hash_2 
				lines = lines + ',' + str(line_http_body_lengh_2)
				lines = lines + ',' + str(line_http_code_2).rstrip('\n')
				lines = lines + ',' + compare_result
			#print new line
			lines = lines + '\n'
	fr.close()

	# write result to csv file
	fw = open(ofile, "w")
	fw.write(lines)
	fw.close()
	
	print str(i) + ' http requests has been sended.'
	print 'The ouput file is "' + ofile + '".'
	print '********************************************************************************'
	
if __name__ == '__main__':
   main()

