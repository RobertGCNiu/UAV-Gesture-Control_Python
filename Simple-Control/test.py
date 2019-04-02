def cal(x,y):
    r = y^((x^y)&-(x<y))
    return r
for i in range(0,10):
    r = cal(10,i)
    print(r)