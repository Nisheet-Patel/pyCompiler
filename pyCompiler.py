import os
from shutil import copyfile
from py_compile import compile

try:
	os.mkdir("dict")
	print("[Folder] dict ")
except: pass


FOLDER_TO_IGNORE = [".vscode", "dict", "__pycache__"]
FILE_TO_IGNORE = []

def is_pyfile(file) -> bool:
	if str(file).split(".")[-1:][0].lower() == 'py':
		return True
	return False


# All Folders into dict folder 
print("\nCreate Folder to dict : ")
def mkdir_tree(path):

	_, dirnames, filenames = next(os.walk(path))

	for dirr in dirnames:

		if dirr in FOLDER_TO_IGNORE:
			continue

		pathh = os.path.join(path, dirr)

		# make folder
		cwd = os.getcwd()
		temp_path = pathh

		''' 
		*\\A -> *\\dict\\A
		'''
		temp_path = "dict" + temp_path.removeprefix(cwd)

		try:
			os.mkdir(os.path.join(cwd, temp_path))
			print("[ + ] ",os.path.join(cwd, temp_path))
		except: pass

		mkdir_tree(pathh)


def dir_compile(path, ignore_files=[]):
	print("\n[ ! ] CWPath : ", path)
	_, dirnames, filenames = next(os.walk(path))

	cwd = os.getcwd()

	for filee in filenames:
		temp_path = path

		'''
		*\\A\\main.py
		*\\dict\\A\\main.py
		'''
		destination = os.path.join(cwd, "dict{}".format(
			temp_path.removeprefix(cwd)), filee)

		if filee in ignore_files:
			copyfile(os.path.join(path, filee), destination)
			continue
			
		if is_pyfile(filee):
			compile(os.path.join(path,filee),
					cfile=(destination+"c"))
			print("[ Compile ] file : ",filee)
		else:
			copyfile(
				os.path.join(path,filee),
				destination)
			print("[ Copy ] file : ",filee)
			
	for dirr in dirnames:
		if dirr in FOLDER_TO_IGNORE:
			continue	

		dir_compile(os.path.join(path,dirr))

path = os.getcwd()
mkdir_tree(path)
dir_compile(path, FILE_TO_IGNORE)
