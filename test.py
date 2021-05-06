def prevUrlChecker(urlStr):
    urlList = urlStr.split('/')
    print(urlList)
    if 'favorites' in urlList:
        return 'favorites'
    elif 'tags' in urlList:
        return 'tags', urlList[4]
    else:
        return 'home'

st = "http://127.0.0.1:5000/tags/food/"

print(prevUrlChecker(st)[1])