#-*- encoding: utf-8 -*-
'''
hello.py.py
Created on 2020/3/28 14:15
Copyright (c) 2020/3/28, finch_xu.
@author: finch_xu
'''
import os
from datetime import datetime

from flask import Flask, request, flash, redirect, url_for, render_template, send_from_directory
from translate.convert import txt2po, json2po, html2po
from translate.tools import pocount
from werkzeug.utils import secure_filename
from pypinyin import lazy_pinyin


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'json', 'html'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CONVERT_FOLDER = 'convert'
app.config['CONVERT_FOLDER'] = CONVERT_FOLDER


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#上传动作
@app.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template("manage.html")
    dt = datetime.now().strftime('%Y%m%d%H%M%S')
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('没有文件')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('没选择文件')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = dt + '-' + secure_filename(file.filename)
            # filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('manage_file', filename=filename))
        return render_template('manage.html')

#管理页面
@app.route('/', methods=['GET', 'POST'])
def manage_file():
    if request.method == 'GET':
        files_list = os.listdir(app.config['UPLOAD_FOLDER'])
        cfiles_list = os.listdir(app.config['CONVERT_FOLDER'])
        return render_template("manage.html", files_list=files_list, cfiles_list=cfiles_list)


###############
@app.route('/convertfile/<path:filename>')
def convert_file(filename):
    #给输出的文件设定po拓展名
    filenameOut = os.path.splitext(filename)[0] + '.po'
    #判断拓展名，来进行不同的转换操作
    key = os.path.splitext(filename)[-1][1:]
    if key == 'txt':
        # aa = open('alisi.txt', 'rb+')
        # bb = open('alisi.po','wb+')
        aa = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb+')
        bb = open(os.path.join(app.config['CONVERT_FOLDER'], filenameOut), 'wb+')

        txt2po.run_converter(aa,bb,template_file=None,duplicatestyle='msgctxt',encoding='utf-8',flavour='plain',no_segmentation=False)
        # html2po.converthtml(aa,'convert-documentation.po',templates=None,includeuntagged=False,pot=False,duplicatestyle='msgctxt',keepcomments=False)
        aa.close()
        bb.close()
        return redirect(url_for('manage_file'))
    if key == 'json':
        aa = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb+')
        bb = open(os.path.join(app.config['CONVERT_FOLDER'], filenameOut), 'wb+')

        # txt2po.run_converter(aa, bb, template_file=None, duplicatestyle='msgctxt', encoding='utf-8', flavour='plain',no_segmentation=False)
        # html2po.converthtml(aa,'convert-documentation.po',templates=None,includeuntagged=False,pot=False,duplicatestyle='msgctxt',keepcomments=False)
        json2po.convertjson(aa, bb, template_file=None, pot=False, duplicatestyle='msgctxt',dialect='default', filter=None)
        aa.close()
        bb.close()
        return redirect(url_for('manage_file'))



    return redirect(url_for('manage_file'))


#下载文件的动作
@app.route('/download/<path:filename>')
def download(filename):
    #通过文件拓展名去不通的文件夹下载
    key = os.path.splitext(filename)[-1][1:]
    if key == 'po':
        return send_from_directory(r"convert", filename=filename, as_attachment=True)
    return send_from_directory(r"uploads", filename=filename, as_attachment=True)


#统计功能
@app.route('/count/<path:filename>')
def count_file(filename):
    countfilename = os.path.join(app.config['CONVERT_FOLDER'],filename)
    state = pocount.calcstats_old(countfilename)
    return render_template("countinfo.html", state=state, filename=filename)

def percent(denominator, devisor):
    if devisor == 0:
        return 0
    else:
        return denominator * 100 / devisor



#运行项目
if __name__=="__main__":
    app.run()




