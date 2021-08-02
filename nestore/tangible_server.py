from matrix_lite import led
import traceback
from bluetooth import *
import subprocess
import time
import syslog
import json
wpa_supplicant_conf = "/etc/wpa_supplicant/wpa_supplicant.conf"
# wpa_supplicant_conf = "/tmp/would_be_wpa_supplicant.conf"
sudo_mode = "sudo "

tangible_server_version = "1.0.0"

def make_discoverable_bluetooth():
     print ('bluetooth on!\n')
     
     
     subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])
 
    
def trust_device(addr):
     print ('trust on!\n')
     os.system("aplay -D hw:2,1 /home/pi/nestore/bluetoothon.wav")
     process= subprocess.Popen(['bluetoothctl'], stdin= subprocess.PIPE, stdout= subprocess.PIPE)
    # process.stdin.write(bytes("pair" + str(addr)+ "\n", "utf-8"))
    
     #process.stdin.flush()
     output, errors= process.communicate(bytes("trust" + str(addr)+ "\n", "utf-8"))  
     print(output)
   #  process.stdin.write(bytes("trust"+ str(addr)+"\n", "utf-8"))

    
def log(priority, str):
    print(str)
    syslog.syslog(priority, str)


def send(client_socket, message, sensible_information=False, custom_formatter=None):
    client_socket.send(message + "!")

    if callable(custom_formatter):
        log(syslog.LOG_INFO, "NESTORE_BLE: sending [" + custom_formatter(message) + " ]")
    elif not sensible_information:
        log(syslog.LOG_INFO, "NESTORE_BLE: sending `" + message + "`")
    else:
        log(syslog.LOG_INFO, "NESTORE_BLE: sending <" + str(len(message)) + " character(s)>")


def recv_timeout(the_socket, timeout=2):
    the_socket.setblocking(0)
    total_data = [];
    begin = time.time()
    while 1:
        # if you got some data, then break after wait sec
        if total_data and time.time() - begin > timeout:
            break
        # if you got no data at all, wait a little longer
        elif time.time() - begin > timeout * 2:
            break
        try:
            data = the_socket.recv(8192)
            if data:
                total_data.append(data)
                begin = time.time()
            else:
                time.sleep(0.1)
        except:
            pass
    data = b''
    for chunk in total_data:
        data += chunk
    return data


def receive(client_socket, sensible_information=False, custom_formatter=None):
    # message = client_socket.recv(8192).decode('utf-8')
    message = recv_timeout(client_socket).decode('utf-8')
    if callable(custom_formatter):
        log(syslog.LOG_INFO, "NESTORE_BLE: received [" + custom_formatter(message) + "]")
    elif not sensible_information:
        log(syslog.LOG_INFO, "NESTORE_BLE: received `" + message + "`")
    else:
        log(syslog.LOG_INFO, "NESTORE_BLE: received <" + str(len(message)) + " character(s)>")
    return message


def wifi_connect(ssid, psk):
    # write wifi config to file
    f = open('wifi.conf', 'w')

    f.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n')
    f.write('update_config=1\n')
    f.write('country=GB\n')
    f.write('\n')
    f.write('network={\n')
    f.write('    ssid="' + ssid + '"\n')
    f.write('    psk="' + psk + '"\n')
    f.write('    key_mgmt= WPA-PSK' + '\n')
    f.write('}\n')
    f.close()

    cmd = ('cp ' + wpa_supplicant_conf + ' wifi.bak.conf')
    cmd_result = os.system(cmd)
    print(cmd + " - " + str(cmd_result))

    cmd = ('sudo mv wifi.conf ' + wpa_supplicant_conf)
    cmd_result = os.system(cmd)
    print(cmd + " - " + str(cmd_result))

    valid_conf = reload_wpa_supplicant()
    if not valid_conf:
        log(syslog.LOG_INFO, "NESTORE_BLE: Restoring previous wpa_supplicant.conf configuration")

        cmd = ('cp wifi.bak.conf ' + wpa_supplicant_conf)
        cmd_result = os.system(cmd)
        print(cmd + " - " + str(cmd_result))
        reload_wpa_supplicant()

    return valid_conf

    # cmd = 'iwconfig wlan0'
    # cmd_result = os.system(cmd)
    # print(cmd + " - " + str(cmd_result))
    #
    # cmd = 'ifconfig wlan0'
    # cmd_result = os.system(cmd)
    # print(cmd + " - " + str(cmd_result))

    # try:
    #  urlopen("https://www.google.com/")
    #  connected=True
    # except:
    # print("no connection")
    # connected=False

    # connected=True


