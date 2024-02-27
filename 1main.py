import json
from multiprocessing.resource_sharer import stop
import re
from unittest import result
import urllib
import urllib.request
import random
from pprint import pprint
from urllib import parse

import requests
import os
import copy
import sys
import io
import time

from requests.models import codes
from requests.adapters import HTTPAdapter, Retry

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
}
OneDriveShareURL = "https://hitote-my.sharepoint.com/:f:/g/personal/kachiya22_hitote_onmicrosoft_com/EukXIUPdJ3FFisviiY35eXwBvXx7ErdkejfidJmVFIyDqQ?e=K8H0Nq"
#OneDriveShareURL = "https://e5freedev001-my.sharepoint.com/:f:/g/personal/thdisc_shared_thdisc_ml/Erj2O4s_cWxPvggi1etis8UB6LLWSuU_jnNuo1RiiiEsww?e=XggaYZ"
#OneDriveShareURL = "https://gitaccuacnz2-my.sharepoint.com/:f:/g/personal/mail_finderacg_com/EheQwACFhe9JuGUn4hlg9esBsKyk5jp9-Iz69kqzLLF5Xw?e=FG7SHh"

aria2Link = "http://localhost:16800/jsonrpc"
aria2Secret = ""

isDownload = True

downloadNum = "173" # 1,2-4,5
#fileCount2 = 3940

fileCount = 0

header = {
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'dnt': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' + str(random.randint(80, 100)) + ' Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.7',
    'service-worker-navigation-preload': 'true',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'iframe',
    'accept-language': 'en-US,en;q=0.6',
}
# "https://gitaccuacnz2-my.sharepoint.com/:f:/g/personal/mail_finderacg_com/EheQwACFhe9JuGUn4hlg9esBsKyk5jp9-Iz69kqzLLF5Xw?e=FG7SHh"
# "https://cokemine-my.sharepoint.com/:f:/g/personal/cokemine_cokemine_onmicrosoft_com/EukJbTMXkhJDrPpNVgZM8oUBmywiHfYgL7TSySrAeokVRw?e=FMaVLz"

def newSession():
    s = requests.session()
    retries = Retry(total=6, backoff_factor=0.1)
    s.mount('http://', HTTPAdapter(max_retries=retries))
    return s


