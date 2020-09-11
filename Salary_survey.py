import tkinter
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
#import sample

import requests
from bs4 import BeautifulSoup
import urllib
from pathlib import Path
import time
import csv
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException







yamaguchi = ["S35501", "S35502", "S35503", "S35504", "S35505", "S35506", "S35507", "S35508", "S35509", "S35510", "S35511", "S35512", "S35513", "S35514"]
yamaguchi_j = ["山口市", "萩市", "宇部市", "下関市", "岩国市", "山口県その他", "防府市", "下松市", "光市", "長門市", "柳井市", "美祢市", "周南市", "山陽小野田市"]
okayama = ["M13200", "S35201", "S35213", "M13212", "S35211", "S35203", "M13204", "S35214", "S35218", "M13221", "S35205", "S35207", "S35216", "S35206", "M13215", "S35208", "S35210"]
okayama_j = ["岡山市", "北区", "南区", "東区", "中区", "倉敷市", "総社市", "玉野市", "赤磐市", "浅口市", "備前市", "津山市", "井原市", "瀬戸内市", "笠岡市", "新見市", "岡山県その他"]
hiroshima =["M13100", "S35101", "S35103", "S35112", "S35102", "S35113", "S35115", "S35114", "S35111", "S35104", "S35121", "S35122", "S35124", "S35106", "S35117", "S35109", "S35107", "S35118", "S35120", "S35108", "S35110"]
hiroshima_j =["広島市", "中区", "南区", "安佐南区", "西区", "安佐北区", "佐伯区", "安芸区", "東区", "福山市", "東広島市", "廿日市市", "安芸郡", "呉市", "三原市", "尾道市", "三次市", "府中市", "大竹市", "安芸高田市", "広島県その他"]
shimane =["S35402", "S35401", "S35404", "S35408", "S35403", "S35410", "S35409", "S35411", "S35407"]
shimane_j =["出雲市", "松江市", "浜田市", "益田市", "大田市", "江津市", "安来市", "雲南市", "島根県その他"]
tottori =["S35301", "S35305", "S35306", "S35303", "S35307"]
tottori_j = ["鳥取市", "米子市", "境港市", "倉吉市", "鳥取県その他"]

def Search(jyoken, display_num):
    for timei in jyoken:
        print(timei)
        ken = []
        ken_j = []
        if timei == "山口":
            ken = yamaguchi
            ken_j = yamaguchi_j
        elif timei == "岡山":
            ken = okayama
            ken_j = okayama_j
        elif timei == "広島":
            ken = hiroshima
            ken_j = hiroshima_j
        elif timei == "島根":
            ken = shimane
            ken_j = shimane_j
        elif timei == "鳥取":
            ken = tottori
            ken_j = tottori_j
        for (area,area_j) in zip(ken,ken_j):
            search_aera = timei+area_j
                
            driver = Open_win(timei)#ウィンドウ開く
                
            driver.execute_script("window.scrollTo(0, 300)")#画面スクロール
                
            flg = Conditions(driver, area)#検索動作

            url = Get_url(driver)#現在のURL取得
                
            Output(url[0], url[1], search_aera, driver, display_num)#csv出力
        
        print(timei + "完了しました．")
    driver.quit()



#ウィンドウ開く
def Open_win(timei):
    driverr = webdriver.Chrome()
    #タウンワーク開く
    url = 'https://townwork.net/?arc=1'
    driverr.get(url)
    time.sleep(1)
    html = requests.get(url)
    #driver.find_element_by_xpath("//input[@type='submit' and @value = '検索する']").click()
    driverr.execute_script("window.scrollTo(0, 300)")
    #県名をクリックさせる
    wait = WebDriverWait(driverr, 20)
    elem = wait.until( expected_conditions.element_to_be_clickable( (By.LINK_TEXT,timei)) )
    elem.click()
    time.sleep(3)
    return driverr

