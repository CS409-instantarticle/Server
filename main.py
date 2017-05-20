
from dep import *
from request_list import *

# 크롤링 테스트

for i in range(1, 10):
    for j in request_list(i):
        j.write()
    print(i)
print("Done")
