import requests
from selenium import webdriver
from urllib.request import urlretrieve
import re
import os

#获取含有js生成的html,得到总页数
url="https://blog.csdn.net/ke_yi_"
driver=webdriver.PhantomJS(executable_path='D:\\Program Files\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
driver.get(url)
ht=driver.page_source
patter=re.compile("<li data-page=\"\d+\"")
pageli=patter.findall(ht)
pagecount=len(pageli)

#获取每一页包含的博客url
urllist=[]
print("开始获取url\n")
for i in range(1,pagecount+1):
    print("爬取页面:"+str(i)+"\n")
    u=str(url)+"/article/list/"+str(i)+"?"
    ht=requests.get(u).text
    blog_patter=re.compile("<div class=\"article-item-box csdn-tracking-statistics\" data-articleid=\".+")
    id_res_set=blog_patter.findall(ht)
    for id in id_res_set:
        patter=re.compile("\d+")
        id_1=patter.search(id).group()
        u="https://blog.csdn.net/ke_yi_/article/details/"+id_1
        if id_1=="90266014":
            continue
        urllist.append(u)
        print("获取url:"+u+"")
print("页面爬取完毕\n")
print("博客一共"+str(len(urllist))+"篇\n")


#获取每一篇博客里面的html和图片保存为本地文件
blog_name="ke_yi_\\"
os.makedirs(blog_name)
os.makedirs(blog_name+"_post")#ke_yi_\\123456-->ke_yi_\\_post
os.makedirs(blog_name+"image")
for url in urllist:
    ht=requests.get(url).text
    
    title_patter=re.compile("title-article[^<]+")
    title=re.split(">",title_patter.search(ht).group())[1]

    id_patter=re.compile("\d+")
    id=id_patter.search(url).group()
    
    print("爬取博客《"+title+"》\n")
    
    f=open(blog_name+"_post\\"+id+".md","w",encoding="utf-8")#ke_yi_\\_post\\123456.md
    
    content_patter=re.compile("<div class=\"htmledit_views\" id=\"content_views\">.*",re.S)
    content=content_patter.search(ht).group()
    _content_patter=re.compile("</div>")
    i=_content_patter.search(content).span()[1]+1
    content=content[0:i]
    
    img_patter=re.compile("https://img-blog.csdnimg.cn/[^?|\"]+")#https://img-blog.csdn.net/20180811165858607?
    img_iter=img_patter.finditer(content)

    
    print("《"+title+"》开始下载图片\n")
    for img in img_iter:
        img_url=img.group()
        local_img_name=re.search("\d+",img_url).group()+".png"#获取图片的编号，得到图片的本地名
        content=content.replace(img_url,"..\\image\\"+local_img_name,1)#替换路径987645.png-->..\\image\\987645.png

        local_img_url=blog_name+"image\\"+local_img_name#ke_yi_\\123456\\987654.png-->ke_yi_\\image\\987654.png
        
        print("下载:"+img_url+"于"+local_img_url+"\n")
        urlretrieve(img_url,local_img_url)
    
    title=re.sub(":+"," ",title)
    print("《"+title+"》完成下载图片\n")

    blog_head="---\ntitle: "+title+"\n---\n"
    f.write(blog_head)
    f.write(content)
    f.close()
    print("《"+title+"》完成下载\n")
print("爬取完成\n")