def downloadFiles(originalPath, req, layers, aria2URL, token, num=[0], _id=0, originalDir=""):
    global fileCount
    if req == None:
        req = newSession()
    # print(header)
    if originalDir == "":
        originalDir = getAria2ConfigDir(aria2URL, token)
    reqf = req.get(originalPath, headers=header,proxies=proxies)
    isSharepoint = False
    if "-my" not in originalPath:
        isSharepoint = True

    # f=open()
    '''
    if ',"FirstRow"' not in reqf.text:
        #print("\t"*layers, "这个文件夹没有文件")
        return 0
'''
    filesData = []
    redirectURL = reqf.url
    redirectSplitURL = redirectURL.split("/")
    query = dict(urllib.parse.parse_qsl(
        urllib.parse.urlsplit(redirectURL).query))
    downloadURL = "/".join(redirectSplitURL[:-1])+"/download.aspx?UniqueId="
    if isSharepoint:
        pat = re.search('templateUrl":"(.*?)"', reqf.text)

        downloadURL = pat.group(1)
        downloadURL = urllib.parse.urlparse(downloadURL)
        downloadURL = "{}://{}{}".format(downloadURL.scheme,
                                         downloadURL.netloc, downloadURL.path).split("/")
        downloadURL = "/".join(downloadURL[:-1]) + \
            "/download.aspx?UniqueId="
        # print(downloadURL)

    # print(reqf.headers)

    s2 = urllib.parse.urlparse(redirectURL)
    header["referer"] = redirectURL
    header["cookie"] = reqf.headers["set-cookie"]
    header["authority"] = s2.netloc

    # .replace("-", "%2D")

    # print(dd, [cc])
    headerStr = ""
    for key, value in header.items():
        # print(key+':'+str(value))
        headerStr += key+':'+str(value)+"\n"

    relativeFolder = ""
    rootFolder = query["id"]
    for i in rootFolder.split("/"):
        if isSharepoint:
            if i != "Shared Documents":
                relativeFolder += i+"/"
            else:
                relativeFolder += i
                break
        else:
            if i != "Documents":
                relativeFolder += i+"/"
            else:
                relativeFolder += i
                break
    relativeUrl = parse.quote(relativeFolder).replace(
        "/", "%2F").replace("_", "%5F").replace("-", "%2D")
    rootFolderUrl = parse.quote(rootFolder).replace(
        "/", "%2F").replace("_", "%5F").replace("-", "%2D")

    graphqlVar = '{"query":"query (\n        $listServerRelativeUrl: String!,$renderListDataAsStreamParameters: RenderListDataAsStreamParameters!,$renderListDataAsStreamQueryString: String!\n        )\n      {\n      \n      legacy {\n      \n      renderListDataAsStream(\n      listServerRelativeUrl: $listServerRelativeUrl,\n      parameters: $renderListDataAsStreamParameters,\n      queryString: $renderListDataAsStreamQueryString\n      )\n    }\n      \n      \n  perf {\n    executionTime\n    overheadTime\n    parsingTime\n    queryCount\n    validationTime\n    resolvers {\n      name\n      queryCount\n      resolveTime\n      waitTime\n    }\n  }\n    }","variables":{"listServerRelativeUrl":"%s","renderListDataAsStreamParameters":{"renderOptions":5707527,"allowMultipleValueFilterForTaxonomyFields":true,"addRequiredFields":true,"folderServerRelativeUrl":"%s"},"renderListDataAsStreamQueryString":"@a1=\'%s\'&RootFolder=%s&TryNewExperienceSingle=TRUE"}}' % (relativeFolder, rootFolder, relativeUrl, rootFolderUrl)

    # print(graphqlVar)
    s2 = urllib.parse.urlparse(redirectURL)
    tempHeader = copy.deepcopy(header)
    tempHeader["referer"] = redirectURL
    tempHeader["cookie"] = reqf.headers["set-cookie"]
    tempHeader["authority"] = s2.netloc
    tempHeader["content-type"] = "application/json;odata=verbose"
    # print(redirectSplitURL)

    graphqlReq = req.post(
        "/".join(redirectSplitURL[:-3])+"/_api/v2.1/graphql", data=graphqlVar.encode('utf-8'), headers=tempHeader,proxies=proxies)
    graphqlReq = json.loads(graphqlReq.text)
    # print(graphqlReq)
    if "NextHref" in graphqlReq["data"]["legacy"]["renderListDataAsStream"]["ListData"]:
        nextHref = graphqlReq[
            "data"]["legacy"]["renderListDataAsStream"]["ListData"]["NextHref"]+"&@a1=%s&TryNewExperienceSingle=TRUE" % (
            "%27"+relativeUrl+"%27")
        filesData.extend(graphqlReq[
            "data"]["legacy"]["renderListDataAsStream"]["ListData"]["Row"])
        # print(filesData)

        listViewXml = graphqlReq[
            "data"]["legacy"]["renderListDataAsStream"]["ViewMetadata"]["ListViewXml"]
        renderListDataAsStreamVar = '{"parameters":{"__metadata":{"type":"SP.RenderListDataParameters"},"RenderOptions":1216519,"ViewXml":"%s","AllowMultipleValueFilterForTaxonomyFields":true,"AddRequiredFields":true}}' % (
            listViewXml).replace('"', '\\"')
        # print(renderListDataAsStreamVar, nextHref,1)

        # print(listViewXml)

        graphqlReq = req.post(
            "/".join(redirectSplitURL[:-3])+"/_api/web/GetListUsingPath(DecodedUrl=@a1)/RenderListDataAsStream"+nextHref, data=renderListDataAsStreamVar.encode('utf-8'), headers=tempHeader,proxies=proxies)
        graphqlReq = json.loads(graphqlReq.text)
        # print(graphqlReq)

        while "NextHref" in graphqlReq["ListData"]:
            nextHref = graphqlReq["ListData"]["NextHref"]+"&@a1=%s&TryNewExperienceSingle=TRUE" % (
                "%27"+relativeUrl+"%27")
            filesData.extend(graphqlReq["ListData"]["Row"])
            graphqlReq = req.post(
                "/".join(redirectSplitURL[:-3])+"/_api/web/GetListUsingPath(DecodedUrl=@a1)/RenderListDataAsStream"+nextHref, data=renderListDataAsStreamVar.encode('utf-8'), headers=tempHeader,proxies=proxies)
            # print(graphqlReq.text)
            graphqlReq = json.loads(graphqlReq.text)
            # print(graphqlReq)
        filesData.extend(graphqlReq["ListData"]["Row"])
    else:
        filesData.extend(graphqlReq[
            "data"]["legacy"]["renderListDataAsStream"]["ListData"]["Row"])
    print("lenof filedata",len(filesData))
    print(filesData[1])
    stop
    #print(filesData)##filesData是list
    

    # fileCount = 0
    for i in filesData:
        if i['FSObjType'] == "1":
            #print("\t"*layers, "文件夹：",
                #  i['FileLeafRef'], "\t独特ID：", i["UniqueId"], "正在进入")
            _query = query.copy()
            _query['id'] = os.path.join(
                _query['id'],  i['FileLeafRef']).replace("\\", "/")
            if not isSharepoint:
                originalPath = "/".join(redirectSplitURL[:-1]) + \
                    "/onedrive.aspx?" + urllib.parse.urlencode(_query)
            else:
                originalPath = "/".join(redirectSplitURL[:-1]) + \
                    "/AllItems.aspx?" + urllib.parse.urlencode(_query)
            
            time.sleep(5)
            downloadFiles(originalPath, req, layers+1,
                          aria2URL, token, num=num, _id=fileCount, originalDir=originalDir)
            # fileCount += downloadFiles(originalPath, req, layers+1,
            #                            aria2URL, token, num=num, _id=fileCount, originalDir=originalDir)
        else:
            fileCount += 1
            #print(num)
            
            if num == [0] or (isinstance(num, list) and fileCount in num):
                #print("\t"*layers, "文件 [%d]：%s\t独特ID：%s\t正在推送" %
                 #     (fileCount, i['FileLeafRef'],  i["UniqueId"]))
                cc = downloadURL+(i["UniqueId"][1:-1].lower())
                dd = dict(out=i["FileLeafRef"],  header=headerStr, dir=originalDir+str(
                    query['id']).split('Documents', 1)[1])
                jsonreq = json.dumps({'jsonrpc': '2.0', 'id': 'qwer',
                                      'method': 'aria2.addUri',
                                      "params": ["token:"+token, [cc], dd]})
                temp2 = jsonreq
                entryname = i["FileRef"].replace("/personal/kachiya22_hitote_onmicrosoft_com/Documents/00001-14000/","")
                #print ("entryname=",entryname)
                #print ("typeofentryname=",type(entryname))
                entrysize = i["File_x0020_Size"]
                #print ("entrysize=",entrysize)
                #print ("typeofentrysize=",type(entrysize))
                #print("entrydisksize=",entrydisksize)
                #print("typeofentrydisksize=",type(entrydisksize))
                if os.path.exists("/home/md1/downloadtemp/00001-14000/"+entryname):

                    if int(entrysize) == os.path.getsize("/home/md1/downloadtemp/00001-14000/"+entryname) :
                        print(fileCount,"same!!")
                    else:
                        print(fileCount,"nosame...  :(")
                        c = requests.post(aria2URL, data=jsonreq)##开始下载
                    #time.sleep(1)
                    #print(json.loads(c.text))
                        temp1 = json.loads(c.text)["result"]
                    
                        while True:
                            
                            jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
                                'method':'aria2.tellStatus',
                                'params':[temp1]})
                            b = requests.post(aria2URL, data=jsonreq)#拿id
                            #print(temp1)
                            ##判断是否
                            if json.loads(b.text)["result"]["status"] == "complete" and json.loads(b.text)["result"]["totalLength"] != "570":
                                #print("break")
                                #print (type(json.loads(b.text)["result"]["totalLength"]))
                                time.sleep(1)
                                break   
                            else:
                                if json.loads(b.text)["result"]["status"] == "complete":
                                    print("boooooooooooom!!!!!!!!!!!!")
                                    time.sleep(3600000)
                                if json.loads(b.text)["result"]["status"] == "error":
                                    time.sleep(200)
                                    jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
                                'method':'aria2.remove',
                                'params':[temp1]})
                                    c = requests.post(aria2URL, data=jsonreq)
                                    m = requests.post(aria2URL, data=temp2)
                                    temp1 = json.loads(m.text)["result"]

                                
                            time.sleep(0.01)
                else:
                    c = requests.post(aria2URL, data=jsonreq)##开始下载
                    #time.sleep(1)
                    #print(json.loads(c.text))
                    temp1 = json.loads(c.text)["result"]
                
                    while True:
                        
                        jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
                            'method':'aria2.tellStatus',
                            'params':[temp1]})
                        b = requests.post(aria2URL, data=jsonreq)#拿id
                        #print(temp1)
                        ##判断是否
                        if json.loads(b.text)["result"]["status"] == "complete" and json.loads(b.text)["result"]["totalLength"] != "570":
                            #print("break")
                            #print (type(json.loads(b.text)["result"]["totalLength"]))
                            time.sleep(1)
                            break   
                        else:
                            if json.loads(b.text)["result"]["status"] == "complete":
                                print("boooooooooooom!!!!!!!!!!!!")
                                time.sleep(3600000)
                            if json.loads(b.text)["result"]["status"] == "error":
                                time.sleep(200)
                                jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
                            'method':'aria2.remove',
                            'params':[temp1]})
                                c = requests.post(aria2URL, data=jsonreq)
                                m = requests.post(aria2URL, data=temp2)
                                temp1 = json.loads(m.text)["result"]

                            
                        time.sleep(0.01)
                        
                    print("num=",num)
                #time.sleep(0.1)
                #pprint(json.loads(c.text))
                
                # exit(0)
            #else:
                #print("\t"*layers, "文件 [%d]：%s\t独特ID：%s\t非目标文件" %
                      #(fileCount, i['FileLeafRef'],  i["UniqueId"])

                #c = requests.post(aria2URL, data=jsonreq)##开始下载
                #time.sleep(1)
                #print(json.loads(c.text))
                #temp1 = json.loads(c.text)["result"]
                """
                while True:
                    
                    jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
                        'method':'aria2.tellStatus',
                        'params':[temp1]})
                    b = requests.post(aria2URL, data=jsonreq)#拿id
                    #print(temp1)
                    ##判断是否
                    if json.loads(b.text)["result"]["status"] == "complete" and json.loads(b.text)["result"]["totalLength"] != "570":
                        #print("break")
                        #print (type(json.loads(b.text)["result"]["totalLength"]))
                        time.sleep(1)
                        break   
                    else:
                        if json.loads(b.text)["result"]["status"] == "complete":
                            print("boooooooooooom!!!!!!!!!!!!")
                            time.sleep(3600000)
                        if json.loads(b.text)["result"]["status"] == "error":
                            time.sleep(200)
                            jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
                        'method':'aria2.remove',
                        'params':[temp1]})
                            c = requests.post(aria2URL, data=jsonreq)
                            m = requests.post(aria2URL, data=temp2)
                            temp1 = json.loads(m.text)["result"]

                        
                    time.sleep(0.01)
                    
                print("num=",num)
                #time.sleep(0.1)
                #pprint(json.loads(c.text))
                
                # exit(0)
            #else:
                #print("\t"*layers, "文件 [%d]：%s\t独特ID：%s\t非目标文件" %
                      #(fileCount, i['FileLeafRef'],  i["UniqueId"])
"""
    #return fileCount


    

