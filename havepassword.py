import os
import asyncio
from main import getFiles, downloadFiles, header,wildcardsMatchFiles
from pprint import pprint


OneDriveShareURL = "https://sj0121gnl-my.sharepoint.cn/:f:/g/personal/jinyang_ipcas_ac_cn/EsaoiIST_95HsflmgEdwxWQBSy_3630AjeB3qWmlnCg8gw?e=Sn9HAN"
OneDriveSharePwd = "tpwDV4"

aria2Link = "http://localhost:6800/jsonrpc"
aria2Secret = ""

isDownload = True
downloadNum = "0"  # 1,2,3,4,5


os.environ['PYPPETEER_HOME'] = os.path.split(os.path.realpath(__file__))[0]
# os.environ['PYPPETEER_DOWNLOAD_HOST'] = "http://npm.taobao.org/mirrors"

from pyppeteer import launch

pheader = {}
url = ""


async def main(iurl, password):
    global pheader, url
    browser = await launch(options={'args': ['--no-sandbox']})
    page = await browser.newPage()
    await page.goto(iurl, {'waitUntil': 'networkidle0'})
    await page.focus("input[id='txtPassword']")
    await page.keyboard.type(password)
    verityElem = await page.querySelector("input[id='btnSubmitPassword']")
    print("密码输入完成，正在跳转")

    await asyncio.gather(
        page.waitForNavigation(),
        verityElem.click(),
    )
    url = await page.evaluate('window.location.href', force_expr=True)
    await page.screenshot({'path': 'example.png'})
    print("正在获取Cookie")
    # print(p.headers, p.url)
    _cookie = await page.cookies()
    pheader = ""
    for __cookie in _cookie:
        coo = "{}={};".format(__cookie.get("name"), __cookie.get("value"))
        pheader += coo
    await browser.close()


def havePwdGetFiles(iurl, password):
    global header
    print("正在启动无头浏览器模拟输入密码")
    asyncio.get_event_loop().run_until_complete(main(iurl, password))
    print("无头浏览器关闭，正在获取文件列表")
    print()
    header['cookie'] = pheader
    print(getFiles(url, None, 0))


def havePwdDownloadFiles(iurl, password, aria2URL, token, num=-1):
    global header
    print("正在启动无头浏览器模拟输入密码")
    asyncio.get_event_loop().run_until_complete(main(iurl, password))
    print("无头浏览器关闭，正在获取文件列表")
    header['cookie'] = pheader
    downloadFiles(url, None, 0, aria2URL, token, num=num)


if __name__ == "__main__":
    if isDownload:
        havePwdDownloadFiles(OneDriveShareURL, OneDriveSharePwd, aria2Link,
                             aria2Secret, num=wildcardsMatchFiles(downloadNum))
    else:
        havePwdGetFiles(OneDriveShareURL, OneDriveSharePwd)
