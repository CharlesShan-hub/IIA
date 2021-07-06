
a = [0,1,2,3,4,5,6]
b = [0,1,2,3]
c = [a,b,[0,1],[2],[3],[0,1,2,3,4,5]]
def _is_sub_list(x):
	print(x)
	if len(x)<=len(b):
		return False
	return x[:len(b)] == b

print(list(filter(_is_sub_list, c)))