def getFilesHavePwd(originalPath, password):
    req = newSession()
    req.cookies.update(header)
    r = req.get(originalPath,proxies=proxies)
    p = re.search(
        'SideBySideToken" value="(.*?)" />', r.text)
    SideBySideToken = p.group(1)
    p = re.search(
        'id="__VIEWSTATE" value="(.*?)" />', r.text)
    __VIEWSTATE = p.group(1)
    p = re.search(
        'id="__VIEWSTATEGENERATOR" value="(.*?)" />', r.text)
    __VIEWSTATEGENERATOR = p.group(1)
    p = re.search(
        '__EVENTVALIDATION" value="(.*?)" />', r.text)
    __EVENTVALIDATION = p.group(1)
    s2 = parse.urlparse(originalPath)
    redirectURL = originalPath
    redirectSplitURL = redirectURL.split("/")
    shareQuery = s2.path.split("/")[-1]
    redirectSplitURL[-1] = "guestaccess.aspx?"+s2.query+"&share="+shareQuery
    pwdURL = "/".join(redirectSplitURL)
    #print(pwdURL, r.headers)
    hewHeader = {
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'dnt': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        "connection": "keep-alive",
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        "host": s2.netloc,
        "origin": s2.scheme+"://"+s2.netloc,
        "Referer": originalPath,
        'sec-ch-ua-mobile': '?0',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',

    }

    req.cookies.update(header,proxies=proxies)
    r = req.post(pwdURL, data={
        "__EVENTTARGET": "btnSubmitPassword",
        "__EVENTARGUMENT": None,
        "SideBySideToken": SideBySideToken,
        "__VIEWSTATE": __VIEWSTATE,
        "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
        "__VIEWSTATEENCRYPTED": None,
        "__EVENTVALIDATION": __EVENTVALIDATION,
        "txtPassword": password
    }, headers=hewHeader, allow_redirects=False)
    #print(r.headers, r.text)
    new_url = r.headers["Location"]

    r = req.get(new_url,
                headers=r.headers, allow_redirects=False)
    #print(r.headers, r.text)


