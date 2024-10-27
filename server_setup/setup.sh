#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)
echo $SCRIPT_DIR
sudo apt install python3-pip python3-venv python3-dev
sudo apt install apache2 apache2-dev

cd $SCRIPT_DIR
python3 -m venv ~/flask_venv
source ~/flask_venv/bin/activate
pip3 install -r ../requirements.txt
pip3 install mod_wsgi mod_wsgi-httpd

# 上記以外に以下の設定が必要
# 1. /etc/apache2/site-available/001-linebot.confの作成
# 2. a2ensite 001-linebot の実行
# 3. /etc/apache2/envvars の実行ユーザをwww-data -> ubuntu へ変更
# 4. mod_wsgi-express module-config >> /etc/apache2/apache2.conf の実行
# 5. echo "WSGIApplicationGroup %{GLOBAL}" >> /etc/apache2/apache2.conf の実行
