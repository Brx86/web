import os, csv, time, requests


def getName(mid):
    userApi = f"https://api.bilibili.com/x/web-interface/card?mid={mid}"
    up = session.get(userApi).json()["data"]
    upName = up["card"]["name"]
    upFans = int(up["follower"])
    if upFans < 250:
        upPages = int(upFans) // 50 + 1
    else:
        upPages = 5
    return upName, upPages


def getFans(mid, i):
    print(f"Page {i+1}...")
    fansApi = f"http://api.bilibili.com/x/relation/followers?vmid={mid}&pn={i+1}"
    return session.get(fansApi).json()["data"]["list"]


def getInfo(u):
    userApi = f"http://api.bilibili.com/x/space/acc/info?mid={u['mid']}&jsonp"
    while 1:
        try:
            ui = session.get(userApi).json()["data"]
            print(f"UID: {u['mid']}\tLevel: {ui['level']}")
            break
        except TypeError:
            print(f"UID: {u['mid']} TypeError!")
            return
        except KeyError:
            print(f"UID: {u['mid']} KeyError!")
            return
    try:
        with open(f"{upMid}/{up[0]}.csv", "a+", encoding="utf-8") as f:
            wCsv = csv.writer(f, lineterminator="\n")
            wCsv.writerow(
                [
                    u["mid"],
                    u["mtime"],
                    u["uname"],
                    u["vip"]["vipType"],
                    ui["level"],
                    ui["sex"],
                    u["sign"].replace("\n", " "),
                ]
            )
    except UnicodeEncodeError:
        print(f'UID: {u["mid"]} UnicodeEncodeError!')


def main():
    global up, upMid, session  # , proxies
    # proxy.times()
    # proxies = proxy.get()
    t0 = time.time()
    session = requests.Session()
    upMid = os.sys.argv[1]
    up = getName(upMid)
    uList, fList = [], []
    if not os.path.exists(upMid):
        os.mkdir(upMid)
    with open(f"{upMid}/{up[0]}.csv", "w+") as f:
        f.write("uid,mtime,uname,vipType,level,sex,sign\n")
    for i in range(up[1]):
        uList.extend(getFans(upMid, i))
    for u in uList:
        getInfo(u)
        time.sleep(1)
    # proxy.times()
    print(f"Cost {time.time()-t0} secs")
    print(f"{up[0]} Finished！")


if __name__ == "__main__":
    main()
