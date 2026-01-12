OpenVPN 
- CA Cấp chứng chỉ  
- Tunnel 
- Người dùng tru cập từ xa đến server
- Khi đấu nối VPN chỉ hỗ trợ 

IPSEc 

- Chạy ở tầng mạng 
 

- Nối từ 2 site với nhau 
- Cho phép toàn bộ mà k quan tâm đến ứng dụng 
- là 1 framework có nhiều giao thức 
-IPSEc Protocol AH, ESP, ESP + AH liên quan đến việc trao đổi dữ liệu 
 + AH: Xác thực nội dung k bị thay đổi 
 + ESP: Xác thực + có mã hóa (thường được khai báo) 
- Confidentiality: Thuật toán mã hóa đối xứng 
- Integrity: 
 + MD5: hàm băm dữ liệu, bảo vệ tính đồng nhất của dữ liệu 
- Authentication: để xác thực PSK, RSA 2 bên bắt tay với nhau 
 + Preshare Key: 
 + RSA: 
- Secure Key Exchange: Dùng để mã hóa dữ liệu, tạo key 
 + DH1, DH2, DH5, DH7 
 
 Transport mode: chỉ vận chuyển, không thay dổi bất kỳ dữ liệu với gói tin ban đầu, chỉ thêm AH hoặc ESP 
 Tunnel mode: toàn bộ bản tin ban đầu, thêm 1 IP mới đòng toàn bộ bản tin ban đầu 
 
 -Trong thực tế thường sử dụng Tunnel mode và ESP
 
 IKE - là một tập hợp các quy định để thuật toán mã hóa và trao đổi các bản tin 
 OAKLEY: Thuật toán mã hóa 
 ISAKMP: Liên quan đến bản tin trao đổi, 
 SKEME: 
 - Khi cấu hình có 2 Phase 
 - Phase1 sẽ thiết lập tunnel dùng thuật toán trao đổi key 
 Sau Phase1 KT thì sẽ tạo Phase2
 Phase2 Thiết lập 1 tunnel bên trong Phase1 và dữ liệu được truyền đi trong Phase2 
 - Phải cho traffic nào đc đi qua tunnal VPN 
 - Phải trỏ được ESP Tunnel 
 - VTI: Tạo 


Trên Pfsense 
- Pre-Shared Key
- bedae8c225ca35c0232ec4a63bb966e9d5330ea230be77ed4eb9eae5


 
 
 
