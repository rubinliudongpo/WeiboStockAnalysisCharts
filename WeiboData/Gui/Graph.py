#-*- coding:utf-8 -*-

from pyecharts import Kline, Line, Page,Overlap,Bar,Pie,Timeline
from pandas import DataFrame as df
import re
import tushare as ts
import time
import pandas as pd

try:
    xrange          # Python 2
except NameError:
    xrange = range  # Python 3

def calculate_month(data, Daycount):
    sum = 0
    result = list( 0 for x in data)#used to calculate ma. Might be deprecated for future versions
    for i in range(0 , Daycount):
        sum = sum + data[i]
        result[i] = sum/(i+1)
    for i in range(Daycount, len(data)):
        sum = sum - data[i-Daycount]+data[i]
        result[i] = sum/Daycount
    return result


def stock_render_page(stock_id, start_date, end_date, option, width, height):
    page = Page()
    a = generate_stock_line(stock_id, "Kline", start_date, end_date, 'qfq')  # stock number, Type, startdate, enddate, 30 or 15 or days
    if a is None:
        return
    time, open, close, low, high = zip(*a)  # get time from returned
    option = "Kline"
    if option != "Kline":
        if len(time[0]) == 4 and time[0][2] == "bar":  # for 分笔data
            overlap = Overlap()
            form = [e[1] for e in a]
            bar = Bar("分笔", width=width * 10 / 11, height=(height * 10 / 11))
            bar.add("分笔", time, form, yaxis_min="dataMin", yaxis_max="dataMax", is_datazoom_show=True,
                    datazoom_type="slider")
            overlap.add(bar)

            line = Line("price", width=width * 10 / 11, height=(height * 10 / 11))
            price = [e[3] for e in a]
            line.add("price", time, price, yaxis_min="dataMin", yaxis_max="dataMax", is_datazoom_show=True,
                     datazoom_type="slider",
                     yaxis_type="value")
            overlap.add(line, yaxis_index=1, is_add_yaxis=True)

            page.add(overlap)

        if len(a[0]) == 5 and a[0][3] == "pie":
            overlap = Overlap()
            timeline = Timeline(is_auto_play=False, timeline_bottom=0)  # zip(namearray,valuearray,quarter,flag,num)
            namearray = [c[0] for c in a]
            valuearray = [d[1] for d in a]
            quarter = [e[2] for e in a]
            num = a[0][4]

            for x in range(0, num / 10):
                list1 = valuearray[x]
                names = namearray[x]
                quarters = quarter[x][0]

                for idx, val in enumerate(list1):
                    list1[idx] = float(val)

                pie = Pie("前十股东", width=width * 10 / 11, height=(height * 10 / 11))

                pie.add("前十股东", names, list1, radius=[30, 55], is_legend_show=False,
                        is_label_show=True, label_formatter="{b}: {c}\n{d}%")
                # print list
                # print names
                # print quarterarray

                timeline.add(pie, quarters)
                # namearray = [y for y in namearray[x]]
            timeline.render()

            return

            # need more statement
        else:
            form = [e[1] for e in a]  # for not分笔 data
            line = Line("分笔", width=width * 10 / 11, height=(height * 10 / 11))
            line.add("分笔", time, form, is_datazoom_show=True, datazoom_type="slider", yaxis_min="dataMin",
                     yaxis_max="dataMax")
            page.add(line)
    else:
        overlap = Overlap()#for k线
        candle = [open, close, low, high]
        candlestick = Kline("分笔", width=width * 10 / 11, height=(height * 10 / 11))
        candlestick.add("分笔", time, candle, is_datazoom_show=True, datazoom_type="slider", yaxis_interval=1)
        overlap.add(candlestick)
        if len(close) > 10:
            ma10 = calculate_month(close, 10)
            line1 = Line(title_color="#C0C0C0")
            line1.add("MA10", time, ma10)
            overlap.add(line1)
        if len(close) > 20:
            ma20 = calculate_month(close, 20)
            line2 = Line(title_color="#C0C0C0")
            line2.add("MA20", time, ma20)
            overlap.add(line2)
        if len(close) > 30:
            ma30 = calculate_month(close, 30)
            line3 = Line(title_color="#C0C0C0")
            line3.add("MA30", time, ma30)
            overlap.add(line3)
        page.add(overlap)
    page.render()