#検索動作
def Conditions(driver, area):
    driver1 = driver
    flg = "true"
    #エリア指定
    areaTag = driver1.find_element_by_css_selector('.area-selectfield.jsc-option-not-required.tw-jsc-area-selectfield')
    area_select = Select(areaTag)
    area_select.select_by_value(area)
    #職種
    occupation = driver1.find_element_by_css_selector('.job-category-selectfield.jsc-option-switcher.jsc-option-not-required.tw-jsc-job-category-selectfield')
    occupation_select = Select(occupation)
    occupation_select.select_by_value("001")
    #給与
    salary = driver.find_element_by_css_selector('.salary-selectfield.jsc-option-switcher.jsc-option-required-root.tw-jsc-salary-category-selectfield')
    salary_select = Select(salary)
    salary_select.select_by_value("01")
    time.sleep(2)
    #アルバイト・パートに☑
    driver1.find_element_by_xpath("//input[@id='part-time-job01']").click()
    driver1.find_element_by_xpath("//input[@id='part-time-job06']").click()
    '''1
    検索ボタン押下
    しかし検索ボタンと同じクラス名のボタンが複数存在．
    同じクラス名の他のボタンは非表示．
    よって，
    同じクラス名のボタン全てに対し，表示の場合押下する処理を行う．
    '''
    for element in driver1.find_elements_by_css_selector('.grd-blue.btn-blue-h43'):
        if element.is_displayed() == True:
            element.click()
            break
    #print(len(driver.find_elements_by_css_selector('.grd-blue.btn-blue-h43')))
    #print("クリックしました")
    '''
    1
    '''
    #職種を選ぶクリック
    wait = WebDriverWait(driver, 20)
    time.sleep(2)
    elem = wait.until( expected_conditions.element_to_be_clickable( (By.LINK_TEXT,"職種を選ぶ")) )
    elem.click()
    time.sleep(3)
    #ファーストフード
    driver.find_element_by_xpath("//input[@id='checkboxfield00106']").click()
    #ファミレスキッチン
    driver.find_element_by_xpath("//input[@id='checkboxfield00110']").click()
    #ファミレスホール
    driver.find_element_by_xpath("//input[@id='checkboxfield00113']").click()
    #うどん
    driver.find_element_by_xpath("//input[@id='checkboxfield00120']").click()
    #選択した条件で絞り込むクリック↓↓
    for element in driver.find_elements_by_css_selector('.grd-blue.btn-blue-h43'):
        if element.is_displayed() == True:
            element.click()
            break
    #print(len(driver.find_elements_by_css_selector('.grd-blue.btn-blue-h43')))
    #print("クリックしました")

    #選択した条件で絞り込むクリック↑↑
    #時給順に並び替え
    time.sleep(2)
    try:
        elem = wait.until( expected_conditions.element_to_be_clickable( (By.LINK_TEXT,"時給順")) )
        elem.click()
    except TimeoutException:
        print("検索結果が０件でした．")
        flg = "false"

    return flg

#現在のURL取得
def Get_url(driver):
    cur_url = driver.current_url
    html = requests.get(cur_url)
    return html, cur_url

