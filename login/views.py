import random
from imp import reload

import jieba
from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os
import sys
reload(sys)

from . import models
from . import forms
import hashlib
import datetime
import csv
import pymysql
# Create your views here.


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user)
    return code



@csrf_exempt
def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    try:
        if request.GET:
            date = request.GET['date']
        else:
            date = '2020-03-01'
    except:
        date = '2020-03-01'
    try:
        type=request.GET['out']
    except:
        type = 'in'

    with open(r'C:\Users\15503\PycharmProjects\mysite\login\csv文件\youtube词云数据.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header_row = next(reader)
        date1, comment1,num1 = [], [],[]
        for row in reader:
            date1.append(row[0])
            comment1.append(row[1])
            num1.append(row[2])
    with open(r'C:\Users\15503\PycharmProjects\mysite\login\csv文件\微博词云数据.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header_row = next(reader)
        date2, comment2 ,num2= [], [],[]
        for row in reader:
            date2.append(row[0])
            comment2.append(row[1])
            num2.append(row[2])
    cy_date=date[-2:]
    cy_date=str(int(cy_date))
    index=int(cy_date)-1
    if type!='in':
        cy_comment = eval(comment1[index])
        cy_num = eval(num1[index])
    else:
        cy_comment = eval(comment2[index])
        cy_num = eval(num2[index])
    db = pymysql.connect("localhost", "root", "20413wrx", "runoob", charset='utf8')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM 微博疫情评论分析结果")
    results = cursor.fetchall()
    topic, positive, negative, neutral = [], [], [], []
    for row in results:
        topic.append(row[0])
        positive.append(row[1])
        negative.append(int(row[2]))
        neutral.append(int(row[3]))

    date = date[5:7] + '.' + date[-2:]
    ctx = date[-1]
    cursor = db.cursor()
    cursor.execute("SELECT * FROM 全国疫情情况")
    results = cursor.fetchall()
    date1, province, confirm, dead, heal = [], [], [], [], []
    for row in results:
        date1.append(row[0])
        province.append(row[1])
        confirm.append(int(row[2]))
        dead.append(int(row[3]))
        heal.append(int(row[4]))
    index = []
    for i in range(len(date1)):
        if date1[i] == date:
            index.append(i)
    map_province, map_confirm, map_dead, map_heal = [], [], [], []
    for i in index:
        map_province.append(province[i])
        map_confirm.append(confirm[i])
        map_dead.append(dead[i])
        map_heal.append(heal[i])
    name='湖北'
    date11='03.01'
    if request.POST:
        name = request.POST['name']
        date1=random.randint(10, 30)
        date11='03.'+str(date1)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM 各省疫情情况")
    results = cursor.fetchall()
    date1, city, province, confirm, dead, heal = [], [], [], [], [], []
    for row in results:
        date1.append(row[0])
        province.append(row[1])
        city.append(row[2])
        confirm.append(int(row[3]))
        dead.append(row[4])
        heal.append(row[5])
    index = []
    for i in range(len(date1)):
        if date1[i] == date11:
            index.append(i)
    city_name = []
    city_confirm = []
    for i in index:
        if province[i] == name:
            city_name.append(city[i])
            city_confirm.append(confirm[i])
    if name=='湖北':
        city_name[2]='襄阳市'
        city_name[4] = '恩施土家族苗族自治州'
    cursor = db.cursor()
    cursor.execute("SELECT * FROM 新增人数")
    results = cursor.fetchall()
    date, confirm, dead, heal = [], [], [], []
    for row in results:
        date.append(row[0])
        confirm.append(row[1])
        dead.append(row[3])
        heal.append(row[4])
    import json
    ctx=int(ctx)+1
    cursor = db.cursor()
    cursor.execute("SELECT * FROM 湖北人口迁出情况")
    results = cursor.fetchall()
    ctx_date,ctx_city ,ctx_province= [],[],[]
    for row in results:
        ctx_city.append(row[0])
        ctx_province.append(row[1])
        ctx_date.append(float(row[ctx]))
    cursor = db.cursor()
    cursor.execute("SELECT * FROM 湖北人口迁入情况")
    results = cursor.fetchall()
    cyx_date,cyx_city,cyx_province = [],[],[]
    for row in results:
        cyx_city.append(row[0])
        cyx_province.append(row[1])
        cyx_date.append(float(row[ctx]))
    return render(request, 'login/index.html',{
            'date': json.dumps(date),'confirm': json.dumps(confirm),'dead': json.dumps(dead),'heal': json.dumps(heal),'ctx_city': json.dumps(ctx_city),'ctx_date': json.dumps(ctx_date),
        'cyx_city': json.dumps(cyx_city), 'cyx_date': json.dumps(cyx_date),'ctx_province': json.dumps(ctx_province),'cyx_province': json.dumps(cyx_province),
        'map_province': json.dumps(map_province), 'map_confirm': json.dumps(map_confirm), 'map_dead': json.dumps(map_dead),
        'map_heal': json.dumps(cyx_province),'city_name': json.dumps(city_name), 'city_confirm': json.dumps(city_confirm),'name': json.dumps(name),
        'topic': json.dumps(topic), 'positive': json.dumps(positive),
        'negative': json.dumps(negative), 'neutral': json.dumps(neutral), 'cy_num': json.dumps(cy_num), 'cy_comment': json.dumps(cy_comment),
        })

def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name=username)
            except :
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())


            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')

    request.session.flush()
    # del request.session['is_login']
    return redirect("/login/")







