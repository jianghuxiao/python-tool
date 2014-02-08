import os;

print_line_limit = 0;
is_write_file = True;

#get file line count
def getfilelines(path):
	fp = file(path);
	lines = fp.readlines();
	count = 0;
	for item in lines:
		item = item.lstrip();
		item = item.rstrip();
		if (cmp(item, "") != 0) and \
			(not item.startswith("\/")) and (not item.startswith("*")) and \
			(not item.startswith("#")):
			count = count + 1;
	fp.close();
	return count;
	
#whether is correct file
def isCorrectFile(itempath):
	if (os.path.isfile(itempath)) and( \
	     itempath.endswith(".java") or itempath.endswith(".aidl") \
	     or itempath.endswith(".h") or itempath.endswith(".c") \
	     or itempath.endswith(".cpp") or itempath.endswith(".pl") \
	     or itempath.endswith(".py")): 
		return True;
	else:
		return False;

#whether is correct folder
def isCorrectFolder(path):
	if os.path.isdir(path) and (".svn" not in path) and( \
	     ("include" in path) or ("src" in path) or \
		 ("source" in path)):
	   return True;
	else:
	   return False;
	   
#file operation
class FileOperation:
	fp = -1;
	
	def openfile(self, path):
		if os.path.isdir(path) and is_write_file:
			if path.endswith("\\"):
				path = path + "codetrack.qy";
			else:
				path = path + "\\codetrack.qy";
			os.walk(path);
			self.fp = file(path, "w");
	   
	def write(self, message):
		if self.fp != -1:
			self.fp.write(message);
	   
	def closefile(self):
		if self.fp != -1:
			self.fp.close();

#format out
def outFormat(itemcount, size):
	format = str(itemcount);
	formatlen = size - len(format);
	i = 0;
	while i < formatlen:
		i = i + 1;
		format = format + " ";
	return format;
			
#print content
def printContent(itemcount, filesize, itempath, fo):
	if itemcount > print_line_limit:
		outStr = "linecount: %s  filesize(byte):%s  %s" % (outFormat(itemcount, 5), outFormat(filesize, 7), itempath);
		fo.write(outStr + "\n");
		print outStr;

#listfiles
def listfiles(path, fo):
	linecount = 0;
	filecount = 0;
	filesize = 0;
	if isCorrectFile(path):
		filecount = filecount + 1;
		linecount = linecount + getfilelines(path);
		size = os.path.getsize(path);
		filesize = filesize + size;
	elif os.path.isdir(path):
		filelist = os.listdir(path);
		for item in filelist:
			itempath = path + "\\" + item;
			if isCorrectFile(itempath): #file
				filecount = filecount + 1;
				itemcount = getfilelines(itempath);
				linecount = linecount + itemcount;
				size = os.path.getsize(itempath);
				filesize = filesize + size;
				printContent(itemcount, size, itempath, fo); #print
			elif isCorrectFolder(itempath): #folder
				resp = listfiles(itempath, fo);
				linecount = linecount + resp['linecount'];
				filecount = filecount + resp['filecount'];
				filesize = filesize + resp['filesize'];
	result = {"linecount":linecount, 'filecount':filecount, 'filesize':filesize};
	return result;

#main enter	
prompt = "--------------------------------";
prompt = prompt * 4;
path = raw_input("please input project path: ");
fo = FileOperation();
fo.openfile(path);
fo.write(prompt + "\n");
print prompt;
resp = listfiles(path, fo);
result = "project linecount:%d  |  filesize(byte):%s  |  filecount:%d\n" % (resp['linecount'], resp['filesize'], resp['filecount']);
fo.write(prompt + "\n" + result);
fo.closefile();
print prompt, "\n", result;