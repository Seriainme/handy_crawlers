import requests,http.cookiejar
import json
import os,time
import qrcode,tqdm
import tkinter
from tkinter import messagebox
from tkinter import ttk
class biliLogin:
    def QR(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'
        }
        respone = requests.get('http://passport.bilibili.com/qrcode/getLoginUrl').json()
        oauthKey = respone['data']['oauthKey']
        QRimg = qrcode.make('https://passport.bilibili.com/qrcode/h5/login?oauthKey='+oauthKey)
        QRimg.save('loginqr.png','PNG')
        loginroot=tkinter.Tk()
        def conScan():
            messagebox.askokcancel('确认？','请确认已经扫码并确认')
            loginroot.destroy()
        textLabel = tkinter.Label(loginroot,text="请使用bilibili手机版扫描二维码确认",justify=tkinter.LEFT)
        conB=tkinter.Button(loginroot,text='我已扫码并确认',justify=tkinter.LEFT,command=conScan,bg='green')
        conB['width']=100
        conB.pack(side=tkinter.BOTTOM)
        qrshow=tkinter.PhotoImage(file='loginqr.png')
        ScanQrLabel=tkinter.Label(loginroot,image=qrshow)
        textLabel.pack(side=tkinter.LEFT)
        ScanQrLabel.pack(side=tkinter.RIGHT)
        loginroot.mainloop()
        os.remove('loginqr.png')
        while True:
            try:
                auth = requests.post('http://passport.bilibili.com/qrcode/getLoginInfo',headers=headers,data={'oauthKey':oauthKey})
                if auth:
                    if auth.json()['code'] == 0:
                        print('200 OK AUTHED.')
                        with open('login.data','w') as data:
                            data.write(auth.cookies.get('SESSDATA'))
                            return auth.cookies.get('SESSDATA')
                    else:
                        return False
                else:
                    return False
            except:
                print('未登陆，正在退出..')
                messagebox.showerror('error','Plz scan the qr pic')
                exit()
            time.sleep(2)
    def loginData(self):
        if os.path.isfile('login.data'):
            SESSDATA = open('login.data','r').read()
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0','Cookie':'SESSDATA='+SESSDATA}
            user = requests.get('http://api.bilibili.com/nav',headers=headers)
            if user:
                return SESSDATA
            else:
                return 'notlogin'
        else:
            return 'notlogin'
def getVideo(SESSDATA,vid,cid,qn):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Cookie':'SESSDATA=' + SESSDATA,
        'Referer':'https://www.bilibili.com'
    }
    videoInfo = requests.get('http://api.bilibili.com/x/web-interface/view?bvid='+vid,headers=headers).json()
    #print('标题:'+videoInfo['data']['title'])
    #print('needed:'+videoInfo['data']['pages'][2]) #pages 里面是个列表
    videoData = requests.get('http://api.bilibili.com/x/player/playurl?bvid=' + vid + '&cid=' + str(cid) + '&fourk=1' + '&qn=' + qn,headers=headers)
    print('qn: '+qn)
    lista = videoData.json()['data']['durl']
    print('下崽中..')
    for i in lista:
        videoStreamUrl = videoData.json()['data']['durl'][lista.index(i)]['url']
        print('videoStreamUrl: '+videoStreamUrl)
        videoStream = requests.get(videoStreamUrl,headers=headers,stream=True)
        videoSize = int(int(videoStream.headers['Content-Length'])/1024+0.5)
        with open( str(cid)+'P'+str(int()+int())+'.flv','wb+') as video:
            for chunk in tqdm.tqdm(iterable=videoStream.iter_content(1024),total=videoSize,unit='k',desc=None):
                if chunk:
                    video.write(chunk)

        print('转码中...' + str(cid) + str(lista.index(i))+'.mp4')
        os.system('D:/ffmpeg/ffmpeg.exe -i ' +str(cid)+'.flv '+'  ' +str(cid)+ '.mp4')
        os.remove( str(cid)+'.flv ')

def getVideoInfo(SESSDATA,bvid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Cookie':'SESSDATA=' + SESSDATA,
        'Referer':'https://www.bilibili.com'
    }
    videoInfo = requests.get('http://api.bilibili.com/x/web-interface/view?bvid='+bvid,headers=headers).json()
    return videoInfo
