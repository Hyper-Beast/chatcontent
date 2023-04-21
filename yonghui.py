import requests
import json
import time
import os
import re
import sys
from urllib import parse



#76406228-f155-4ac7-a8f2-52070997516b


uid=''
deviceid=''
shopid='9039'


def printf(text):
    print(text)
    sys.stdout.flush()


def load_send():
    global send
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(cur_path)
    if os.path.exists(cur_path + "/sendNotify.py"):
        try:
            from sendNotify import send
        except:
            send=False
            printf("加载通知服务失败~")
    else:
        send=False
        printf("加载通知服务失败~")
load_send()


def gettimestamp():
    t = time.time()
    return str(round(t * 1000))
    

def getaccesstoken():
    global access_token
    try:
        url = f"https://api.yonghuivip.com/web/passport/member/accessToken/775?sign=&uid={uid}&channel=appStore&timestamp={gettimestamp()}&deviceid=&v=7.11.5&access_token="
        headers={
            'Host':'api.yonghuivip.com',
            'Accept':'*/*',
            "X-YH-Biz-Params":"gib=--,0+_'_!_*_,**!**&gvo=_'0-_*+-+,__+!,-*&ncjkdy=,$+,&vmzv=&nzggzmdy=(&xdotdy=!",
            'userKey':'',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-Hans-CN;q=1',
            'Content-Type':'application/json',
            'Content-Length':'83',
            'X-YH-Context':'origin=ios&morse=1',
            'Connection':'keep-alive',
            'DNT':'0',
            'User-Agent':'YhStore/7.11.5(client/phone; iOS 15.1.1; iPhone13,3)'
            }
        with open('yhtoken.txt', 'r') as f:
            refresh_token = f.read()
        data = {"uid": uid, "refresh_token": refresh_token}
        response = requests.post(url=url, headers=headers, json=data)
        json_data = response.json()['data']
        new_refresh_token = json_data.get('refresh_token')
        if new_refresh_token and new_refresh_token != refresh_token:
            with open('yhtoken.txt', 'w') as f:
                f.write(new_refresh_token)
        access_token = json_data['access_token']
    except Exception as e:
        print(f'获取token出错{str(e)}')
        os._exit(0)


def signin():
    url='https://api.yonghuivip.com/web/coupon/signreward/sign?timestamp='+gettimestamp()+'&channel=ios&platform=ios&v=7.11.5.300&app_version=7.11.5.300&brand=iPhone&productLine=YhStore&appType=h5&deviceid='+deviceid+'&shopid='+shopid+'&memberid='+uid+'&access_token='+access_token+'&sign='
    headers={
        'Host':'api.yonghuivip.com',
        'Origin':'https://m.yonghuivip.com',
        'Connection':'keep-alive',
        'Accept':'application/json, text/plain, */*',
        'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 YhStore/7.11.5(client/phone; iOS 15.1.1; iPhone13,3)',
        'Accept-Language':'zh-CN,zh-Hans;q=0.9',
        'Referer':'https://m.yonghuivip.com/',
        'Accept-Encoding':'gzip, deflate, br'
        }
    data='{"memberId":"'+uid+'","shopId":"'+shopid+'","missionid":39}'
    response=requests.post(url=url,headers=headers,data=data).json()
    try:
        printf('签到完成获得'+str(response['data']['signrewardvo']['credit'])+'积分')
        if response['data']['signrewardvo']['couponvos']!=None:
            printf('获得'+str(response['data']['signrewardvo']['couponvos'][0]['orderminamount']/100)+'减'+str(response['data']['signrewardvo']['couponvos'][0]['amount']/100)+'优惠券')
    except:
        printf('日常签到失败:'+str(response))