def obtain_current_ip():
    p = subprocess.Popen(['ifconfig', 'wlan0'], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    ip_address = None
    for l in out.decode('utf-8').split('\n'):
        if l.strip().startswith("inet "):
            ip_address = l.strip().split(' ')[1]

    if ip_address is not None:
        log(syslog.LOG_INFO, "NESTORE_BLE: ip address: " + str(ip_address))
    else:
        log(syslog.LOG_INFO, "NESTORE_BLE: no ip address")

    return ip_address


def reload_wpa_supplicant():
    # restart wifi adapter
    #    cmd = (sudo_mode + 'ifconfig wlan0 down')
    #    cmd_result = os.system(cmd)
    #    log(syslog.LOG_INFO, cmd + " - " + str(cmd_result))
    #
    #    time.sleep(2)
    #
    #    cmd = (sudo_mode + 'ifconfig wlan0 up')
    #    cmd_result = os.system(cmd)
    #    log(syslog.LOG_INFO, cmd + " - " + str(cmd_result))

    log(syslog.LOG_INFO, "NESTORE_BLE: reconfiguring wlan0 wpa_supplicant.conf")
    reconf_process = subprocess.Popen(['/sbin/wpa_cli', '-i', 'wlan0', 'reconfigure'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = reconf_process.communicate()
    result = out.decode('utf-8').strip()
    if result == 'OK':
        return True
    else:
        log(syslog.LOG_ERR, "NESTORE BLE: invalid wpa_supplicant.conf: " + result)
        return False
    # cmd = "wpa_cli -i wlan0 reconfigure"
    # cmd_result = os.system(cmd)
    # log(syslog.LOG_INFO, cmd + " - " + str(cmd_result))


def handle_configure_wifi(client_socket):
    send(client_socket, "waiting-ssid")
    ssid = receive(client_socket)

    if ssid == '':
        send(client_socket, "aborting")
        return

    send(client_socket, "waiting-psk")
    psk = receive(client_socket, True)

    if psk == '':
        send(client_socket, "aborting")
        return

    send(client_socket, "configuring-wifi")

    success = wifi_connect(ssid, psk)

    if success:
        time.sleep(15)
        handle_current_ip(client_socket)
        connected=True
        
    else:
        send(client_socket, "invalid-conf")
        connected=False


def handle_current_ip(client_socket):
    ip_address = obtain_current_ip()
    if ip_address is not None:
        send(client_socket, "ip-address:" + str(ip_address))
    else:
        send(client_socket, "no-ip-address")


def token_log_formatter(token):
    l = len(token)
    if l > 30:
        return "Token (" + str(l) + " characters): " + token[:5] + "......." + token[-5:]
    else:
        return "Token (" + str(l) + " characters)"


def handle_configure_user(client_socket):
    send(client_socket, "waiting-access-token")
    token = receive(client_socket, True, token_log_formatter)
    if token == '':
        send(client_socket, "aborting")
        return
    send(client_socket, "waiting-user-language")
    lang = receive(client_socket)
    saveUserProfile(token, lang)
   
    time.sleep(3)  # simulate time for setup

    send(client_socket, "user-configured")

def saveUserProfile(token, lang):
    
    data={"lang-id": lang, "user-id": token}
    with open("/home/pi/nestore/userprofile.json", "w") as jsonFile:
           json.dump(data, jsonFile)



def handle_check_user(client_socket):
    send(client_socket, "checking-user")

    # TODO implement user check
    time.sleep(3)  # simulate time for check
    user_ok = True

    if user_ok:
        send(client_socket, "user-ok")
    else:  # expired token / no user ...
        send(client_socket, "user-need-setup")


def handle_version(client_socket):
    send(client_socket, tangible_server_version)


def handle_client(client_socket):
    commands = {
        "configure-wifi": handle_configure_wifi,
        "current-ip": handle_current_ip,
        "configure-user": handle_configure_user,
        "check-user": handle_check_user,
        "version": handle_version,
        "quit": None
    }

    while True:
        send(client_socket, "ready")
        command = receive(client_socket)
        if commands.__contains__(command):
            if command != "quit":
                commands[command](client_socket)
            else:
                return
        else:
            log(syslog.LOG_ERR, "NESTORE_BLE: ignoring  unknown command - " + command)
            send(client_socket, "unknown-command")


def start_server():
#    while True:
        make_discoverable_bluetooth()
        server_socket = BluetoothSocket(RFCOMM)
        server_socket.bind(("", PORT_ANY))
        server_socket.listen(1)

        port = server_socket.getsockname()[1]

        #uuid = "815425a5-bfac-47bf-9321-c5ff980b5e11"
        #uuid = "440f0605-9ff1-4758-8e1c-611f6047eb50"
        uuid= "440f0605-9ff1-4758-8e1c-611f6047eb50"
        advertise_service(server_socket, "Nestore Tangible Conf Service",
                          service_id=uuid,
                          service_classes=[uuid, SERIAL_PORT_CLASS],
                          profiles=[SERIAL_PORT_PROFILE])

        log(syslog.LOG_INFO, "NESTORE_BLE: Waiting for connection on RFCOMM channel " + str(port))
        
        client_socket, client_info = server_socket.accept()
        
        log(syslog.LOG_INFO, "NESTORE_BLE: Accepted connection from " + str(client_info))
        
        print(client_info[0])
        trust_device(client_info[0])
        try:
            handle_client(client_socket)
        except:
            e_type, e, e_tb = sys.exc_info()
            error_as_string = str.join("NESTORE_BLE: ", traceback.format_exception(e_type, e, e_tb))
            log(syslog.LOG_ERR, "NESTORE_BLE: bluetooth wifi config handling failed - " + error_as_string)

        client_socket.close()
        server_socket.close()

        # finished config
        log(syslog.LOG_INFO, "NESTORE_BLE: Finished configuration")
        led.set("blue") 
        time.sleep(1)
        led.set("blue") 
        time.sleep(1)
        



