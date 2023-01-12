# scan_net
Python Script with Fing which scan local network at regular interval, and notify by Telegram


Fing CLI : https://www.fing.com/images/uploads/general/CLI_Linux_Debian_5.5.2.zip  (Debian .deb file)

You need to add this line at the end of sudoers file, to be able to run `sudo fing` without password asking :

```myusername ALL = (root) NOPASSWD: /bin/fing```

You have to replace `myusername` with your username
