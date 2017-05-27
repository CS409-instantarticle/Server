
from dep import *
from request_list import *

# 크롤링 테스트

# ignore original files
t = False 


flag = True
i = 0

while flag:
	for j in request_list(i):
		try:
			j.write()
		except IOError:
			if t: flag = False
	print(i)
	i = i + 1
print("Done")