def wildcardsMatchFiles(text):
    fileNum = []
    data = text.split(",")
    for v in data:
        i = v.split("-")
        if len(i) < 2:
            fileNum.append(int(i[0]))
        else:
            for j in range(int(i[0]), int(i[1])+1):
                fileNum.append(j)
    # print(fileNum)
    fileNum = list(set(fileNum))
    return sorted(fileNum)


def getAria2ConfigDir(aria2URL, token):
    jsonreq = json.dumps({'jsonrpc': '2.0', 'id': 'qwer',
                          'method': 'aria2.getGlobalOption', "params": ["token:"+token]})
    c = requests.post(aria2URL, data=jsonreq)
    return json.loads(c.text)["result"]["dir"]


if __name__ == "__main__":
    datelist=[]
    
    if isDownload:
        #datelist = getdatalist(OneDriveShareURL, None, 0, aria2Link,
                    #  aria2Secret, num=wildcardsMatchFiles(downloadNum))
        #print("date的长度:",len(datelist))
        #for i in range(fileCount2,len(datelist)):
            
        #print("正在推送第",i,"文件")
        #downloadFiles(datelist[i], None, 0, aria2Link,
                 #   aria2Secret, num=wildcardsMatchFiles(downloadNum))
        downloadFiles(OneDriveShareURL, None, 0, aria2Link,
        aria2Secret, num=wildcardsMatchFiles(downloadNum))
        time.sleep(5)
        
        
        #print(datelist)

    
    # getFilesHavePwd(
    #   "https://jia666-my.sharepoint.com/:f:/g/personal/1025_xkx_me/EsqNMFlDoyZKt-RGcsI1F2EB6AiQMBIpQM4Ka247KkyOQw?e=oC1y7r&guestaccesstoken=xyz", "xkx")
