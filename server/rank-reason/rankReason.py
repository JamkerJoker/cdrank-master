import requests
import time
import calendar
import json
import os
import re
import csv
import platform

from acount import vf_user,vf_pwd
from UnnormalReasonCount import flight_reason
# flight_reason(CallSign,DepAP,ArrAP,start_day,end_day)
    
'''
更新日志：

2018.9.4
1.账号独立
2.加入OCR登录异常处理

2018.9.5
1.根据Windows或Linux系统，定文件生成路径
2.华东departRate改名normalRate

2018.9.7
1.每次更新前一日数据
2.判断更新昨日数据由当日17点改为不限制

2018.9.8
1.判断更新昨日数据由不限制改为当日5点
（不正常原因模块，加入判断更新昨日数据：17点）
2.登录放到循环中，防止回话意外终止后不能更新数据

2018.9.9
1.因服务器已设置好定时，删除循环
2.前端网页可以识别departRate，华东normalRate改回departRate---（还是改成normalRate）
3.修复Linux系统路径问题

2018.9.12
1-3号,最小航班量改成日期，其他改成4
'''
def get_platform_path():
    if platform.system()=='Windows':
        path=''
    elif platform.system()=='Linux':
        path='/usr/share/nginx/html/data/'
    return path
    
def get_date(month=None):
    now_=time.localtime(time.time())
    now_year=now_.tm_year
    now_month=now_.tm_mon
    now_date=now_.tm_mday
    now_hour=now_.tm_hour
    # print(now_year,now_month,now_date)
    year=now_year
    if not month:
        month=now_month
    elif int(month)>now_month:
        print('输入月有误')
        return None
    if month==now_month:
        if now_date==1:
            # 1号选定日期为上月，最后一天
            month=now_month-1
            max_day=calendar.monthrange(year,month)[1]
            # print('本月数据还未统计，无法获取，查找上月数据')
            if now_hour<5:
                # 1号1700前选定日期为上月，倒数第二天
                max_day=max_day-1
        elif now_date==2:
            # 2号1700前，选定日期为上月最后一天
            if now_hour<5:
                month=now_month-1
                max_day=max_day=calendar.monthrange(year,month)[1]
            else:
                max_day=now_date-1
        else:
            max_day=now_date-1
            if now_hour<5:
                max_day=max_day-1
    else:
        max_day=calendar.monthrange(year,month)[1]
    # print(year,month,max_day)
    return year,month,max_day
        
        
    
def login(n=0):
    login_url='http://fisc.variflight.com/v1/user/login'
    post_data={
    'LoginForm[username]':vf_user,
    'LoginForm[password]':vf_pwd
    }
    login_rep= s.post(url=login_url,headers=headers,data=post_data)
    # print(login_rep.content)
    if login_rep.json()["message"]=='Success':
        print('飞常准登录成功\n')
        token=login_rep.json()["data"]
        return token
    else:
        while n<3:
            n=+1
            return login(n)
    
    # 获取单个机场单个时间段的所有相关航班的排名
def get_airport_day_rank(url,start_day,end_day,airport):
    if end_day[8:] in ['01','02','03']:
        minNumber=int(end_day[8:])
    else:
        minNumber=4
    post_data={
    'airport':airport,
    'flightNumber':'EU',
    'minNumber':minNumber,
    'startDay':start_day,
    'endDay':end_day,
    'cancel':'1',
    }
    # print(post_data)
    rep=s.post(url,headers=headers,data=post_data)
    if rep.status_code==200:
        if rep.json()["message"]=='Success':
            data=rep.json()["data"]
            if type(data)==dict:
                # print(airport,'\n',list(data.values()),'\n')
                return list(data.values())
            elif type(data)==list:
                # print(airport,'\n',data,'\n')
                return data
                
# 添加原因模块，数据处理，筛选排名
def rank_add_reason(url,start_day,end_day,airport):
    new_rank_list=[]
    rank_list=get_airport_day_rank(url,start_day,end_day,airport)
    if rank_list:
        for x in rank_list:
            if x['ranking']<=60: #取排名60以内的数据
                x['startDay']=start_day
                x['endDay']=end_day
                x['flight']=f"{x['fnum']} {x['forg']}-{x['fdst']}"
                del x['planTime']
                del x['plan']
                
                if 'aviation' in url: #仅全国航班统计原因
                    CallSign=x['fnum']
                    DepAP=x['forg']
                    ArrAP=x['fdst']
                    reason=flight_reason(CallSign,DepAP,ArrAP,start_day,end_day)
                    if reason:
                        x.update(reason)
                        new_rank_list.append(x)
                        
                elif 'east' in url: #华东departRate改名normalRate（已恢复）
                    x['normalRate']=x['departRate']
                    del x['departRate']
                    new_rank_list.append(x)
                    
                elif 'attention' in url: #东北地区排名看normalRanking
                    del x['ranking']
                    x['ranking']=x['normalRanking']
                    del x['normalRanking']
                    new_rank_list.append(x)
                    
    # print(new_rank_list)
    return new_rank_list
    
    # 遍历机场
