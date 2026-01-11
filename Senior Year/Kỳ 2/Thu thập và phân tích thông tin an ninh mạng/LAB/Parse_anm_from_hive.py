import os
import sys
from Registry import Registry
from datetime import datetime

def get_control_set(reg_system):
    """Xác định ControlSet đang sử dụng"""
    try:
        select = reg_system.open("Select")
        current = select.value("Current").value()
        return f"ControlSet00{current}"
    except:
        return "ControlSet001"  # Fallback nếu không xác định được

def analyze_system_info(reg_system, control_set):
    """Phân tích thông tin hệ thống"""
    print("\n=== THÔNG TIN HỆ THỐNG ===")
    
    # Tên máy tính
    try:
        compname = reg_system.open(f"{control_set}\\Control\\ComputerName\\ComputerName")
        print(f"[+] Tên máy tính: {compname.value('ComputerName').value()}")
    except Exception as e:
        print(f"[!] Không đọc được tên máy tính: {str(e)}")

    # Múi giờ
    try:
        timezone = reg_system.open(f"{control_set}\\Control\\TimeZoneInformation")
        print(f"[+] Múi giờ: {timezone.value('TimeZoneKeyName').value()}")
    except Exception as e:
        print(f"[!] Không đọc được thông tin múi giờ: {str(e)}")

    # Thời gian shutdown cuối cùng
    try:
        shutdown_time = reg_system.open(f"{control_set}\\Control\\Windows").value("ShutdownTime").value()
        if shutdown_time:
            print(f"[+] Thời gian shutdown cuối cùng: {shutdown_time}")
    except:
        pass

def analyze_network_info(reg_system, control_set):
    """Phân tích thông tin mạng"""
    print("\n=== THÔNG TIN MẠNG ===")
    try:
        interfaces = reg_system.open(f"{control_set}\\Services\\Tcpip\\Parameters\\Interfaces")
        for interface in interfaces.subkeys():
            print(f"\n[+] Interface: {interface.name()}")
            try:
                if "Name" in interface.values():
                    print(f"  - Tên adapter: {interface.value('Name').value()}")
                if "DhcpIPAddress" in interface.values() and interface.value("DhcpIPAddress").value():
                    print(f"  - IP: {interface.value('DhcpIPAddress').value()}")
                if "DhcpSubnetMask" in interface.values() and interface.value("DhcpSubnetMask").value():
                    print(f"  - Subnet mask: {interface.value('DhcpSubnetMask').value()}")
                if "DhcpServer" in interface.values() and interface.value("DhcpServer").value():
                    print(f"  - DHCP Server: {interface.value('DhcpServer').value()}")
                if "DefaultGateway" in interface.values() and interface.value("DefaultGateway").value():
                    print(f"  - Gateway: {interface.value('DefaultGateway').value()}")
            except Exception as e:
                print(f"  [!] Lỗi khi đọc thông tin interface: {str(e)}")
    except Exception as e:
        print(f"[!] Không đọc được thông tin mạng: {str(e)}")

def analyze_usb_devices(reg_system, control_set):
    """Phân tích thiết bị USB"""
    print("\n=== THIẾT BỊ USB ===")
    try:
        usbstor = reg_system.open(f"{control_set}\\Enum\\USBSTOR")
        for device in usbstor.subkeys():
            for instance in device.subkeys():
                try:
                    vendor = device.name().split("&")[0].replace("Disk&Ven_", "")
                    product = device.name().split("&")[1].replace("Prod_", "")
                    rev = device.name().split("&")[2].replace("Rev_", "")
                    
                    print(f"\n[+] Thiết bị: {vendor} {product} (Rev: {rev})")
                    print(f"  - ID: {device.name()}\\{instance.name()}")
                    
                    if "FriendlyName" in instance.values():
                        print(f"  - Tên thiết bị: {instance.value('FriendlyName').value()}")
                    if "ParentIdPrefix" in instance.values():
                        print(f"  - Parent ID: {instance.value('ParentIdPrefix').value()}")
                    if "FirstInstallDate" in instance.values():
                        date = instance.value("FirstInstallDate").value()
                        print(f"  - Ngày cài đặt đầu tiên: {date}")
                except Exception as e:
                    print(f"  [!] Lỗi khi đọc thông tin thiết bị: {str(e)}")
    except Exception as e:
        print(f"[!] Không đọc được thông tin USB: {str(e)}")

