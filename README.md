# scan_net
Python Script with Fing which scan local network at regular interval, and notify by Telegram

You need to add this line at the end of sudoers file, to be able to run `sudo fing` without password asking :

```myusername ALL = (root) NOPASSWD: /bin/fing```

You have to replace `myusername` with your username