def get_day_rank_list(url,airport_list,start_day,end_day):
    rank_dict={}
    rank_list=[]
    for airport in airport_list:
        # rank=get_airport_day_rank(url,start_day,end_day,airport)
        rank=rank_add_reason(url,start_day,end_day,airport)
        if rank:
            rank_list.append(rank)
    rank_dict[end_day]=rank_list
    # print(rank_list,'\n')
    # print(rank_dict)
    return rank_dict
    
def old_rank(file):
    if os.path.isfile(file):
    # file为之前日期生成的json文件，rank_data为新抓取的数据
        with open(file,'r',encoding='utf-8') as fp:
            old_rank_data=json.load(fp)
            old_rank_date=list(old_rank_data)
        return old_rank_data,old_rank_date
    else:
        return '',''
            
class New_rank():
    '''
    全局变量：
        east_airport,aviation_airport
        rank_token
        year,month,max_day,target_day
    '''
    def __init__(self,tag):
        self.host="http://fisc.variflight.com"
        self.tag=tag
        if tag=='east':
            self.airport_list=east_airport
            self.start_month=str(month-2).zfill(2)# 华东从上上月1号开始统计
        if tag=='aviation':
            self.airport_list=aviation_airport
            self.start_month=str(month).zfill(2)# 全国从当月1号开始统计
        self.url=self.host+"/v1/"+self.tag+"/index?token="+rank_token
        
        if tag=='northeast':
            self.airport_list=northeast_airport
            self.start_month=str(month).zfill(2)# 东北从当月1号开始统计
            self.url=self.host+"/v1/attention/index?token="+rank_token
            
        self.file=platform_path+self.tag+'_rank_list.json'
        self.file_month=platform_path+self.tag+'_month_rank.json'
        self.stop_month=str(month).zfill(2)
        self.start_day=f'{year}-{self.start_month}-01'
        
        
    def get_new_rank(self):
        total_rank_list={}
        # 获取旧数据
        old_rank_data,old_rank_date=old_rank(self.file)
        if old_rank_data:
            total_rank_list.update(old_rank_data)
        # 获取新数据
        for x in range(1,max_day+1):
            y=str(x).zfill(2)
            end_day=f'{year}-{self.stop_month}-{y}'
            if end_day not in old_rank_date:
                print(f'正在下载{end_day}_{self.tag}数据')
                rank_list=get_day_rank_list(self.url,self.airport_list,self.start_day,end_day)
                total_rank_list.update(rank_list)
                
                # 更换前一日数据
                z=str(x-1).zfill(2)
                end_day2=f'{year}-{self.stop_month}-{z}'
                rank_list=get_day_rank_list(self.url,self.airport_list,self.start_day,end_day2)
                total_rank_list.update(rank_list)
                
                with open(self.file,'w',encoding='utf-8') as fp:
                    json.dump(total_rank_list,fp,ensure_ascii=False)
        return total_rank_list
        
    def get_month_rank(self):
        total_rank_list={}
        old_rank_data=old_rank(self.file_month)[0]
        if old_rank_data:
            total_rank_list.update(old_rank_data)
        for m in [month-2,month-1,month]:
            start_date1=f'{year}-{str(m).zfill(2)}-01'
            stop_day1=calendar.monthrange(year,m)[1]
            stop_date1=f'{year}-{str(m).zfill(2)}-{stop_day1}'
            print(f'正在下载{start_date1}_{stop_date1}_{self.tag}数据')
            rank_list=get_day_rank_list(self.url,self.airport_list,start_date1,stop_date1)
            # print(rank_list)
            total_rank_list.update(rank_list)
            with open(self.file_month,'w',encoding='utf-8') as fp:
                json.dump(total_rank_list,fp,ensure_ascii=False)
        
                
s=requests.Session()
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
platform_path=get_platform_path()
aviation_airport=[
"ZBAA","ZSPD","ZGGG","ZUUU","ZPPP","ZGSZ","ZSSS","ZLXY","ZUCK","ZSHC",
"ZSAM","ZSNJ","ZGHA","ZHHH","ZHCC","ZSQD","ZWWW","ZBTJ","ZJHK"]

east_airport=["ZSPD","ZSNJ","ZSHC","ZSAM","ZSQD","ZSFZ"]
northeast_airport=["ZYHB","ZYCC","ZYTX","ZYTL"]
    
if __name__=='__main__':
    rank_token=login()
    if rank_token:
        set_month=''
        # set_month=input('输入需要的月份，不输入则为当月,按回车确认:\n')
        if set_month:
            set_month=int(set_month)
        year,month,max_day=get_date(set_month)
        target_day=f'{year}-{str(month).zfill(2)}-{str(max_day).zfill(2)}'
        print(target_day,'\n')
        east_rank_all=New_rank('east').get_new_rank()
        east_rank_all=New_rank('east').get_month_rank()
        
        aviation_rank_all=New_rank('aviation').get_new_rank()
        
        east_rank_all=New_rank('northeast').get_new_rank()
        east_rank_all=New_rank('northeast').get_month_rank()

        
        
        

    
    
    