def analyze_os_info(reg_software):
    """Phân tích thông tin hệ điều hành"""
    print("\n=== THÔNG TIN HỆ ĐIỀU HÀNH ===")
    try:
        winver = reg_software.open("Microsoft\\Windows NT\\CurrentVersion")
        print(f"[+] Tên hệ điều hành: {winver.value('ProductName').value()}")
        print(f"[+] Phiên bản: {winver.value('CurrentVersion').value()}")
        print(f"[+] Build: {winver.value('CurrentBuild').value()}")
        
        if "InstallDate" in winver.values():
            install_date = datetime.utcfromtimestamp(winver.value("InstallDate").value())
            print(f"[+] Ngày cài đặt: {install_date}")
        
        if "RegisteredOwner" in winver.values():
            print(f"[+] Chủ sở hữu: {winver.value('RegisteredOwner').value()}")
        
        if "ProductId" in winver.values():
            print(f"[+] Product ID: {winver.value('ProductId').value()}")
    except Exception as e:
        print(f"[!] Không đọc được thông tin hệ điều hành: {str(e)}")

def analyze_installed_software(reg_software):
    """Phân tích phần mềm đã cài đặt"""
    print("\n=== PHẦN MỀM ĐÃ CÀI ĐẶT ===")
    uninstall_keys = [
        "Microsoft\\Windows\\CurrentVersion\\Uninstall",
        "Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
    ]
    
    software_list = []
    
    for key_path in uninstall_keys:
        try:
            uninstall = reg_software.open(key_path)
            for program in uninstall.subkeys():
                try:
                    if "DisplayName" in program.values():
                        name = program.value("DisplayName").value()
                        version = program.value("DisplayVersion").value() if "DisplayVersion" in program.values() else "N/A"
                        publisher = program.value("Publisher").value() if "Publisher" in program.values() else "N/A"
                        install_date = program.value("InstallDate").value() if "InstallDate" in program.values() else "N/A"
                        install_location = program.value("InstallLocation").value() if "InstallLocation" in program.values() else "N/A"
                        
                        software_list.append({
                            "name": name,
                            "version": version,
                            "publisher": publisher,
                            "install_date": install_date,
                            "install_location": install_location
                        })
                except:
                    continue
        except:
            continue
    
    # Sắp xếp và hiển thị
    software_list.sort(key=lambda x: x["name"].lower())
    
    for idx, software in enumerate(software_list, 1):
        print(f"\n[{idx}] {software['name']}")
        print(f"  - Phiên bản: {software['version']}")
        print(f"  - Nhà phát hành: {software['publisher']}")
        print(f"  - Ngày cài đặt: {software['install_date']}")
        if software['install_location'] != "N/A":
            print(f"  - Vị trí cài đặt: {software['install_location']}")
    
    print(f"\n[+] Tổng cộng: {len(software_list)} phần mềm đã cài đặt")

def analyze_uninstalled_software(reg_software):
    """Phân tích phần mềm đã gỡ cài đặt"""
    print("\n=== PHẦN MỀM ĐÃ GỠ CÀI ĐẶT ===")
    uninstall_keys = [
        "Microsoft\\Windows\\CurrentVersion\\Uninstall",
        "Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
    ]
    
    uninstalled_list = []
    
    for key_path in uninstall_keys:
        try:
            uninstall = reg_software.open(key_path)
            for program in uninstall.subkeys():
                try:
                    if "UninstallString" in program.values() and "DisplayName" in program.values():
                        name = program.value("DisplayName").value()
                        uninstall_string = program.value("UninstallString").value()
                        
                        uninstalled_list.append({
                            "name": name,
                            "uninstall_string": uninstall_string
                        })
                except:
                    continue
        except:
            continue
    
    for idx, software in enumerate(uninstalled_list, 1):
        print(f"\n[{idx}] {software['name']}")
        print(f"  - Lệnh gỡ cài đặt: {software['uninstall_string']}")
    
    print(f"\n[+] Tổng cộng: {len(uninstalled_list)} phần mềm đã gỡ cài đặt")

