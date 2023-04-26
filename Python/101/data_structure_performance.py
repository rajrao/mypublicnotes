'''
Building test data with list_size:1000 and search_size:1000....
test data ready
Running baseline...
Base Line: Found: 13 in 0.16529169998830184
List2: Found: 12 8.17% of baseline 91.83% faster     
Dictionary: Found: 12 0.29% of baseline 99.71% faster
set: Found: 12 0.12% of baseline 99.88% faster 
'''
from faker import Faker
from timeit import default_timer as timer
fake = Faker()

list_size = 1000
search_size = 1000

print(f"Building test data with list_size:{list_size} and search_size:{search_size}....")
list = []
dict = {}
set = set()
for i in range(0, list_size):
    name = fake.name()
    list.append(name)
    dict[name] = name
    set.add(name)

search_list = []
for i in range(0, search_size):
    name = fake.name()
    search_list.append(name)
print("test data ready")

print("Running baseline...")
start = timer()
fnd_cnt = 0
for search_name in search_list:
    for name in list:
        if (search_name == name):
            fnd_cnt += 1
list1_time = timer() - start            
print(f"Base Line: Found: {fnd_cnt} in {list1_time}")

start = timer()
fnd_cnt = 0
for search_name in search_list:
    if (search_name in list):
        fnd_cnt += 1
list2_time = timer() - start        
print(f"List2: Found: {fnd_cnt} {(list2_time/list1_time):.2%} of baseline {((list1_time-list2_time)/list1_time):.2%} faster")


start = timer()
fnd_cnt = 0
for search_name in search_list:
    if (search_name in dict):
        fnd_cnt += 1
dict_time = timer() - start        
print(f"Dictionary: Found: {fnd_cnt} {(dict_time/list1_time):.2%} of baseline {((list1_time-dict_time)/list1_time):.2%} faster")

start = timer()
fnd_cnt = 0
for search_name in search_list:
    if (search_name in set):
        fnd_cnt += 1
set_time = timer() - start        
print(f"set: Found: {fnd_cnt} {(set_time/list1_time):.2%} of baseline {((list1_time-set_time)/list1_time):.2%} faster")
