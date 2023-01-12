# scan_net
Python 3.7+ Script with Fing which scan local network at regular interval, and notify by Telegram

Pre requisites :
`pip install pandas colorlog`


Fing CLI : https://www.fing.com/images/uploads/general/CLI_Linux_Debian_5.5.2.zip  (Debian .deb file)

You need to add this line at the end of sudoers file ( run `visudo` ) to be able to run `sudo fing` without password asking :

```myusername ALL = (root) NOPASSWD: /bin/fing```

You have to replace `myusername` with your username

Adjust variables at the beginning of the script
