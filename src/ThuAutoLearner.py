from urllib import request
from urllib import parse
from urllib import error
import urllib
import string
import os
from MainHTMLParser import mainHTTPParser
from  NoteListHTMLParser import noteListHTMLParser
from NoteHTMLParser import noteHTTPParser
from HwListHTMLParser import hwListHTMLParser
from HwHTMLParser import hwHTTPParser
from NewDetailParser import newDetailParser
from DlListHTMLParser import dlListHTMLParser
from http import cookiejar
import sys
import json
import time
if(os.path.exists("conf.txt")==False):
    print("conf.txt不存在")
    os.system("pause")
    sys.exit(1)
userid = ""
userpass = ""
rootpath = ""
temp = ""
conffile = open("conf.txt",'r')
while((temp is "") or (temp is "\n")):
    temp = conffile.readline().replace("\n","")
temp = ""
while((userid is "")or(userid is "\n")):
    userid = conffile.readline().replace("\n","")
while((temp is "") or (temp is "\n")):
    temp = conffile.readline().replace("\n","")
temp = ""
while((userpass is "")or(userpass is "\n")):
    userpass = conffile.readline().replace("\n","")
while((temp is "") or (temp is "\n")):
    temp = conffile.readline().replace("\n","")
temp = ""
while((rootpath is "")or(rootpath is "\n")):
    rootpath = conffile.readline().replace("\n","")
if(os.path.exists(rootpath)==False):
    print("目标路径 "+rootpath+" 不存在")
    os.system("pause")
    sys.exit(1)
