Chuyên đề: Tấng công bảo mật ở các Layer 
Layer 2 
- MAC Flooding (Tấn công tràn bảng CAM) 
- Giới hạn số lượng MAC 
- Đưa ra hd khi bị vi phạm: Restrict 
- Khai đúng port mới đc vào 
- sticky :
- ARP spoofing (giả mạo)
 - Tấn công 
- Tấn công DHCP 
DHCP Starvation Attack (Lấy hết ip từ server) 
Rogue Server (Dựng 1 server giả mạo) 
 - Tính năng DHCP Snooping chống giả hardware add, chống giả mạo server 
- Tấn công DHCP HARDWARE ADD 
- Tấn công STP 

Phương pháp bảo mật 
- Không dùng VLAN1 để khai báo các cổng 
- Không cho tất cả VLAN đi qua trunk 
- Khai báo Port với người dùng : 
 + Port Security
 + Tắt port k dùng 
 + DHCP Snooping trusted/Untrusted 
 + Private Vlan 
 + BPD 

Bảo mật ở layer 3 
- Access control list (ACL): là 1 danh sách các yêu cầu cần kể kiểm soát việc truy cập thiết bị, ứng dụng hay dịch vụ mạng 
- Hoạt động chính của ACL là Permit và Deny 
- Việc kiểm soat đc thực hiện cả 2 hướng vào & ra 
- Thường được khai báo trên các tb Sw, Router và đặc biệt là Firewall 


Bảo vệ tấn công TCP SYN Attack 
- Tấn công DDoS giả mạo địa chỉ nguồn 
Bảo vệ IP Spoofing bằng uRPF


Mã hóa 
- có 2 loại: Đối xứng và bất đối xứng 
- Đối xứng: tốc độ mã hóa và giải mã rất nhanh 
- Bất đối xứng: Bảo mật hơn, tốc độ xử lý lâu 
	+ Thuật toán trao đổi khóa Diffie Hellman 
- Hàm băm xác thực dữ liệu Hash có 2 loại SHA và MD5
- Mã hóa công khai Public Key (PKI) 
HTTPS 
IPSec: là giải pháp bảo vệ layer 3 
Có 3 thành phần AH, ESP, IKE 
AH & ESP 
- AH: Sài 1 key chung để mã hóa IP Header + data + key -> hash 
- ESH: giống AH và mã hóa thêm bản tin 

Hoạt động của IPSEc 

B1: xác định dữ liệu 
B2: Trao đổi IKE Phase 1 
B3: Trao đổi IKE Phase 2 
IKE: Trao đổi cách thức cần bảo mật 



Phase 1: 5 thông số 
Hash: MD5, SHA 
authentication: Preshare-key, RSA 
group:
Lifetime:
Encryption: 

IKE phase 2
+ Giao thức IPSec: ESP hoặc AH.
+ IPSec mode: Tunnel hoặc transport.
+ Encryption: 
+ Hash: MD5, SHA 