def gui(SESSDATA):
    mainGui = tkinter.Tk()
    mainGui.title('大黄出品，必属精品=。=')
    mainGui.geometry('300x500')
    def logoff():
        os.remove('login.data')
        messagebox.showinfo('ok','ok')
        exit()
    b_logoff=tkinter.Button(mainGui,text='删除登录信息',command=logoff,bg='purple')
    b_logoff['width']=250
    b_logoff.pack()
    l1=tkinter.Label(mainGui,text='Plz enter bv number:',bg='green')
    l1.pack()
    l2=tkinter.Label(mainGui,text='choose  the first episode:',bg='yellow')
    l3=tkinter.Label(mainGui,text='choose  the last episode:',bg='red')
    l4=tkinter.Label(mainGui,text='choose clarity:',bg='blue')
    qntips=tkinter.Label(mainGui,text=qntip)
    cid1choose=ttk.Combobox(mainGui)
    cid2choose=ttk.Combobox(mainGui)
    qnchoose=ttk.Combobox(mainGui)
    bvinput=tkinter.Entry(mainGui)
    bvinput['width']=250
    bvinput.pack()
    chooses=[]
    cidlist=[]
    def getdata():
        bvid=bvinput.get()
        if bvid:
            data=getVideoInfo(SESSDATA,bvid)
            videoNumber=data['data']['videos']
            for i in range(1,int(videoNumber+1)):
                chooses.append(str(i))
                cidlist.append(data['data']['pages'][int(i-1)]['cid'])
            cid1choose['value']=chooses
            cid1choose.current(0)
            cid1choose['width']=250
            l2.pack()
            cid1choose.pack()
            l3.pack()
            cid1choose.pack()

            cid2choose['value']=chooses
            cid2choose.current(0)
            cid2choose['width']=250
            l2.pack()
            cid2choose.pack()
            l3.pack()
            cid2choose.pack()
            l4.pack()
            b2.pack()
            b1.pack_forget()
    def getqnlist():
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
            'Cookie':'SESSDATA=' + SESSDATA,
            'Referer':'https://www.bilibili.com'
        }
        choose=cid1choose.get()
        choose2=cid2choose.get()
        if choose and choose2:
         if int(cid1choose.get()) not  in range(1,len(cidlist)+1) or int(cid2choose.get()) not  in range(1,len(cidlist)+1)  :
                messagebox.showerror('Error','输入的页码有误哦，请仔细检查')
         else:

            videoqn=requests.get('https://api.bilibili.com/x/player/playurl?bvid='+bvinput.get()+'&cid='+str(cidlist[int(int(choose)-1)]),headers=headers).json()
            qnlist=videoqn['data']['accept_quality']
            qnchoose['value']=qnlist
            qnchoose['width']=250
            b2.pack_forget()
            qnchoose.pack()
            qntips.pack()
            qnchoose.current(0)
            b3.pack()


    def download():
        choose=qnchoose.get()
        choose2=qnchoose.get()
        print('choose:'+choose)
        bvid=bvinput.get()
        print('bvid:'+bvid)
        print('int(int(cid1choose.get())-1):  '+str(int(int(cid1choose.get())-1)))#cid1choose.get()=1  是输入的值
        cid=str(cidlist[int(int(cid1choose.get())-1)])
        cid_str=[]


        if int(cid1choose.get())>int(cid2choose.get()) :
         messagebox.showerror('哥们你没没睡醒呢？','起始页大于终止页')
        else :
         start_e=int(cid1choose.get())


         for cid_number in range(int(int(cid1choose.get())-1),int(int(cid2choose.get()))):
                cid_str.append(str(cidlist[cid_number]))
         for  z in range(len(cid_str)):
                print('cid_str:'+cid_str[z])
         print(str(len(cid_str)))
         qn=str(qnchoose.get())
         for cid_str_n in range(len(cid_str)):
            cid_str_spec=cid_str[cid_str_n]
            getVideo(SESSDATA,bvid,cid_str_spec,qn)
         exit()
        #commmand 是具体的实现动作，当鼠标进行点击，即运行对应的函数
    b1=tkinter.Button(mainGui,text='Acquire video list',command=getdata)#输入bv号后，点击'Acquire video list'才有下一步界面的显示
    b2=tkinter.Button(mainGui,text='click to choose video clarity ',command=getqnlist,bg='green')
    b3=tkinter.Button(mainGui,text='开始下崽!',command=download)
    b1['width']=250
    b1.pack()
    b2['width']=250
    b3['width']=250
    mainGui.mainloop()

if __name__ == '__main__':

    canlogin=biliLogin().loginData()
    qntip='''    
    代码  值  含义
    16	360P 流畅
    32	480P 清晰
    64	720P 高清（登录）
    74	720P60 高清（大会员）
    80	1080P 高清（登录）
    112	1080P+ 高清（大会员）
    116	1080P60 高清（大会员）
    120	4K 超清（大会员）
    '''
    if not canlogin == 'notlogin':  #canlogin    是 biliLogin().loginData() 所产生的字符串
        SESS=canlogin
        gui(SESSDATA=SESS) #界面展示 notlogin
    else:#if the user logs in
        QRDATA = biliLogin().QR()
        if not QRDATA == False:
            SESS=QRDATA
            gui(SESSDATA=SESS)
