import requests
from selenium import webdriver
from urllib.request import urlretrieve
import re
import os

url="https://blog.csdn.net/ke_yi_"
driver=webdriver.PhantomJS(executable_path='D:\\Program Files\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
driver.get(url)
#整个html页面
ht=driver.page_source
#获取博客页数
patter=re.compile("<li data-page=\"\d+\"")
pageli=patter.findall(ht)
pagecount=len(pageli)#总页数
#获取每一页博客的url后面的序号
urllist=[]
print("开始获取url\n")
for i in range(1,pagecount+1):
    print("爬取页面:"+str(i)+"\n")
    u=str(url)+"/article/list/"+str(i)+"?"#获取页面
    #driver.get(u)#获取每页html
    #ht=driver.page_source
    ht=requests.get(u).text
    blog_patter=re.compile("<div class=\"article-item-box csdn-tracking-statistics\" data-articleid=\".+")
    id_res_set=blog_patter.findall(ht)
    
    #获取每页面博客url
    for id in id_res_set:
        patter=re.compile("\d+")
        id_1=patter.search(id).group()
        u="https://blog.csdn.net/ke_yi_/article/details/"+id_1
        urllist.append(u)
        print("获取url:"+u+"\n")
print("页面爬取完毕\n")

#保存每一篇博客的html页面并下载每一个页面中的图片

print("博客一共"+str(len(urllist))+"篇\n")
blog_name="ke_yi_\\"
os.makedirs(blog_name)
for url in urllist:
    #driver.get(url)
    #ht=driver.page_source
    ht=requests.get(url).text
    #获取标题作为文件名
    patter=re.compile("title-article[^<]+")
    title=re.split(">",patter.search(ht).group())[1]
    
    print("爬取博客《"+title+"》\n")
    
    os.makedirs(blog_name+title)#创建文件夹
    f=open(blog_name+title+"\\"+title+".html","w",encoding="utf-8")#打开文件
    
    patter=re.compile("<div class=\"htmledit_views\" id=\"content_views\">.*",re.S)
    content=patter.search(ht).group()
    patter=re.compile("</div>")
    i=patter.search(content).span()[1]+1
    content=content[0:i]
    #把content上的图片下载下来替换路径https://img-blog.csdnimg.cn/20190511114500433.png?
    img_patter=re.compile("https://img-blog.csdnimg.cn/[^?|\"]+")
    img_iter=img_patter.finditer(content)
    print("《"+title+"》开始下载图片\n")
    for img in img_iter:
        img_url=img.group()
        local_img_url=re.search("\d+",img_url).group()+".png"
        content=content.replace(img_url,local_img_url)
        print("下载:"+img_url+"于"+local_img_url+"\n")
        urlretrieve(img_url,blog_name+title+"\\"+local_img_url)
    print("《"+title+"》完成下载图片\n")
    f.write(content)
    f.close()
    print("《"+title+"》完成下载\n")
print("爬取完成\n")


