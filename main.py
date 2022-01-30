import os, time


def sync_data():
    os.chdir("web")
    os.system("git pull")
    if os.path.exists("../vers"):
        os.system("rm -rf ../vers")
        print("Removing old vers directory")
    os.system("mkdir ../vers")
    log = os.popen("git log --pretty=oneline|cut -c 1-8")
    ver_list = log.read().splitlines()[:-33]
    print("Creating vers directory...")
    for ver in ver_list:
        os.system(f"git reset --hard {ver} > /dev/null")
        os.system(f"cp 439916362/朝色泛起之际_.csv ../vers/{ver}.csv > /dev/null")
    print("Done")


def read_data():
    user_count, bar_dict = {}, {}
    csv_list = os.listdir("../vers")
    for csv in csv_list:
        with open(f"../vers/{csv}", "r") as f:
            for line in f:
                line = line.split(",")
                if line[0].isdigit():
                    user_count[line[0]] = line[1]
    for key, value in user_count.items():
        date = time.strftime("%Y-%m-%d", time.localtime(int(value)))
        if date not in bar_dict.keys():
            bar_dict[date] = 1
        else:
            bar_dict[date] += 1
    return bar_dict


def draw_charts(bar_dict):
    xx, yy = [], []
    for i in sorted(bar_dict):
        xx.append(i)
        yy.append(bar_dict[i])

    from pyecharts import options as opts
    from pyecharts.charts import Bar

    bar = (
        Bar()
        .add_xaxis(xx)
        .add_yaxis("", yy, color="#607D8B")
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
            title_opts=opts.TitleOpts(title="朝色每日涨粉", subtitle=""),
            datazoom_opts=[opts.DataZoomOpts()],
        )
    )
    bar.render("../index.html")


if __name__ == "__main__":
    sync_data()
    data = read_data()
    draw_charts(data)
    print("Done")