class Guoyuan:
    def signin():
        url='https://activity.yonghuivip.com/api/web/flow/farm/doTask?timestamp='+gettimestamp()+'&channel=ios&platform=ios&v=7.11.5.300&deviceid='+deviceid+'&shopid='+shopid+'&memberid='+uid+'&app_version=7.11.5.300&brand=iPhone&os=ios&osVersion=15.1.1&productLine=YhStore&appType=h5&access_token='+access_token+'&sign='
        headers={
            'Host':'activity.yonghuivip.com',
            'Content-Type':'application/json',
            'Origin':'https://m.yonghuivip.com',
            'Accept-Encoding':'gzip, deflate, br',
            'Connection':'keep-alive',
            'Accept':'application/json',
            'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 YhStore/7.11.5(client/phone; iOS 15.1.1; iPhone13,3)',
            'Referer':'https://m.yonghuivip.com/',
            'Content-Length':'69',
            'Accept-Language':'zh-CN,zh-Hans;q=0.9'
            }
        data='{"taskType":"sign","activityCode":"HXNC-QG","shopId":"","channel":""}'
        response=requests.post(url=url,headers=headers,data=data)
        printf('永辉果园签到信息:'+str(json.loads(response.text)['data']['signText']))
        time.sleep(1)
    
    
    def gettaskinfo():
        global tasklist
        global aidlist
        global taskidlist
        aidlist=[]
        taskidlist=[]
        tasklist=[]
        temptaskinfo=''
        url = f"https://activity.yonghuivip.com/api/web/flow/farm/task/list?activityCode=HXNC-QG&parentId=280381&access_token={access_token}&timestamp={gettimestamp()}&channel=ios&platform=ios&v=7.11.5.300&deviceid=&shopid={shopid}&memberid={uid}&app_version=7.11.5.300&brand=iPhone&os=ios&osVersion=15.1.1&productLine=YhStore&appType=h5&sign="
        headers={
            'Host':'activity.yonghuivip.com',
            'Origin':'https://m.yonghuivip.com',
            'Connection':'keep-alive',
            'Accept':'application/json, text/plain, */*',
            'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 YhStore/7.11.5(client/phone; iOS 15.1.1; iPhone13,3)',
            'Accept-Language':'zh-CN,zh-Hans;q=0.9',
            'Referer':'https://m.yonghuivip.com/',
            'Accept-Encoding':'gzip, deflate, b'
                }
        response=requests.get(url=url,headers=headers)
        for i in range(len(json.loads(response.text)['data'])):
            if json.loads(response.text)['data'][i]['title'].find('浏览')!=-1:
                try:
                    tasklist.append(json.loads(response.text)['data'][i]['actionUrl'])
                except:
                    pass
        for temptask in tasklist:
            temptask=parse.unquote(temptask).split('&')
            for task in temptask:
                if task.find('aid=')!=-1:
                    aidlist.append(task.replace('aid=',''))
                if task.find('taskid=')!=-1:
                    taskidlist.append(task.replace('taskid=',''))
                    
    def view():
        for i in range(len(aidlist)):
            url='https://api.yonghuivip.com/web/coupon/dailyreward/browse?memberId='+uid+'&sceneValue=4&platform=ios&v=7.11.5.300&channel=4&distinctId=&proportion=3&pagesize=6&networkType=5g&aid='+aidlist[i]+'&appType=h5&os=ios&osVersion=15.4&channelSub=&brand=iPhone&productLine=YhStore&deviceid='+deviceid+'&sellerid=7&shopid='+shopid+'&uid='+uid+'&access_token='+access_token+'&showmultiseller=%7B%227%22:%229039%22%7D&userid='+uid+'&timestamp='+gettimestamp()+'&sign='
            
            data='{"platform":"ios","v":"7.11.5.300","channel":"4","distinctId":"","proportion":3,"screen":"1170*2532","pagesize":6,"networkType":"5g","aid":"'+aidlist[i]+'","appType":"h5","model":"iPhone 12 Pro (A2341/A2406/A2407/A2408)","os":"ios","osVersion":"15.4","channelSub":"","brand":"iPhone","productLine":"YhStore","deviceid":"'+deviceid+'","sellerid":"7","shopid":"'+shopid+'","uid":"'+uid+'","access_token":"'+access_token+'","showmultiseller":"{\\"7\\":\\"9039\\"}","userid":"'+uid+'","pageid":"'+aidlist[i]+'","pid":"280381","taskid":"'+taskidlist[i]+'","sceneValue":"4","memberId":"'+uid+'"}'
            
            headers={
                'Host':'api.yonghuivip.com',
                'Accept':'application/json, text/plain, */*',
                "X-YH-Biz-Params":"gib=--,0+_'_!_*_,**!**&gvo=_'0-_*+-+,__+!,-*&ncjkdy=,$+,&nzggzmdy=(&xdotdy=!",
                'Accept-Language':'zh-CN,zh-Hans;q=0.9',
                'Accept-Encoding':'gzip, deflate, br',
                'Content-Type':'application/json;charset=utf-8',
                'Origin':'https://cmsh5.yonghuivip.com',
                'X-YH-Context':'origin=h5&morse=1',
                'Connection':'keep-alive',
                'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 YhStore/7.11.5(client/phone; iOS 15.4; iPhone13,3)',
                'Referer':'https://cmsh5.yonghuivip.com/',
                'Content-Length':str(len(data))
                    }
            response=requests.post(url=url,headers=headers,data=data).json()
            printf(response['data']['title'])
        printf('------等待15秒后领取奖励------')
    def getaward():
        rewardidlist=[]
        headers={
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Host": "activity.yonghuivip.com",
            "Origin": "https://m.yonghuivip.com",
            "Referer": "https://m.yonghuivip.com/",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 YhStore/7.11.5(client/phone; iOS 15.4; iPhone13,3)"
        }

        
        url='https://activity.yonghuivip.com/api/web/flow/farm/task/list?activityCode=HXNC-QG&parentId=280381&access_token='+access_token+'&timestamp='+gettimestamp()+'&channel=ios&platform=ios&v=7.11.5.300&deviceid='+deviceid+'&shopid='+shopid+'&memberid='+uid+'&app_version=7.11.5.300&brand=iPhone&os=ios&osVersion=15.1.1&productLine=YhStore&appType=h5&sign='
        response=requests.get(url=url,headers=headers)
        for i in range(len(json.loads(response.text)['data'])):
            try:
                rewardidlist.append(json.loads(response.text)['data'][i]['rewardId'])
            except:
                pass
        url='https://activity.yonghuivip.com/api/web/flow/farm/receiveWater?timestamp='+gettimestamp()+'&channel=ios&platform=ios&v=7.11.5.300&sellerid=&deviceid='+deviceid+'&shopid='+shopid+'&memberid='+uid+'&app_version=7.11.5.300&channelSub=&brand=iPhone&model=iPhone%2012%20Pro%20(A2341%2FA2406%2FA2407%2FA2408)&os=ios&osVersion=15.4&networkType=WIFI&screen=390*844&productLine=YhStore&appType=h5&access_token='+access_token+'&sign='
        
        if rewardidlist:
            for i in range(len(aidlist)):
                data={"taskId":taskidlist[i],"id":rewardidlist[i],"taskType":"activityPage","activityCode":"HXNC-QG"}
                try:
                    response=requests.post(url=url,headers=headers,data=json.dumps(data)).json()
                    printf('获得'+str(response['data']['receiveAmount'])+'水滴')
                except:
                    printf(response)
    def waterinfo():
        global wateringtimes
        wateringtimes=0
        url='https://activity.yonghuivip.com/api/web/flow/farm/info?access_token='+access_token+'&timestamp='+gettimestamp()+'&channel=ios&platform=ios&v=2.0.07&deviceid='+deviceid+'&shopid='+shopid+'&memberid='+uid+'&sign='
        headers={
            'Host':'activity.yonghuivip.com',
            'Origin':'https://m.yonghuivip.com',
            'Connection':'keep-alive',
            'Accept':'application/json, text/plain, */*',
            'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 YhStore/7.11.5(client/phone; iOS 15.1.1; iPhone13,3)',
            'Accept-Language':'zh-CN,zh-Hans;q=0.9',
            'Referer':'https://m.yonghuivip.com/',
            'Accept-Encoding':'gzip, deflate, b'
                }
        response=requests.get(url=url,headers=headers)
        printf('当前状态为:'+json.loads(response.text)['data']['ladderText'])
        wateringtimes=json.loads(response.text)['data']['memberAmount']/10
        printf('剩余浇水次数为:'+str(int(json.loads(response.text)['data']['memberAmount']/10)))
        if int(wateringtimes)>0:
            printf('-----------开始浇水-----------')
        time.sleep(1)
    
    
    def watering():
        try:
            url='https://activity.yonghuivip.com/api/web/flow/farm/watering?timestamp='+gettimestamp()+'&channel=ios&platform=ios&v=7.11.5.300&deviceid='+deviceid+'&shopid='+shopid+'&memberid='+uid+'&app_version=7.11.5.300&brand=iPhone&os=ios&osVersion=15.1.1&productLine=YhStore&appType=h5&access_token='+access_token+'&sign='
            headers={
                'Host':'activity.yonghuivip.com',
                'Content-Type':'application/json',
                'Origin':'https://m.yonghuivip.com',
                'Accept-Encoding':'gzip, deflate, br',
                'Connection':'keep-alive',
                'Accept':'application/json',
                'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 YhStore/7.11.5(client/phone; iOS 15.1.1; iPhone13,3)',
                'Referer':'https://m.yonghuivip.com/',
                'Content-Length':'87',
                'Accept-Language':'zh-CN,zh-Hans;q=0.9'
                }
            data='{"activityCode":"HXNC-QG","shopId":"","channel":"","inviteTicket":"","inviteShopId":""}'
            for i in range(int(wateringtimes)):
                response=requests.post(url=url,headers=headers,data=data)
                printf(f'第{i+1}浇水返回信息:'+str(json.loads(response.text)['data']['ladderText']))
                time.sleep(1)
        except:
            printf(str(json.loads(response.text)['message']))
            time.sleep(1)

getaccesstoken()
printf('======开始日常签到======')
signin()
printf('======开始果园签到======')
Guoyuan.signin()
printf('======去做果园任务======')
Guoyuan.gettaskinfo()
Guoyuan.view()
time.sleep(16)
Guoyuan.getaward()
printf('======开始果树浇水======')
Guoyuan.waterinfo()
Guoyuan.watering()