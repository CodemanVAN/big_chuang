import re
import os
pt=re.compile('''"assets/(.*?)"''')#assets/images/favicon.png  {% static "setps/js/jquery.min.js" %}
name=[]
data=''
with open(r'C:\Users\18249\Desktop\django\raspi\htmls\home.html','r',encoding="utf-8") as f:
    for i in f.readlines():
        a=re.findall(pt,i)
        if a!=[]:
            data+=i.replace("assets/"+a[0],'{% static "home_assets/'+a[0]+'" %}')
        else: data+=i
with open('1.html','w',encoding="utf-8") as f:
    f.write(data)