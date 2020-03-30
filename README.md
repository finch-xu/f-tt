### 这是一个测试项目,构建了一个文档转换PO程序，用于文件翻译使用
环境：
- ubuntu 18.04
- Translate ToolKit 2.5.0 API
- Python3.7
- Flask 1.1.1
- uWGSI

Translate ToolKit 官方文档 http://docs.translatehouse.org/projects/translate-toolkit/en/latest/api/index.html

### 目前实现的功能是:
- txt文档转po文件（txt2po）
- json文件转po文件（json2po）
- 对po文件进行分析统计（pocount）


### How to use ?
(1)安装&运行uwsgi:

(```)

sudo apt-get install uwsgi uwsgi-plugin-python uwsgi-plugin-python3
sudo uwsgi /home/ubuntu/f-tt/flaskr/uwsgi.ini -d /home/ubuntu/f-tt/flaskr/logs/log.log
(```)

uwsgi.ini文件在项目的 f-tt/flaskr/uwsgi.ini
(杀死uwsgi的命令是 sudo pkill -f uwsgi -9)
(2)修改nginx配置文件

(```)
sudo vim /etc/nginx/sites-available/default

server {
	listen 5000;

	root /var/www/html;

	server_name ip或者你的域名;

	location / {
		include /etc/nginx/uwsgi_params;
		uwsgi_pass 127.0.0.1:622;
	}

(```)
然后重启nginx即可.
(3)这时候输入地址:5000回车就能看到你的网站了.