#登录网络学堂
#data
data = {}
data['userid'] = userid
data['userpass'] = userpass
data['submit1'] = '登录'
data = parse.urlencode(data).encode('utf-8')
#header
header = {}
header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
#http request
loginurl = 'https://learn.tsinghua.edu.cn/MultiLanguage/lesson/teacher/loginteacher.jsp'
loginreq = request.Request(loginurl,data,header)
mainurl = 'http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/MyCourse.jsp?typepage=1'
mainreq = request.Request(mainurl,headers=header)
#cookie opener
cookie = cookiejar.CookieJar()
handler = request.HTTPCookieProcessor(cookie)
opener = request.build_opener(handler)
try:
    opener.open(loginreq)
    response = opener.open(mainreq)
    html = response.read().decode('utf-8')
    if(html==""):
        print("用户名密码错误！")
        os.system("pause")
        sys.exit(1)
    else:
        hp = mainHTTPParser()
        hp.feed(html)
        updatepath = rootpath + 'update.txt'
        if(os.path.isfile(updatepath)):
            os.remove(updatepath)
        update = open(updatepath,"a")
        for lesson in hp.lessons:
            notenum = 1
            hwnum = 1
            filenum = 1
            print(lesson[1])
            if(os.path.exists(rootpath+lesson[1]) == 0):
                os.mkdir(rootpath+lesson[1])
                os.mkdir(rootpath+lesson[1]+'\\作业附件')
            update.write("课程名称："+lesson[1]+'\n\n')
            update.write('***7天内上传的公告：'+'\n\n')
            if(len(lesson[0])>8 or (lesson[0] == '153978')):
                if(len(lesson[0])>8):
                    idend = len(lesson[0])
                    idbegin = lesson[0].find('home')+5
                    lesson[0] = lesson[0][idbegin:idend]
                else:
                    lesson[0]='2017-2018-2-34100254-0'
                #重新登录
                ndata = {}
                ndata['i_user'] = userid
                ndata['i_pass'] = userpass
                ndata = parse.urlencode(ndata).encode('utf-8')
                header = {}
                header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
                loginurl = 'https://id.tsinghua.edu.cn/do/off/ui/auth/login/post/fa8077873a7a80b1cd6b185d5a796617/0?/j_spring_security_thauth_roaming_entry'
                loginreq = request.Request(loginurl,ndata,header)
                opener.open(loginreq)
                #访问新学堂公告
                print("下载公告中……\n")
                note_url = 'http://learn.cic.tsinghua.edu.cn/b/myCourse/notice/listForStudent/'+lesson[0]
                note_req = request.Request(note_url,headers=header)
                note_html = opener.open(note_req).read().decode('utf-8')
                note_json = json.loads(note_html)
                for note in note_json['paginationList']['recordList']:
                    loadtime = time.mktime(time.strptime(note['courseNotice']['regDate'],"%Y-%m-%d"))
                    if(time.time()-loadtime<7*24*3600):
                        print(note['courseNotice']['title']+'\n')
                        update.write(str(notenum)+'.标题:'+note['courseNotice']['title']+'\n'+'发布人:'+note['courseNotice']['owner']+'  发布时间:'+note['courseNotice']['regDate']+'\n')
                        notenum=notenum+1
                        ndp = newDetailParser()
                        ndp.feed(note['courseNotice']['detail'])
                        data = ndp.detail
                        if(data is not None):
                            data = data.replace(u'\xa0',u'')
                            data = data.replace(u'\r',u'')
                            data = data.replace(u'\n',u'')
                            data = data.replace(u'\t',u'')
                            data = data.replace(u' ',u'')
                        else:
                            data = ""
                        update.write('正文：'+data+'\n\n')
                #由于这种方式读取的公告不会将公告状态由未读改为已读，因此需要发送一个“一键已读”的POST
                click_url = 'http://learn.cic.tsinghua.edu.cn/b/myCourse/notice/addStatusforYiDu/'+lesson[0]
                clickdata={}
                clickdata = parse.urlencode(clickdata).encode('utf-8')
                clickreq = request.Request(click_url,clickdata,header)
                opener.open(clickreq)
                #下载新学堂文件
                print("下载文件中……\n")
                download_url = 'http://learn.cic.tsinghua.edu.cn/b/myCourse/tree/getCoursewareTreeData/'+lesson[0]+'/0'
                download_req = request.Request(download_url,headers=header)
                download_html = opener.open(download_req).read().decode('utf-8')
                download_json = json.loads(download_html)
                update.write("***7天内上传的文件："+'\n\n')
                for i in download_json['resultList']:
                    for j in download_json['resultList'][i]['childMapData']:
                        for k in download_json['resultList'][i]['childMapData'][j]['courseCoursewareList']:
                            temp = k['resourcesMappingByFileId']
                            if(os.path.exists(rootpath+lesson[1]+'\\'+temp['fileName'])is not True):
                                print(k['title']+'\n')
                                update.write(str(filenum)+'.文件标题：'+k['title']+'上传时间:'+time.asctime(time.localtime(temp['regDate']))+ ' 大小：'+str(int(temp['fileSize'])/1024)+'KB\n')
                                filenum = filenum+1
                                update.write('文件名称：'+temp['fileName']+'\n')
                                data = k['detail']
                                if(data is not None):
                                    data = data.replace(u'\xa0',u'')
                                    data = data.replace(u'\r',u'')
                                    data = data.replace(u'\n',u'')
                                    data = data.replace(u'\t',u'')
                                    data = data.replace(u' ',u'')
                                else:
                                    data = ""
                                update.write('简要说明：'+data+'\n\n')
                                fileid = temp['fileId']
                                #下载文件和标记已下载
                                file_url = 'http://learn.cic.tsinghua.edu.cn/b/resource/downloadFileStream/'+fileid
                                file_req = request.Request(file_url,headers=header)
                                file_html = opener.open(file_req).read()
                                dlpath = rootpath+lesson[1]+'\\'+temp['fileName']
                                dlpath = dlpath.replace("?","_")
                                dlpath = dlpath.replace("*","_")
                                dlpath = dlpath.replace("<","_")
                                dlpath = dlpath.replace(">","_")
                                dlpath = dlpath.replace("|","_")
                                filecontent = file_html
                                file = open(dlpath,"wb")
                                file.write(filecontent)
                                file.close()
                                mark_url = 'http://learn.cic.tsinghua.edu.cn/b/courseFileAccess/markReadFile/'+temp['fileId']
                                mark_req = request.Request(mark_url,headers=header)
                                response = opener.open(mark_req).read().decode('utf-8')
                            else:
                                regdate = temp['regDate']/1000
                                if(time.time()-regdate<7*24*3600):
                                    update.write(str(filenum)+'.文件标题：'+k['title']+'上传时间:'+time.asctime(time.localtime(temp['regDate']/1000))+ ' 大小：'+str(int(temp['fileSize'])/1024)+'KB\n')
                                    filenum = filenum+1
                                    update.write('文件名称：'+temp['fileName']+'\n')
                                    data = k['detail']
                                    if(data is not None):
                                        data = data.replace(u'\xa0',u'')
                                        data = data.replace(u'\r',u'')
                                        data = data.replace(u'\n',u'')
                                        data = data.replace(u'\t',u'')
                                        data = data.replace(u' ',u'')
                                    else:
                                        data = ""
                                    update.write('简要说明：'+data+'\n\n')
                #提示未提交作业
                print("下载作业中……\n")
                homework_url = 'http://learn.cic.tsinghua.edu.cn/b/myCourse/homework/list4Student/'+lesson[0]+'/0'
                homework_req = request.Request(homework_url,headers=header)
                homework_html = opener.open(homework_req).read().decode('utf-8')
                homework_json = json.loads(homework_html)
                update.write("***未交作业："+'\n\n')
                for homework in homework_json['resultList']:
                    if(homework['courseHomeworkRecord']['status']=="0"):
                        print(homework['courseHomeworkInfo']['title']+'\n')
                        update.write(str(hwnum)+'.作业标题：'+homework['courseHomeworkInfo']['title']+'\n')
                        hwnum = hwnum + 1
                        update.write('发布日期：'+time.asctime( time.localtime(homework['courseHomeworkInfo']['beginDate']/1000))+' 截止日期：'+time.asctime( time.localtime(homework['courseHomeworkInfo']['endDate']/1000)))
                        if(homework['courseHomeworkInfo']['homewkAffix'] is None):
                            update.write(' 无附件\n')
                        else:
                            update.write(' 有附件(已下载至课程对应文件夹)\n')
                            hfilepath = rootpath+lesson[1]+'\\'+'作业附件\\'+homework['courseHomeworkInfo']['homewkAffixFilename']
                            if(os.path.exists(hfilepath)is not True):
                                hfile_url = 'http://learn.cic.tsinghua.edu.cn/b/resource/downloadFileStream/'+homework['courseHomeworkInfo']['homewkAffix']
                                hfile_req = request.Request(hfile_url,headers=header)
                                hfile_html = opener.open(hfile_req).read()
                                hfilepath = hfilepath.replace("?","_")
                                hfilepath = hfilepath.replace("*","_")
                                hfilepath = hfilepath.replace("<","_")
                                hfilepath = hfilepath.replace(">","_")
                                hfilepath = hfilepath.replace("|","_")
                                print(hfilepath)
                                hfile_open = open(hfilepath,"wb")
                                hfile_open.write(hfile_html)
                                hfile_open.close()
                        homewkdetail = homework['courseHomeworkInfo']['detail']
                        data=""
                        if(homewkdetail is not None):
                            hwdetail = newDetailParser()
                            hwdetail.feed(homewkdetail)
                            data = hwdetail.detail
                            data = data.replace(u'\xa0',u'')
                            data = data.replace(u'\r',u'')
                            data = data.replace(u'\n',u'')
                            data = data.replace(u'\t',u'')
                            data = data.replace(u' ',u'')
                        update.write('作业要求：'+data+'\n\n')
                print("ok\n")
                update.write('******************************************************************\n\n')
                continue
            #访问公告
            print("下载公告中……\n")
            note_url = "http://learn.tsinghua.edu.cn/MultiLanguage/public/bbs/getnoteid_student.jsp?course_id="+lesson[0]
            note_req = request.Request(note_url,headers=header)
            note_html = opener.open(note_req).read().decode('utf-8')
            np = noteListHTMLParser()
            np.feed(note_html)
            for note in np.note:
                loadtime = time.mktime(time.strptime(note[3],"%Y-%m-%d"))
                if(time.time()-loadtime<7*24*3600):
                    turl = parse.quote(note[0], safe = string.printable)
                    treq = request.Request(turl,headers=header)
                    thtml = opener.open(treq).read().decode('utf-8')
                    nnp = noteHTTPParser()
                    nnp.feed(thtml)
                    nnp.text = nnp.text.replace(u'\xa0',u' ')
                    nnp.text = nnp.text.replace(u'\r',u' ')
                    nnp.text = nnp.text.replace(u'\n',u' ')
                    print(note[1]+'\n')
                    update.write(str(notenum)+'.标题：'+note[1]+'\n'+'发布人：'+note[2]+'  发布时间：'+note[3]+'\n')
                    notenum = notenum + 1
                    update.write('正文:'+nnp.text+'\n\n')
            #访问未交作业
            print("下载作业中……\n")
            update.write("***未交作业："+'\n\n')
            hw_url = "http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/hom_wk_brw.jsp?course_id="+lesson[0]
            hw_req = request.Request(hw_url,headers=header)
            hw_html = opener.open(hw_req).read().decode('utf-8')
            hwp = hwListHTMLParser()
            hwp.feed(hw_html)
            for hw in hwp.hw:
                if(hw[4]=='尚未提交'):
                    hurl = hw[0]
                    hreq = request.Request(hurl,headers=header)
                    hhtml = opener.open(hreq).read().decode('utf-8')
                    hhwp =  hwHTTPParser()
                    hhwp.feed(hhtml)
                    print(hw[1]+'\n')
                    update.write(str(hwnum)+'.作业标题：'+hw[1]+'\n')
                    hwnum = hwnum + 1
                    update.write('发布日期：'+hw[2]+' 截止日期：'+hw[3])
                    if(hhwp.havefile==1):
                        update.write(' 有附件(已下载至课程对应文件夹)\n')
                        print(hhwp.url)
                        filerequest = request.Request(hhwp.url,headers=header)
                        fileresponse = opener.open(filerequest)
                        file = fileresponse.read()

                        tstr = fileresponse.info()['Content-Disposition']
                        begin = tstr.index("=")+2
                        end = len(tstr)-1
                        filename = tstr[begin:end]
                        filename = filename.encode("iso-8859-1").decode("gbk")
                        filename.replace("?","_")
                        filename.replace("*","_")
                        filename.replace(":","_")
                        filename.replace("\"","_")
                        filename.replace("<","_")
                        filename.replace(">","_")
                        filename.replace("|","_")
                        filename.replace("\\","_")
                        filename.replace("/","_")
                        dlpath = rootpath+lesson[1]+'\\'+'作业附件\\'+filename
                        dlfile = open(dlpath,'wb')
                        dlfile.write(file)
                        dlfile.close()
                    else:
                        update.write(' 无附件\n')
                    update.write('作业要求：'+hhwp.text+'\n\n')
            #访问未下载文件
            print("下载文件中……\n")
            update.write("***7天内上传的文件："+'\n\n')
            dl_url = 'http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/download.jsp?course_id='+lesson[0]
            dl_req = request.Request(dl_url,headers=header)
            dl_html = opener.open(dl_req).read().decode('utf-8')
            dlp = dlListHTMLParser()
            dlp.feed(dl_html)
            for dl in dlp.dl:
                    dlFileRequest = request.Request(dl[0],headers=header)
                    dlFileResponse = opener.open(dlFileRequest)
                    tstr = dlFileResponse.info()['Content-Disposition']
                    begin = tstr.index("=")+2
                    end = len(tstr)-1

                    filename = tstr[begin:end]
                    filename = filename.encode("iso-8859-1").decode("gbk")
                    filename = filename.replace("?","_")
                    filename = filename.replace("*","_")
                    filename = filename.replace(":","_")
                    filename = filename.replace("\"","_")
                    filename = filename.replace("<","_")
                    filename = filename.replace(">","_")
                    filename = filename.replace("|","_")
                    filename = filename.replace("\\","_")
                    filename = filename.replace("/","_")
                    dlpath = rootpath+lesson[1]+'\\'+filename
                    if(os.path.exists(dlpath) is not True):
                        print(dlpath)

                        filecontent = dlFileResponse.read()
                        file = open(dlpath,"wb")
                        file.write(filecontent)
                        file.close()
                        print(dl[1]+'\n')
                        update.write(str(filenum) + '.文件标题：'+dl[1]+' 上传时间：'+dl[4] + '大小：'+dl[3]+'\n')
                        filenum = filenum + 1
                        update.write('简要说明：'+dl[2]+'\n\n')
                    else:
                        loadtime = time.mktime(time.strptime(dl[4],"%Y-%m-%d"))
                        if(time.time()-loadtime<7*24*3600):
                            update.write(str(filenum) + '.文件标题：'+dl[1]+' 上传时间：'+dl[4] + '大小：'+dl[3]+'\n')
                            filenum = filenum + 1
                            update.write('简要说明：'+dl[2]+'\n\n')
            update.write('******************************************************************\n\n')
            print("ok\n")
    update.close()
    os.system("pause")
except error.HTTPError as e:
    print('HTTPError!')
    print(e.code)
    os.system("pause")
except error.URLError as e:
    print('URLError!')
    print(e.reason)
    os.system("pause")
