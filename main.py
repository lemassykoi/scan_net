#!/usr/bin/env python3
import os, subprocess, sys, logging, colorlog, time, signal
import ipaddress, requests
import pandas as pd
TG_chat_id  = ''
TG_token    = ''
sleep_time  = 15
irrelevant  = ['192.168.0.2',   # Dashcam
               '192.168.0.120', # Smartphone
               '192.168.0.200', # Google Home
               '192.168.0.254']
file1       = 'devices_list_1.csv'
file2       = 'devices_list_2.csv'
my_log_file = 'scan_net.log'
method1     = 'log,csv,' + file1
method2     = 'log,csv,' + file2

def Notify(Message):
    logger = logging.getLogger()
    logger.info(Message)
    requests.get('https://api.telegram.org/bot' + TG_token + '/sendMessage?chat_id=' + TG_chat_id + '&text=' + Message)

def setup_logging(log_file):
  # Création de l'objet logger
  logger = logging.getLogger()
  logger.setLevel(logging.INFO)

  # Création de l'objet handler et ajout au logger
  log_handler = logging.FileHandler(log_file)
  logger.addHandler(log_handler)

  # Création du formatter avec couleurs
  console_formatter = colorlog.ColoredFormatter("%(asctime)s - %(log_color)s%(levelname)s:%(reset)s\t - %(message)s",
    log_colors={
      'INFO':     'green',
      'WARNING':  'yellow',
      'ERROR':    'red',
      'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
  )
  
  # Création de l'objet handler pour la console
  console_handler = logging.StreamHandler()
  # Ajout du formatter au handler
  console_handler.setFormatter(console_formatter)
  # Ajout au logger
  logger.addHandler(console_handler)
  
  # Création du formateur et ajout au handler
  log_formatter = logging.Formatter('%(asctime)s - %(levelname)s\t - %(message)s')
  log_handler.setFormatter(log_formatter)
  console_handler.setFormatter(console_formatter)

def signal_handler(signal, frame):
  print("\n\t Ctrl+C détecté, arrêt du programme \n")
  # Insérez ici le code nécessaire pour arrêter proprement votre programme
  sys.exit(0)

def show_diff():
  logger = logging.getLogger()
  logger.info('Starting fing scanner...#1')
  result = subprocess.run(['sudo', 'fing', '-r', '1', '-o', method1], capture_output=True, text=True)
  df1 = pd.read_csv(file1, names=['date_time','status','ip','NaN','dns_name','mac_address','manufacturer'], delimiter=';')
  os.remove(file1)
  df1 = df1.sort_values(by='ip', key=lambda col: col.map(lambda x: ipaddress.IPv4Address(x)))
  df1 = df1.drop(columns=['date_time', 'status', 'NaN', 'dns_name', 'manufacturer'])
  first_df_ips = set(df1['ip'])
  logger.info('...........................Done !')
  
  logger.info('Sleep for ' + str(sleep_time) + ' seconds...')
  time.sleep(sleep_time)

  logger.info('Starting fing scanner...#2')
  result = subprocess.run(['sudo', 'fing', '-r', '1', '-o', method2], capture_output=True, text=True)
  df2 = pd.read_csv(file2, names=['date_time','status','ip','NaN','dns_name','mac_address','manufacturer'], delimiter=';')
  os.remove(file2)
  df2 = df2.sort_values(by='ip', key=lambda col: col.map(lambda x: ipaddress.IPv4Address(x)))
  df2 = df2.drop(columns=['date_time', 'status', 'NaN', 'dns_name', 'manufacturer'])
  second_df_ips = set(df2['ip'])
  logger.info('...........................Done !')

  new_ips = second_df_ips - first_df_ips
  if new_ips:
    logger.warning('Differences : ')
    for new_ip in new_ips:
      if new_ip not in irrelevant:
        print(f"New IP : {new_ip}")
        ## nmap new_ip
      else:
        print(f"Irrelevant IP : {new_ip}")
  else:
    logger.info('No new host. Cool.')
  return new_ips

def main():
  signal.signal(signal.SIGINT, signal_handler)
  if os.path.exists(file1):
    logger.info('Deleting old CSV files')
    os.remove(file1)
  if os.path.exists(file2):
    os.remove(file2)
  # Configuration des logs
  log_file = my_log_file
  setup_logging(log_file)
  logger = logging.getLogger()
  # Start main func
  logger.info('Starting main()...')
  while True:
    new_ips = show_diff()
    for ip_add in new_ips:
      if ip_add not in irrelevant:
        Notify('New IP : ' + str(ip_add))
    logger.info('Sleep...')
    time.sleep(sleep_time)

if __name__ == "__main__":
  main()
  
