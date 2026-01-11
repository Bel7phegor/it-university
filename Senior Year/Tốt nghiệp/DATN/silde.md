KỊCH BẢN THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN TỐT NGHIỆP
(Bắt đầu trình chiếu Slide 1)

Slide 1: Trang tiêu đề
"Lời đầu tiên, em xin gửi lời chào đến quý Thầy Cô trong Hội đồng bảo vệ đồ án tốt nghiệp và các bạn. Em tên là [Tên của bạn]. Sau đây, em xin phép được trình bày báo cáo đồ án tốt nghiệp của mình với đề tài: 'Xây dựng hệ thống mạng doanh nghiệp ứng dụng tự động hóa với Ansible, giám sát bằng Prometheus và bảo mật với pfSense IDS/IPS'. Đề tài được thực hiện dưới sự hướng dẫn của [Tên giảng viên]."

Slide 2: Giới thiệu & Mục tiêu
"Kính thưa Hội đồng, xuất phát từ thực tế chuyển đổi số hiện nay, các doanh nghiệp đang đối mặt với 3 thách thức lớn trong quản trị hạ tầng mạng:

Quản trị thủ công: Việc cấu hình từng thiết bị rất tốn thời gian và dễ xảy ra sai sót do con người.

Thiếu giám sát tập trung: Khi có sự cố, quản trị viên mất nhiều thời gian để khoanh vùng lỗi do thiếu dữ liệu thống nhất.

An ninh thụ động: Các Firewall truyền thống thường không đủ khả năng chặn các cuộc tấn công tự động tốc độ cao.

Từ đó, em đề xuất giải pháp ứng dụng mô hình NetDevOps. Mục tiêu của đề tài là xây dựng một hệ thống tích hợp 3 yếu tố: Hạ tầng mạng phân vùng an toàn, Tự động hóa các tác vụ quản trị, và Giám sát - Cảnh báo chủ động."

Slide 3: Công nghệ cốt lõi & Kiến trúc
"Để hiện thực hóa mô hình NetDevOps này, em sử dụng các công nghệ mã nguồn mở hàng đầu hiện nay:

Về Automation, em chọn Ansible vì tính chất Agentless (không cần cài phần mềm lên thiết bị mạng), rất phù hợp để quản lý switch/router.

Về Giám sát, em sử dụng bộ đôi Prometheus và Grafana để thu thập metric hiệu năng.

Về Quản lý Log, em dùng Loki & Promtail để tập trung nhật ký hệ thống về một nơi.

Về Bảo mật, trái tim của hệ thống là pfSense tích hợp Suricata làm IDS/IPS.

Đặc biệt, em sử dụng Teleport để thay thế SSH truyền thống, giúp truy cập từ xa an toàn hơn."

Slide 4: Thiết kế mô hình mạng
"Mời thầy cô nhìn vào sơ đồ thiết kế mạng. Em đã xây dựng mô hình phân vùng 3 lớp điển hình:

Vùng WAN: Kết nối Internet.

Vùng DMZ: Chứa các Public Server như Web, Mail, được cách ly để giảm thiểu rủi ro cho mạng nội bộ.

Vùng LAN: Được chia thành các VLAN chức năng (Staff, Guest, Tech, Manager).

Tại hạ tầng Switch, em triển khai giao thức HSRP trên cặp Core Switch để đảm bảo tính sẵn sàng cao (High Availability), nếu một switch hỏng, hệ thống vẫn hoạt động bình thường.

Giao thức định tuyến OSPF được dùng để quảng bá tuyến động giữa các vùng."

Slide 5: Luồng dữ liệu hệ thống
"Để hệ thống vận hành trơn tru, em thiết kế 4 luồng dữ liệu chính:

Monitoring Flow: Prometheus sẽ chủ động 'kéo' (pull) dữ liệu metric từ các thiết bị thông qua giao thức SNMP hoặc Node Exporter.

Logging Flow: Các thiết bị mạng và server đẩy log qua Syslog đến Promtail, sau đó lưu trữ tại Loki.

Visualization Flow: Quản trị viên chỉ cần truy cập Grafana để xem toàn bộ dữ liệu này.

Automation Flow: Ansible Server sẽ đẩy các cấu hình hoặc lệnh backup xuống thiết bị thông qua kết nối SSH an toàn."

Slide 6: Triển khai hạ tầng & Bảo mật
"Đi sâu vào phần triển khai bảo mật trên pfSense:

