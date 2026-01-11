import winreg
from datetime import datetime

def get_autostart_programs():
    """Thu thập ứng dụng khởi động cùng hệ thống từ Registry"""
    autostart_locations = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run")
    ]
    
    print("[+] Ứng dụng khởi động cùng hệ thống:")
    for hive, key_path in autostart_locations:
        try:
            with winreg.OpenKey(hive, key_path) as key:
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        print(f"  - {name}: {value}")
                        i += 1
                    except OSError:
                        break
        except WindowsError as e:
            print(f"  [!] Lỗi khi truy cập {key_path}: {e}")

def get_usb_history():
    """Thu thập lịch sử kết nối USB từ Registry"""
    usb_keys = [
        r"SYSTEM\CurrentControlSet\Enum\USBSTOR",
        r"SYSTEM\CurrentControlSet\Enum\USB"
    ]
    
    print("\n[+] Lịch sử thiết bị USB:")
    for key_path in usb_keys:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                i = 0
                while True:
                    try:
                        device_id = winreg.EnumKey(key, i)
                        device_key = f"{key_path}\\{device_id}"
                        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, device_key) as dev_key:
                            try:
                                friendly_name = winreg.QueryValueEx(dev_key, "FriendlyName")[0]
                                print(f"  - {device_id}: {friendly_name}")
                            except WindowsError:
                                print(f"  - {device_id}")
                        i += 1
                    except OSError:
                        break
        except WindowsError as e:
            print(f"  [!] Lỗi khi truy cập {key_path}: {e}")

def get_user_activity():
    """Thu thập hoạt động gần đây của người dùng từ Registry"""
    print("\n[+] Hoạt động gần đây của người dùng:")
    
    # MRU (Most Recently Used) - File đã mở gần đây
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs") as key:
            for i in range(0, winreg.QueryInfoKey(key)[1]):
                name, value, _ = winreg.EnumValue(key, i)
                if name.isdigit():  # Bỏ qua các giá trị không phải số
                    print(f"  - File đã mở: {value.decode('utf-16le', errors='ignore').rstrip('\x00')}")
    except WindowsError as e:
        print(f"  [!] Lỗi khi truy cập RecentDocs: {e}")

if __name__ == "__main__":
    print(f"=== THU THẬP THÔNG TIN AN NINH MẠNG TỪ REGISTRY - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    get_autostart_programs()
    get_usb_history()
    get_user_activity()