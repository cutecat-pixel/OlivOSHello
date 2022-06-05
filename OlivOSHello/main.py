# -*- encoding: utf-8 -*-
'''
   ____     __    _           ____    _____    __  __          __    __
  / __ \   / /   (_) _   __  / __ \  / ___/   / / / /  ___    / /   / /  ____
 / / / /  / /   / / | | / / / / / /  \__ \   / /_/ /  / _ \  / /   / /  / __ \
/ /_/ /  / /   / /  | |/ / / /_/ /  ___/ /  / __  /  /  __/ / /   / /  / /_/ /
\____/  /_/   /_/   |___/  \____/  /____/  /_/ /_/   \___/ /_/   /_/   \____/
@File      :   OlivOSHello.main.py
@Author    :   Cute_CAT
@Contact   :   2971504919@qq.com
'''
import random
import OlivOS
import OlivOSHello
import pymysql
from datetime import date

DBHOST = 'localhost'
DBUSER = 'root'
DBPASS = '123456'
DBNAME = 'Hello_data'

replyOfsex = ['少年', '少女']

class Event(object):
    def init(plugin_event, Proc):
        while True:
            try:
                sql_base = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS)
                cur = sql_base.cursor()
                cur.execute("CREATE DATABASE IF NOT EXISTS `Hello_data`")
                sql_base.commit()
                sql_base.close()
                sql_base = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)
                cur = sql_base.cursor()
                cur.execute('CREATE TABLE IF NOT EXISTS `Hellos`(`Hello_cnt` INT, `User_date` VARCHAR(20))')
                cur.execute('CREATE TABLE IF NOT EXISTS `Hellos_user`(`User_id` VARCHAR(20), `User_date` VARCHAR(20), `User_sta` INT)')
                sql_base.close()
                break
            except pymysql.Error as e:
                print(str(e))

    def private_message(plugin_event, Proc):
        unity_reply(plugin_event, Proc)

    def group_message(plugin_event, Proc):
        unity_reply(plugin_event, Proc)

    def save(plugin_event, Proc):
        pass

def deleteBlank(str):
    str_list = list(filter(None,str.split(" ")))
    return str_list

def Hello_count():
    hellocnt = 0
    try:
        sql_base = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)
        cur = sql_base.cursor()
        sql_check = "SELECT * FROM `Hellos`"
        cur.execute(sql_check)
        hello = cur.fetchone()
        if hello == None:
            try:
                sqlCha = "INSERT INTO `Hellos` (`Hello_cnt`, `User_date`) VALUE (%s,%s)"
                v = (1, str(date.today()))
                cur.execute(sqlCha, v)
                sql_base.commit()
                hellocnt = 1
            except pymysql.Error as e:
                print(e)
                sql_base.rollback()
        else:
            if hello[1] != str(date.today()):
                try:
                    sql_up = "UPDATE `Hellos` SET `Hello_cnt`=%s, `User_date`=%s"
                    va = (1, str(date.today()))
                    cur.execute(sql_up, va)
                    sql_base.commit()
                    hellocnt = 1
                except pymysql.Error as e:
                    print(e)
                    sql_base.rollback()
            else:
                try:
                    sql_up = "UPDATE `Hellos` SET `Hello_cnt`=%s"
                    va = (hello[0] + 1)
                    cur.execute(sql_up, va)
                    sql_base.commit()
                    hellocnt = hello[0] + 1
                except pymysql.Error as e:
                    print(e)
                    sql_base.rollback()
        sql_base.close()
        return hellocnt
    except pymysql.Error as e:
        print(e)

def unity_reply(plugin_event, Proc):
    command_list = deleteBlank(plugin_event.data.message)
    if command_list[0] == '早安':
        try:
            sql_base = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)
            cur = sql_base.cursor()
            sql_use = "SELECT * FROM `Hellos_user` WHERE `User_id`=%s"
            cur.execute(sql_use, plugin_event.data.user_id)
            user = cur.fetchone()
            if user == None:
                try:
                    sqlCha = "INSERT INTO `Hellos_user` (`User_id`, `User_date`, `User_sta`) VALUE (%s,%s,%s)"
                    val = (plugin_event.data.user_id, str(date.today()), 1)
                    cur.execute(sqlCha, val)
                    sql_base.commit()
                    plugin_event.reply(plugin_event.data.sender['name'] + '早上好喵~\n' + '你是今天第' + str(Hello_count()) + '个起床的' + random.choice(replyOfsex))
                    sql_base.close()
                except pymysql.Error as e:
                    print(e)
            elif user[1] != str(date.today()):
                try:
                    sqlCha = "UPDATE `Hellos_user` SET `User_date`=%s, `User_sta`=%s WHERE `User_id`=%s"
                    val = (str(date.today()), 1, plugin_event.data.user_id)
                    cur.execute(sqlCha, val)
                    sql_base.commit()
                    plugin_event.reply(plugin_event.data.sender['name'] + '早上好喵~\n' + '你是今天第' + str(Hello_count()) + '个起床的' + random.choice(replyOfsex))
                    sql_base.close()
                except pymysql.Error as e:
                    print(e)
            elif user[2] == 1:
                try:
                    plugin_event.reply('你不是起床了吗(/= _ =)/~┴——┴')
                finally:
                    sql_base.close()
            elif user[2] == 0:
                try:
                    plugin_event.reply('你不是睡了吗(/= _ =)/~┴——┴，今天不许起床了')
                finally:
                    sql_base.close()
        except pymysql.Error as e:
            print(e)
    elif command_list[0] == '晚安':
        try:
            sql_base = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)
            cur = sql_base.cursor()
            sql_use = "SELECT * FROM `Hellos_user` WHERE `User_id`=%s"
            cur.execute(sql_use, plugin_event.data.user_id)
            user = cur.fetchone()
            if user == None:
                try:
                    sqlCha = "INSERT INTO `Hellos_user` (`User_id`, `User_date`, `User_sta`) VALUE (%s,%s,%s)"
                    val = (plugin_event.data.user_id, str(date.today()), 0)
                    cur.execute(sqlCha, val)
                    sql_base.commit()
                    plugin_event.reply(plugin_event.data.sender['name'] + "晚安喵~")
                    sql_base.close()
                except pymysql.Error as e:
                    print(e)
            elif user[1] != str(date.today()) or (user[2] == 0 and user[1] == str(date.today())):
                try:
                    plugin_event.reply('睡死你得了(/= _ =)/~┴——┴')
                except pymysql.Error as e:
                    print(e)
                finally:
                    sql_base.close()
            elif user[2] == 1:
                try:
                    sqlCha = "UPDATE `Hellos_user` SET `User_sta`=%s WHERE `User_id`=%s"
                    val = (0, plugin_event.data.user_id)
                    cur.execute(sqlCha, val)
                    sql_base.commit()
                    plugin_event.reply(plugin_event.data.sender['name'] + "晚安喵~")
                    sql_base.close()
                except pymysql.Error as e:
                    print(e)
        except pymysql.Error as e:
            print(e)