Em sử dụng HAProxy làm Reverse Proxy, giúp ẩn thông tin server thật và cung cấp chứng chỉ SSL cho các dịch vụ nội bộ.

Quan trọng nhất là hệ thống IDS/IPS Suricata. Em cấu hình Suricata hoạt động ở chế độ IPS (Legacy Mode), cho phép nó đứng giữa luồng dữ liệu, phân tích gói tin dựa trên các bộ luật (Ruleset). Nếu phát hiện dấu hiệu tấn công như quét mạng hay khai thác lỗ hổng, nó sẽ lập tức Drop gói tin và Block IP tấn công."

Slide 7: Hệ thống giám sát (PLG Stack)
"Đối với hệ thống giám sát, em triển khai theo kiến trúc Microservices sử dụng Docker Compose. Bộ PLG Stack (Prometheus - Loki - Grafana) cho phép giám sát toàn diện:

Chúng ta biết được CPU, RAM của Server đang dùng bao nhiêu.

Biết được lưu lượng băng thông qua từng cổng Switch.

Và đọc được Log từ Firewall ngay trên Dashboard mà không cần SSH vào thiết bị.

Hệ thống cảnh báo (Alertmanager) được tích hợp để gửi tin nhắn về Telegram ngay khi có sự cố, ví dụ như Server bị Down hay Backup thất bại."

Slide 8: Tự động hóa (Ansible & Teleport)
"Về phần tự động hóa, đây là điểm nhấn giúp giảm tải công việc cho quản trị viên:

Em đã viết các Ansible Playbook để tự động sao lưu cấu hình (Backup) Cisco Switch và pfSense định kỳ hàng ngày.

Một kịch bản khác là tự động chặn IP (Block IP) khi phát hiện tấn công, biến hệ thống phòng thủ thành chủ động.

Ngoài ra, việc truy cập server được quản lý qua Teleport. Thay vì dùng SSH Key dễ bị lộ lọt, Teleport cấp quyền truy cập theo phiên, ghi lại toàn bộ thao tác lệnh của quản trị viên để phục vụ audit sau này."

Slide 9: Kết quả thực nghiệm
"Sau khi triển khai trên môi trường giả lập GNS3 kết hợp VMware, em đã thu được các kết quả khả quan:

Về giám sát: Dashboard Grafana hiển thị trực quan trạng thái toàn mạng theo thời gian thực.

Về tự động hóa: Hệ thống tự động gửi báo cáo PDF chứa thông tin log, traffic và trạng thái backup vào cuối ngày qua Telegram.

Về bảo mật: Em đã thực hiện tấn công giả lập bằng Nmap (quét port) và Hping3 (tấn công DoS).

Kết quả là Suricata đã phát hiện hành vi quét mạng và tự động đưa IP tấn công vào danh sách đen (Blacklist).

Server web vẫn hoạt động bình thường, chứng tỏ khả năng ngăn chặn tấn công từ chối dịch vụ hiệu quả."

Slide 10: Đánh giá & Hướng phát triển
"Qua quá trình thực hiện, em tự đánh giá hệ thống có các ưu điểm:

Mô hình toàn diện, khép kín quy trình vận hành.

Sử dụng 100% mã nguồn mở giúp tối ưu chi phí cho doanh nghiệp SMB.

Khả năng phản ứng sự cố nhanh nhờ tự động hóa.

Tuy nhiên, đề tài vẫn còn hạn chế là chưa triển khai cơ chế dự phòng (Cluster) cho chính server giám sát. Hướng phát triển tiếp theo em dự kiến là tích hợp AI/ML để phân tích Log, giúp phát hiện các bất thường mà Rule tĩnh không bắt được."

Slide 11: Kết luận
"Kính thưa Hội đồng, Đồ án đã xây dựng thành công mô hình mạng doanh nghiệp hiện đại theo hướng NetDevOps. Kết quả thực nghiệm chứng minh rằng việc kết hợp giữa Hạ tầng mạng truyền thống với các công cụ Tự động hóa và Giám sát hiện đại là hoàn toàn khả thi, giúp nâng cao hiệu quả quản trị và an toàn thông tin.

Em xin chân thành cảm ơn Thầy [Tên GVHD] đã tận tình hướng dẫn em hoàn thành đồ án này. Bài thuyết trình của em đến đây là kết thúc. Em rất mong nhận được những ý kiến đóng góp và câu hỏi từ quý Thầy Cô. Em xin cảm ơn!"