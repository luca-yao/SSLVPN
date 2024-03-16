
# 前言
目前公司因為資訊安全性考量，所以在Fortigate的VPN開啟了 mac-addr-check 的功能，畢竟不能限制VPN連線來源，透過帳號控管仍有很高的風險

>肯定一堆人密碼是 a12345或者password
<br>10元買帳號(・∀・)つ⑩ 

## 程序思維講解
因為公司大老們，異想天開的想要透過MAC管理使用者登入設備以外，還想要透過/**日期來自動開關VPN權限**/，所以我在清單中除了新增設備的MAC位址以外，還添加了 開始日期(start_time) 與 結束日期 (end_time) ，再透過CI/CD程序(我自己是用Jenkins)來進行自動化管理。

思緒是這樣的，如果公司只有50個人雖然要花一點時間，但也不算辦不到
<BR>假設公司有100人，也不是真的辦不到，但要花很多時間去處理，假設今天公司有300人呢?1000人呢?
<BR>總不能還是一個一個加吧? 並且還會發生硬體設備更新或故障更換的問題。
<BR>況且如果跟我一樣碰上喜歡作夢的老先生，除了想辦法做以外，你還真不知道可以怎麼做呢。
<BR>光想到我要去記每一個使用者的申請日期和時間，我就想~~辭職~~了。

> 於是 "科技來自於人性，人性來自於惰性" (　˙灬˙　)

---
懶惰鬼的我想到，不如就透過'Netmiko'來幫我處理吧
<br />本次套件的樹狀結構如下：
+ SSL-VPN
  + List
    + 部門名稱  ※Client清單
  + Firewall-sslvpn.py ※主程式
  + mac_list.py  ※讀取/寫入 檔案
  + mail_sender.py  ※信件寄送

老樣子還是把一些功能拆出來模組化了，模組化的好處是當初問題比較好排除，也更好調整

這只是我自己的習慣啦，如果想要全部擠在一個上面也可以。(ゝ∀･)
by the way, let's go!

講主程式之前，咱們先來講講，比主程式更重要也修改更多的部門清單吧!
---
List/MIS  ※本次以MIS舉例

```
- USER: luca_yao
  WIFI: a4:cc:ee:aa:00:01  #Wifi MAC
  WIRED: a4:cc:ee:aa:00:01 #有線 MAC
  START_TIME: 01-01        #開始時間
  END_TIME: 06-30          #結束時間

- USER: Joanna_wang
  WIFI: aa:bb:33:d3:qq:01
  WIRED: da:a9:11:23:22:ea
  START_TIME: 02-02
  END_TIME: 02-12
```

Firewall-sslvpn.py
--
```
# Editer : Luca_yao
# E-mail : stelliva42@gmail.com
# Date : 2024/02/06

import os, re
from netmiko import ConnectHandler
from mac_list import main

def connect_to_fortigate(device_info):
    try:
        log_file_path = f"netmiko.log"
        net_connect = ConnectHandler(**device_info, session_log=log_file_path)
        print("Connected to FortiGate device")
        return net_connect
    except Exception as e:
        print(f"Error connecting to FortiGate: {e}")
        return None

def configure_sslvpn_portal(net_connect, portal_name, mac_addr_list):
    try:
        commands = [
            'config vpn ssl web portal',
            f'edit {portal_name}',
            'config mac-addr-check-rule',
            f'edit "VPN_{file_name}"',
            f'set mac-addr-list {mac_addr_list}',
            'show',
            'next',  
            'end',   
        ]
        for command in commands:
            output = net_connect.send_command_timing(command)
        print(output)

    except Exception as e:
        print(f"Error configuring SSL VPN Portal: {e}")

    finally:
        if net_connect:
            net_connect.disconnect()
            print("Disconnected from FortiGate device")

# FortiGate Device information
fortigate_device = {
    'device_type': 'fortinet',
    'ip': 'xxx.xxx.xxx.xxx', #防火牆IP
    'username': 'username',  #帳號
    'password': 'password',  #密碼
    'port': 22, 
}

file_name = input()
file_path = os.path.join("List", file_name)

net_connection = connect_to_fortigate(fortigate_device)

if net_connection:
    sslvpn_portal_name = f'SSLVPN_{file_name}_Portal'
    mac_addr_list = main(file_path)
    configure_sslvpn_portal(net_connection, sslvpn_portal_name, mac_addr_list)
```

### 結論
再透過Jenkins上的自動化排程進行，可以達到每天幫我們做使用者開啟與關閉，配合mail_sender可以在關閉的當天寄送郵件給使用者，提醒他VPN已關閉。

當然公司該走的流程還是得走，但我們就不用花時間來處理這些~~砸碎~~重要的事項，有更多時間去做更有意義或是產生自我價值的事情。

有人說過要怎麼阻止一個人成長或者摧毀他人，就是讓他不停地重複的事情，或者忙到沒時間成長，沒動力自修
### 公司可能不差，但主管爛是不可避免的，我們能做的就是保持更做熱誠、持續成長
## 公司不養廢人，但有很多人會希望你是廢人
# 共勉之 (#`皿´)
