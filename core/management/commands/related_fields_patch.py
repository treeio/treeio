#Django command helper to apply django related fields patch programattically
import django
import os
from subprocess import Popen, PIPE

patch_file = os.path.join(os.path.abspath('.'),'bin','django-related-fields.patch')
dir_to_file_in_need_of_patch = os.path.dirname(django.__file__)
try:
	process = Popen(['patch','-p1'],stdin=PIPE,shell=False,cwd=dir_to_file_in_need_of_patch)
	process.communicate(open(patch_file).read())
	process.kill()
except:
	pass