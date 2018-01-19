#-*-encoding:utf-8-*-
import requests
import re
from bs4 import BeautifulSoup
from prettytable import PrettyTable

def main():
      class jiaowu():

            session = requests.Session()
            userId=""   # 学号
            password="" # 密码

            def __init__(self):
                  self.login()

            ### 一系列重定向后获取登录url ###
            def getLoginUrl(self):       
                  #获取重定向地址
                  print("正在进入主页(登陆页)...")
                  indexUrl="http://jw2005.scuteo.com"
                  req1=self.session.head(indexUrl,allow_redirects=False)
                  req1.encoding="gb2312"
                  locUrl1=indexUrl + req1.headers["location"]

                  req2=self.session.head(locUrl1,allow_redirects=False)
                  locUrl2=req2.headers["location"]

                  req3 = self.session.head(locUrl2,allow_redirects=False)
                  loginUrl = locUrl2.split("/default2.aspx")[0] + req3.headers["location"]
                  return loginUrl

            ### 登录 ###
            def login(self):  
                  #获取登录页面
                  loginUrl = self.getLoginUrl()
                  mark=loginUrl.split("(")[1].split(")")[0]

                  req4=self.session.get(loginUrl)
                  req4.encoding="gb2312"

                  soup=BeautifulSoup(req4.text,"html.parser")
                  a_input=soup.select("#form1 > input")
                  __VIEWSTATE=a_input[0]["value"]       #获取验证__VIEWSTATE

                  #下载验证码，并输入验证码
                  codeUrl=loginUrl.replace("default2.aspx","CheckCode.aspx")       #验证码url
                  req5=self.session.get(codeUrl)
                  pic="checkcode.jpg"
                  fp=open(pic,"wb")
                  fp.write(req5.content)
                  fp.close()
                  while(1):
                        checkcode=input("请输入验证码(输入0换验证码):")
                        if(checkcode=="0"):
                              req5=self.session.get(codeUrl)
                              pic="checkcode.jpg"
                              fp=open(pic,"wb")
                              fp.write(req5.content)
                              fp.close()
                        else:
                              #post登录
                              print("正在登录...")
                              postUrl=loginUrl
                              payload={
                                    "__VIEWSTATE":__VIEWSTATE,
                                    "txtUserName":self.userId,
                                    "TextBox2":self.password,
                                    "txtSecretCode":checkcode,
                                    "RadioButtonList1":"学生",
                                    "Button1":"",
                                    "lbLanguage":"",
                                    "hidPdrs":"",
                                    "hidsc":""
                              }
                              headers={
                                    "Referer":postUrl
                              }

                              req6=self.session.post(postUrl,data=payload,headers=headers,allow_redirects=True)
                              mainUrl=req6.url
                              return_data = req6.text

                              #判断登录是否成功
                              if('验证码不正确' in return_data):
                                    print("验证码错误，请重新输入...")
                              elif('密码错误' in return_data):
                                    print("密码错误，请先更正密码再重新运行...")
                                    return
                              elif('用户名不存在或未按照要求参加教学活动' in return_data):
                                    print("不存在该学号，请先更正学号再重新运行...")
                                    return
                              else:
                                    print("登陆成功...")
                                    break
                                    

                  soup=BeautifulSoup(req6.text,"html.parser")
                  a_list=soup.select(".sub > li > a")
                  count=1

                  print("功能如下:")
                  for a in a_list:
                        print(count,a.text)
                        count+=1

                  while(1):
                        func=input("输入功能编号:")
                        func=int(func)
                        if(func==13):      #个人课表
                              print("正在获取课表...")
                              funcUrl=mainUrl.replace("xs_main.aspx?xh="+self.userId,a_list[func-1]["href"])
                              headers={
                                    "Referer":mainUrl
                              }
                              req8=self.session.get(funcUrl,headers=headers)
                              soup=BeautifulSoup(req8,"html.parser")
                              print(req8.text)
                        elif(func==14):         #成绩
                              print("正在获取成绩...")
                              funcUrl=mainUrl.replace("xs_main.aspx?xh="+self.userId,a_list[func-1]["href"])
                              print(funcUrl)
                              headers={
                                    "Referer":mainUrl
                              }
                     
                              req8=self.session.get(funcUrl,headers=headers)
                              req8.encoding="gb2312"

                              soup=BeautifulSoup(req8.text,"html.parser")
                              all_input=soup.select("input")
                              __VIEWSTATE=all_input[2]["value"]

                              #post获取成绩
                              payload={
                                          "__EVENTTARGET":"",
                                          "__EVENTARGUMENT":"",
                                          "__VIEWSTATE":__VIEWSTATE,
                                          "hidLanguage":"",
                                          "ddlXN":"",
                                          "ddlXQ":"",
                                          "ddl_kcxz":"",
                                          "btn_zcj":"%C0%FA%C4%EA%B3%C9%BC%A8"
                                    }
                              req9=self.session.post(funcUrl,data=payload,headers=headers)
                              html = BeautifulSoup(req9.text,'html.parser')
                              trs = html.select('#Datagrid1 tr')
                              table = PrettyTable(['学年','学期','课程名称','课程性质','学分','绩点','成绩',' 排名'])
                              table.padding_width = 2
                              for i in range(1,len(trs)):
                                    tds = trs[i].select('td')
                                    table.add_row([tds[0].text,tds[1].text,tds[3].text,\
                                                tds[4].text,tds[6].text,tds[7].text,tds[8].text,tds[15].text])
                              print(table)
                        else:
                              print("暂只有功能13、14...")

      jiaowu = jiaowu()

if __name__ == '__main__':
      main()