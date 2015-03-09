# Auto File Upload local to FTP server with python

Auto file Upload in maximum two day of week day. easily can set up config.ini.

Requirements
============
* python 2.7

Setup Config.ini file
====================

[auto_sync]
st_date = 3
en_date = 6
ext = .zip
path = /home/../../zipfile or py file folder
src_path = /home/../Source.hg/
svr_name = ftp.website.com
usrname = admin
pass = admin
cmd=rm -r
cr_date = 2013-02-02
ctrl_time=15:00:00
ctrl = 0

Run script
=============
python sync.py



