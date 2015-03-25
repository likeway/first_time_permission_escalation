# coding=UTF-8
import sys, getopt, re, os, urllib2, hashlib, datetime
from optparse import OptionParser
outcsv="dir_list_" + datetime.datetime.now().strftime("%Y%m%d_%H%M") + ".csv"
options = OptionParser(usage="%prog dir_list.txt [options]", version="%prog 20150324", description="input dir_list.txt ,then \n"
"(1)replace path with url,\n"
"(2)exclude file type, \n"
"(3)request url with/without cookie, \n"
"(4)output csv list. \n"
"ex: dir_list.py dir_list.txt -p \"/var/web/\" -u \"http://test.com/\" -c \"jessionid=xoxo\"")
options.add_option("-o", "--out", type="string", default=outcsv, help="output csv(default: " + outcsv + ")")
options.add_option("-d", "--demo", action="store_true", help="50 reuqest (default: disable)")
options.add_option("-s", "--skip", action="store_true", help="replace keyword only, no request  (default: disable)")
options.add_option("-p", "--path", type="string", help="path keyword C:\dir\\ or /var/web/")
options.add_option("-u", "--url", type="string", help="target url http://test.com/")
options.add_option("-e", "--exclu", type="string", default="jpg|JPG|gif|GIF|png|PNG|bmp|BMP|tif|TIF|css|db", help="exclude file type(default: jpg|JPG|gif|GIF|png|PNG|bmp|BMP|tif|TIF|css)")
options.add_option("-c", "--coo", type="string", help="permission escalation need cookie")
	
def run_url(ifile,ofile,demo_mode,skip_mode,local_path,url_path,exclude_file_type,cookie_str):
	# read input cht soc file list
	fr = open(ifile,"r")
	i = 0
	lines=""
	lines_dir=""
	for url in fr.readlines():	
		# exclude not important file types
		if re.search(exclude_file_type, url) >= 0:
			continue
		
		# replace local file path to url path
		if local_path:
			url = url.replace(local_path, url_path)
			# replace windows local file path \ to  /
			url = url.replace("\\","/")
		# remove newline /n
		url = url.rstrip("\n")
		
		extstr = re.search("\.\w{1,15}$", url)
		extstr_tmp=""
		if extstr:
			extstr_tmp = extstr.group()
		# if skip_mode is enabled, jump to next for loop
		if skip_mode:
			lines = lines + url + "," + extstr_tmp+ "\n"
			continue
		
		# if demo_mode is enabled, process only 50 request 
		if demo_mode and i >= 50:
			break
		
		print str(i) + "\r",
		i += 1
		line_http_body_hash=""
		line_http_body_hash_2=""
		line_http_body_lengh=0
		line_http_body_lengh_2=0
		line_http_code=""
		line_http_code_2=""
		# send http/https request
		try:
			if url.find("https") >= 0:
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
		#print column name 
		if i==1:
			lines = "URL, Ext, Hash_1, Response_Length_1, Response_Code_1 \n"
			if not cookie_str == "":
				lines = "URL, Ext, Hash_1, Response_Length_1, Response_Code_1, Hash_2, Response_Length_2, Response_Code_2, Hash_Comparison \n"
		#print data row
		lines = lines + url.rstrip("\n")
		lines = lines + "," + extstr_tmp
		lines = lines + "," + line_http_body_hash 
		lines = lines + "," + str(line_http_body_lengh)
		lines = lines + "," + str(line_http_code).rstrip("\n")
		
		# set cookies send http request
		if not cookie_str == "":
			try:
				req_2 = urllib2.Request(url)
				req_2.add_header("Cookie", cookie_str)
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
			compare_result = "different"
			if line_http_body_hash == line_http_body_hash_2:
				compare_result = "same"	
			lines = lines + "," + line_http_body_hash_2 
			lines = lines + "," + str(line_http_body_lengh_2)
			lines = lines + "," + str(line_http_code_2).rstrip("\n")
			lines = lines + "," + compare_result
		
		lines = lines + "\n"
	fr.close()
	# write result to csv file
	fw = open(ofile, "w")
	fw.write(lines)
	fw.close()
	print str(i) + " http requests has been sended."
	print "The ouput file is " + ofile
	print "********************************************************************************"	
	
def main():	
	opts, args = options.parse_args()
	options.print_help()
	# stop script if no input
	if len(args) < 1:		
		return
	#run url
	run_url(args[0],opts.out,opts.demo,opts.skip,opts.path,opts.url,opts.xx,opts.coo)

if __name__ == "__main__":
	main()
