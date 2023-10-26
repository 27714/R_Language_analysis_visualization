#  - * - coding:utf-8 - * -
"""
作者：LENOVO1
日期：2022年12月02日
"""
# https://www.51job.com/lanzhou/

import time

import numpy as np
import pandas as pd
import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By

dr = webdriver.Chrome()


def Crawling(url, w):
    dr.get(url)
    dr.find_element_by_xpath('//*[@id="kwdselectid"]').send_keys('大数据')
    time.sleep(1)
    dr.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div/div[1]/button').click()
    time.sleep(2)
    datas = []
    for i in range(2, w+1):

        element = dr.find_elements(By.XPATH, '//span[@class="jname at"]')
        print(len(element))
        for i in range(1, len(element)):
            data = []
            count = 1
            try:
                # 工作职称
                job = dr.find_elements(By.XPATH, "//span[@class='jname at']")[i].text
                data.append(job)
                print(job)
            except IndexError:
                pass
            try:
                # 发布时间
                timed1 = dr.find_elements(By.XPATH, "//span[@class='time']")[i].text
                data.append(timed1)
                print(timed1)
            except IndexError:
                pass
            try:
                # 待遇或技术
                time_fabu = dr.find_elements(By.XPATH, "//p[@class='tags']/span")[i].text
                data.append(time_fabu)
                print(time_fabu)
            except IndexError:
                pass
            try:
                # 薪资
                salary = dr.find_elements(By.XPATH, "//span[@class='sal']")[i].text
                data.append(salary)
                print(salary)
            except IndexError:
                pass
            try:
                # 相关信息
                degree = dr.find_elements(By.XPATH, "//span[@class='d at']")[i].text
                data.append(degree)
                print(degree)
            except IndexError:
                pass

            datas.append(data)
        dr.find_element_by_xpath('//input[@class="mytxt"]').send_keys(i)
        dr.find_element_by_xpath('//span[@class="jumpPage"]').click()
    print(datas)
    print(len(datas))
    return datas


def save_mysql(datas):
    # 数据库连接
    db = pymysql.connect(host='localhost', user='root',
                         password='', port=3306, db='second')
    # 游标
    print('开始将数据插入mysql数据库中\n')
    cur = db.cursor()
    sql = 'CREATE TABLE job6(id int auto_increment primary key comment' \
          ' "主键ID",工作职称 CHAR(50), 发布时间 CHAR(50),待遇 CHAR(50), 薪资 CHAR(50), 学历 CHAR(50)) ' \
          'CHARSET=utf8 COLLATE utf8_general_ci; '
    cur.execute(sql)
    print("数据表创建成功\n")
    count = 1
    for data in datas:
        data = tuple(data)
        sql = """insert into job6
                   (工作职称, 发布时间,待遇, 薪资, 学历)
                   values
                   (%s, %s,%s, %s, %s)    
               """

        count = count+1
        print(count, "插入成功")
        cur.execute(sql, data)
    cur.close()
    db.commit()
    db.close()
    return "数据保存在demo_db数据库中，请前往查看"


if __name__ == '__main__':
    url = "https://www.51job.com/lanzhou"
    data = Crawling(url,8)
    save_mysql(data)
    dr.close()
    dr.quit()