def analyze_user_profiles(reg_sam, reg_software):
    """Phân tích thông tin người dùng"""
    print("\n=== THÔNG TIN NGƯỜI DÙNG ===")
    
    # Danh sách người dùng từ SAM
    try:
        users = reg_sam.open("SAM\\Domains\\Account\\Users\\Names")
        print("\n[+] Danh sách tài khoản người dùng:")
        for user in users.subkeys():
            print(f"  - {user.name()}")
    except Exception as e:
        print(f"[!] Không đọc được danh sách người dùng từ SAM: {str(e)}")
    
    # Thông tin profile từ SOFTWARE
    try:
        profilelist = reg_software.open("Microsoft\\Windows NT\\CurrentVersion\\ProfileList")
        print("\n[+] Thông tin profile người dùng:")
        for profile in profilelist.subkeys():
            try:
                sid = profile.name()
                path = profile.value("ProfileImagePath").value()
                print(f"  - SID: {sid}")
                print(f"    Đường dẫn: {path}")
                
                if "LastUseTime" in profile.values():
                    last_use = profile.value("LastUseTime").value()
                    print(f"    Thời gian sử dụng cuối: {last_use}")
            except:
                continue
    except Exception as e:
        print(f"[!] Không đọc được ProfileList: {str(e)}")

def analyze_registry_from_dd(mount_path):
    """Phân tích chính từ ảnh đĩa DD"""
    registry_paths = {
        'SYSTEM': os.path.join(mount_path, 'Windows/System32/config/SYSTEM'),
        'SOFTWARE': os.path.join(mount_path, 'Windows/System32/config/SOFTWARE'),
        'SAM': os.path.join(mount_path, 'Windows/System32/config/SAM')
    }

    print(f"\n=== PHÂN TÍCH REGISTRY TỪ ĐĨA ẢNH TẠI {mount_path} ===")

    # Phân tích SYSTEM hive
    if os.path.exists(registry_paths['SYSTEM']):
        try:
            reg_system = Registry.Registry(registry_paths['SYSTEM'])
            control_set = get_control_set(reg_system)
            
            analyze_system_info(reg_system, control_set)
            analyze_network_info(reg_system, control_set)
            analyze_usb_devices(reg_system, control_set)
        except Exception as e:
            print(f"[!] Lỗi khi đọc SYSTEM hive: {str(e)}")
    else:
        print(f"[!] Không tìm thấy file SYSTEM tại {registry_paths['SYSTEM']}")

    # Phân tích SOFTWARE hive
    if os.path.exists(registry_paths['SOFTWARE']):
        try:
            reg_software = Registry.Registry(registry_paths['SOFTWARE'])
            
            analyze_os_info(reg_software)
            analyze_installed_software(reg_software)
            analyze_uninstalled_software(reg_software)
        except Exception as e:
            print(f"[!] Lỗi khi đọc SOFTWARE hive: {str(e)}")
    else:
        print(f"[!] Không tìm thấy file SOFTWARE tại {registry_paths['SOFTWARE']}")

    # Phân tích SAM hive
    if os.path.exists(registry_paths['SAM']) and os.path.exists(registry_paths['SOFTWARE']):
        try:
            reg_sam = Registry.Registry(registry_paths['SAM'])
            reg_software = Registry.Registry(registry_paths['SOFTWARE'])
            
            analyze_user_profiles(reg_sam, reg_software)
        except Exception as e:
            print(f"[!] Lỗi khi đọc SAM hive: {str(e)}")
    else:
        print(f"[!] Không tìm thấy file SAM hoặc SOFTWARE cần thiết")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mount_path = sys.argv[1]
    else:
        mount_path = "/media/anphuc/C8CA0C8DCA0C7A48"
    
    if not os.path.exists(mount_path):
        print(f"[!] Thư mục {mount_path} không tồn tại")
        print("Hãy chắc chắn rằng bạn đã mount đĩa ảnh đúng cách")
        print("Ví dụ lệnh mount:")
        print("sudo mkdir /media/diskimage")
        print("sudo mount -o ro,loop,offset=$((206848*512)) cfreds_2015_data_leakage_pc.dd /media/diskimage")
        sys.exit(1)
    
    analyze_registry_from_dd(mount_path)