def generate_stock_line(stock_id, Type, start_date, end_date, interval):
    startdata = start_date.replace("/","-").replace("\n","") #convert to tushare readable date
    enddata = end_date.replace("/","-").replace("\n","")
    current_time = time.strftime("%Y/%m/%d")
    if Type ==  "分笔":
        if start_date!=current_time:
            array = ts.get_tick_data(stock_id, date = startdata)#分笔
            if array is None:
                return
            array = array.sort_values("time")
            date = array["time"].tolist()
            amount = array["amount"].tolist()
            atype = array["type"].tolist()
            price = array["price"].tolist()
            flag = ["bar" for i in date]
            for idx,val in enumerate(atype):#if卖盘，交易变成负数
                if val == "卖盘":
                    amount[idx] = -amount[idx]
                if val == "中性盘":#if中性盘，则忽略. Might have a problem with this part??
                    amount[idx] = 0
            returnarray = zip(date,amount,flag,price)
            return returnarray
        else:
            array = ts.get_today_ticks(stock_id)#Tushare里今日分笔和历史分笔需要分别对待
            if array is None:
                return
            array = array.sort_values("time")
            date = array["time"].tolist()
            amount = array["amount"].tolist()
            atype = array["type"].tolist()
            flag = ["bar" for i in date]
            for idx, val in enumerate(atype):
                if val == "卖盘":
                    amount[idx] = -amount[idx]
                if val == "中性盘":
                    amount[idx] = 0
            returnarray = zip(date, amount, flag)
            return returnarray

    if Type=="季度饼图":
        datestr = start_date.split("/")
        thisyear = datestr[0]
        df2 = ts.top10_holders(code=stock_id, gdtype="1")
        test = df2[1]["quarter"].tolist()
        df_ready = df2[1]
        idxlist = []
        for idx, val in enumerate(test):
            a = val.split("-")
            if a[0] == thisyear:
                # print a[0],idx
                idxlist.append(idx)
        thing = df_ready.loc[idxlist]
        thing = thing.sort_values(["quarter", "name"])
        # print a[0],id
        name = thing["name"].tolist()
        value = thing["hold"].tolist()
        quarter = thing["quarter"].tolist()
        namearray = [name[i:i + 10] for i in xrange(0, len(name), 10)]
        valuearray = [value[j:j + 10] for j in xrange(0, len(value), 10)]
        quarterarray = [quarter[k:k + 10] for k in xrange(0, len(quarter), 10)]

        flag = ["pie" for i in namearray]
        num = [len(value) for k in namearray]
        returnarray = zip(namearray,valuearray,quarterarray,flag,num)
        return returnarray

    if interval!="qfq" and interval!="hfq":
        if interval=="1min" or interval=="5min" or interval=="15min" or interval=="30min" or interval=="60min":
            df = ts.get_tick_data(stock_id, date=startdata)
            df.sort_values("time")
            a = startdata + " " + df["time"]
            df["time"] = a
            df["time"] = pd.to_datetime(a)
            df = df.set_index("time")
            price_df = df["price"].resample(interval).ohlc()
            price_df = price_df.dropna()
            vols = df["volume"].resample(interval).sum() #relevant data processing algorithm taken from Jimmy, Creator of Tushare
            vols = vols.dropna()
            vol_df = pd.DataFrame(vols, columns=["volume"])
            amounts = df["amount"].resample(interval).sum()
            amounts = amounts.dropna()
            amount_df = pd.DataFrame(amounts, columns=["amount"])
            newdf = price_df.merge(vol_df, left_index=True, right_index=True).merge(amount_df, left_index=True,
                                                                                right_index=True)
            if Type != "Kline":
                Type1 = firstletter(Type).encode("ascii")
                target = newdf[Type1].tolist()
                date = newdf.index.format()
                returnarray = zip(date, target)
                return returnarray
            else:
                Date = newdf.index.format()
                Open = newdf["open"].tolist()
                Close = newdf["close"].tolist()
                High = newdf["high"].tolist()
                Low = newdf["low"].tolist()
                Candlestick = zip(*[Date, Open, Close, Low, High])
                return Candlestick

        #正常历史k线
        if Type!="Kline":
            array = ts.get_k_data(stock_id, start=startdata, end=enddata, ktype=interval)
            if array is None:
                return
            Type1 = firstletter(Type).encode("ascii")
            target = array[Type1].tolist()
            date = array["date"].tolist()
            returnarray = zip(date,target)
            return returnarray
        else:
            array = ts.get_k_data(stock_id, start=startdata, end=enddata, ktype=interval)
            if array is None:
                return
            Date = array["date"].tolist()
            Open = array["open"].tolist()
            Close = array["close"].tolist()
            High = array["high"].tolist()
            Low = array["low"].tolist()
            Candlestick = zip(*[Date,Open,Close,Low,High])
            return Candlestick
    else:
        if Type!="Kline": # 复权
            array = ts.get_h_data(stock_id, start = startdata, end = enddata, autype= interval)
            if array is None:
                return
            Type1 = firstletter(Type).encode("ascii")
            array = array.sort_index()
            target = array[Type1].tolist()
            date = array.index.format()
            returnarray = zip(date, target)
            return returnarray
        else :
            array = ts.get_h_data(stock_id, start=startdata, end=enddata, autype=interval)
            if array is None:
                return
            array = array.sort_index()
            Date = array.index.format()
            Open = array["open"].tolist()
            Close = array["close"].tolist()
            High = array["high"].tolist()
            Low = array["low"].tolist()
            # list_array = [Date, Open, Close, Low, High]
            Candlestick = zip(*[Date, Open, Close, Low, High])
            return Candlestick

def Mergegraph(stuff):
    sth = []
    for i in stuff:
        j = re.split("-",i)
        sth.append(j)
    flat_list = [item for sublist in sth for item in sublist]
    return flat_list

def firstletter(argument): #小写第一个字母
    return argument[:1].lower() + argument[1:]

def capfirstletter(argument): #大写第一个字母
    return argument[:1].upper() + argument[1:]
def returnquarter(argument):
    if argument<4:
        return 1
    if argument>=4 and argument <7:
        return 2
    if argument>=7 and argument < 11:
        return 3
    if argument>=11:
        return 4