#csv出力
def Output(html, url, search_aera, driver, display_num):
    soup = BeautifulSoup(html.content, "html.parser")
    #現在のページからtable要素を抽出
    tables = soup.findAll("table")
    #ファイル名の先頭に市名付与
    csvFile = open(search_aera+"_table.csv", 'wt', encoding = 'utf-8')
    writer = csv.writer(csvFile)
    i = 0 #表示件数とfor文の回転数を比較するためのカウンタ
    writer.writerow([url])#URL出力
    for restaurant in driver.find_elements_by_css_selector('.job-lst-main-contents'):#1店舗分のブロックをrestaurantへ入れる
        for table in tables:#restaurantの中のtable探す．（1件しかないのでfor文いらないが，書き換えるのがめんどくさかった)
            i = i + 1
            if i > display_num:
                break
            #店舗名取得↓
            count = 0;
            for name in driver.find_elements_by_css_selector('.job-lst-main-ttl-txt'):#店舗名をすべて取得する
                count = count + 1
                if count == i:#店舗名がcount個目とi個目の店舗情報（両方ページ全体から見ての話）が一致したとき，店舗情報と店舗名も一致する
                    writer.writerow(["[" + str(i) + "]---------------------------------------------------------------------------------"])
                    writer.writerow([name.text])
                    break
            #店舗名取得↑
            j = 0
            #テーブル（バイト内容）を4つだけ抽出
            #テーブル情報をcsv出力↓↓
            for rows in table.findAll(['tr']):
                csvRow = []
                for cell in rows.findAll(['td']):
                    j = j + 1
                    csvRow.append(cell.get_text())
                    writer.writerow(csvRow)
                    # コマンドラインに出力
                    #print(csvRow)
            #テーブル情報をcsv出力↑↑
    # ファイルを閉じる
    csvFile.close()
    # ウィンドウを閉じる
    driver.quit()
'''
for (area,area_j) in zip(yamaguchi,yamaguchi_j):
    search_aera = "山口県"+area_j
    
    driver = Open_win()#ウィンドウ開く
    
    driver.execute_script("window.scrollTo(0, 300)")#画面スクロール
    
    Conditions(driver)#検索動作

    url = Get_url(driver)#現在のURL取得
    
    Output(url[0], url[1])#csv出力
    
    print(area_j + "完了しました．")
    driver.quit()
'''
def app():
    """ 実行ボタンの動作
    """
    jyoken = []
    if yamaBln.get():
        jyoken.append("山口")
    if okaBln.get():
        jyoken.append("岡山")
    if hiroBln.get():
        jyoken.append("広島")
    if simaBln.get():
        jyoken.append("島根")
    if toriBln.get():
        jyoken.append("鳥取")
    display_num = int(txt.get())
    # 結合実行
    Search(jyoken, display_num)
    # メッセージボックス
    messagebox.showinfo("時給調査", "完了しました。")
    #print("showinfo", res)
    
# メインウィンドウ
main_win = tkinter.Tk()
main_win.title("時給調査")
main_win.geometry("500x500")

# メインフレーム
main_frm = ttk.Frame(main_win)
main_frm.grid(column=0, row=0, sticky=tkinter.NSEW, padx=5, pady=10)

hiroBln = tkinter.BooleanVar()
hiro = tkinter.Checkbutton(main_win,variable = hiroBln, text='広島')
hiro.place(x=50, y=70)
okaBln = tkinter.BooleanVar()
oka = tkinter.Checkbutton(main_win,variable = okaBln, text='岡山')
oka.place(x=150, y=70)
simaBln = tkinter.BooleanVar()
sima = tkinter.Checkbutton(main_win,variable = simaBln, text='島根')
sima.place(x=50, y=100)
toriBln = tkinter.BooleanVar()
tori = tkinter.Checkbutton(main_win,variable = toriBln, text='鳥取')
tori.place(x=150, y=100)
yamaBln = tkinter.BooleanVar()
yama = tkinter.Checkbutton(main_win,variable = yamaBln, text='山口')
yama.place(x=250, y=70)

num = tkinter.Label(text='取得店舗数：')
num.place(x=50, y=150)
txt = tkinter.Entry(width=5)
txt.place(x=150, y=150)
# ウィジェット作成（実行ボタン）
app_btn = ttk.Button(main_frm, text="実行", command=app)

# ウィジェットの配置

#app_btn.grid(column=1, row=2)
app_btn.place(x=200, y=200)
# 配置設定
main_win.columnconfigure(0, weight=1)
main_win.rowconfigure(0, weight=1)
main_frm.columnconfigure(1, weight=1)

main_win.mainloop()


