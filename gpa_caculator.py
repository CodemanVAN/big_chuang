xuefen = [4, 3.5, 1, 0.5, 4.5, 2.0, 1, 2, 1, 3]
jidian = [2, 2.7, 4, 4, 2, 3.8, 4, 1.7, 1.4, 2.4]
total = sum(xuefen)
gpa = 0
if len(xuefen) != len(jidian):
    print('学科数目与输入数目不等')
    exit(0)
while xuefen != []:
    gpa += xuefen.pop()/total*jidian.pop()
print(gpa)
