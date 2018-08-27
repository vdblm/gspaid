#! /bin/bash

export LC_ALL=C

pkill python3
rm -rf gspaid
pip3 freeze | xargs pip3 uninstall -y

git clone https://github.com/vdblm/gspaid.git
cd gspaid
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py shell < install.py
python3 manage.py runserver 80 &
