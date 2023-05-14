import requests
import os
import json

maven_urls = {
    "https://repo1.maven.org/maven2/"
}
maven_pkg_path = {
    "com.android.volley:volley:1.2.0"
}


        

#------------------------------------------------------------------
# 下载Maven文件
# @param mavenUrl 仓库地址
# @param pkgPath 包路径，用于创建本地repo仓地址
# @param fileName 文件名称
#------------------------------------------------------------------
def downloadMavenFile(mavenUrl, pkgPath, fileName):
    # print("============ 开始下载文件 >>>>>>> Start")
    # print("============ info start ===========")
    # print("mavenUrl is:", mavenUrl)
    # print("pkgPath is:", pkgPath)
    # print("fileName is:", fileName)
    # print("============ info end ===========")
    
    url = mavenUrl + pkgPath.replace("/", ".") + "/" + fileName
    print(">>> 开始下载：", url)
    file = requests.get(url)
    with open("./" + pkgPath + "/" + fileName, "wb") as bufferWriter:
         bufferWriter.write(file.content)
    isDownloadSuccess = os.path.exists("./" + pkgPath + "/" + fileName)
    if(isDownloadSuccess == True):
        print(url + " ====================== 下载 成功!")
    else:
        print(url + " ====================== 下载 失败!")
    return isDownloadSuccess


#------------------------------------------------------------------
# 下载Maven文件
# @param path创建包路径如com.android.volley
#------------------------------------------------------------------
def makeDirs(path):
    pathArray = path.split(":")
    pkgDir = pathArray[0] = pathArray[0].replace(".", "/")
    # print(">>>>> pkgDir:", pkgDir)
    fileName = pathArray[1]
    # print(">>>>> fileName:", fileName)
    fileVersion = pathArray[2]
    # print(">>>>> fileVersion:", fileVersion)
    isDirExits = os.path.exists(pkgDir)
    if(isDirExits == False):
        os.makedirs(pkgDir)
    return pathArray

#------------------------------------------------------------------
# 主程序 入口函数
#------------------------------------------------------------------
def main() :
    # 解析本地以来Json文件
    with open('maven_list.json', 'rb') as jsonFile:
        jsonData = json.load(jsonFile)
    repo_hosts = jsonData['repo_hosts']
    dependence = jsonData['dependence']    
    for path in dependence:
        pathArray = makeDirs(path)
        for host in repo_hosts:
            pkgDir = pathArray[0]
            fileName = pathArray[1]
            fileVersion = pathArray[2]
            isAARExits = downloadMavenFile(host, pkgDir, fileName + fileVersion + ".aar")
            isPOMExits = downloadMavenFile(host, pkgDir, fileName + fileVersion + ".pom")
            if(isAARExits == True and isPOMExits == True):
                break

main()