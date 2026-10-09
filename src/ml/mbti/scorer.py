from typing import Any, Dict, List, Optional
from src.schemas.mbti_schema import (
    CareerTrajectoryItem,
    DimensionScore,
    MajorRecommendation,
    MBTIAnswerItem,
    MBTIQuestion,
    MBTIResultData,
)

MBTI_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "text": "Bạn hào hứng với việc thuyết trình, dẫn dắt đội nhóm và điều phối hiện trường công trình hơn là ngồi nghiên cứu tài liệu một mình.",
        "dimension": "EI",
        "positive_trait": "E",
        "context_field": "Kỹ năng điều hành & Quản lý",
    },
    {
        "id": 2,
        "text": "Bạn cảm thấy tập trung và làm việc hiệu quả nhất khi có không gian yên tĩnh để viết code, vẽ bản thiết kế hoặc giải toán kỹ thuật.",
        "dimension": "EI",
        "positive_trait": "I",
        "context_field": "Nghiên cứu & Lập trình",
    },
    {
        "id": 3,
        "text": "Khi gặp sự cố kỹ thuật hóc búa, xu hướng đầu tiên của bạn là thảo luận sôi nổi ngay với bạn bè và đồng nghiệp xung quanh.",
        "dimension": "EI",
        "positive_trait": "E",
        "context_field": "Giao tiếp & Phản biện",
    },
    {
        "id": 4,
        "text": "Bạn thường có xu hướng suy nghĩ độc lập và tự tìm giải pháp trước khi đưa ra ý kiến trong cuộc họp nhóm.",
        "dimension": "EI",
        "positive_trait": "I",
        "context_field": "Tư duy độc lập",
    },
    {
        "id": 5,
        "text": "Bạn thích các hoạt động giao thương, đàm phán hợp đồng cung ứng và mở rộng mạng lưới quan hệ đối tác logistics.",
        "dimension": "EI",
        "positive_trait": "E",
        "context_field": "Kinh tế & Chuỗi cung ứng",
    },
    {
        "id": 6,
        "text": "Bạn thích làm việc trực tiếp với máy móc cụ thể, số liệu đo đạc thực tế và tiêu chuẩn thi công rõ ràng hơn là các mô hình lý thuyết.",
        "dimension": "SN",
        "positive_trait": "S",
        "context_field": "Kỹ thuật cơ khí & Xây dựng",
    },
    {
        "id": 7,
        "text": "Bạn đam mê tìm hiểu các xu hướng công nghệ tương lai như Trí tuệ nhân tạo (AI), Xe tự hành, Robot thông minh và Thành phố thông minh.",
        "dimension": "SN",
        "positive_trait": "N",
        "context_field": "Công nghệ cao & AI",
    },
    {
        "id": 8,
        "text": "Bạn tin tưởng vào các quy trình kỹ thuật đã được thực chứng qua thời gian hơn là áp dụng ngay những giải pháp thử nghiệm chưa xác thực.",
        "dimension": "SN",
        "positive_trait": "S",
        "context_field": "Quy chuẩn & Kiểm định",
    },
    {
        "id": 9,
        "text": "Bạn thích phân tích bức tranh tổng thể, quy hoạch mạng lưới giao thông đô thị và dự báo xu hướng phát triển 5-10 năm tới.",
        "dimension": "SN",
        "positive_trait": "N",
        "context_field": "Quy hoạch & Tầm nhìn chiến lược",
    },
    {
        "id": 10,
        "text": "Bạn thường nảy ra nhiều ý tưởng độc đáo, sáng tạo ra các phương án thiết kế kiến trúc hoặc mô hình tối ưu mới lạ.",
        "dimension": "SN",
        "positive_trait": "N",
        "context_field": "Sáng tạo & Đổi mới",
    },
    {
        "id": 11,
        "text": "Khi đưa ra quyết định, bạn luôn ưu tiên tính chính xác toán học, độ an toàn chịu lực và hiệu quả kinh tế lên trên cảm tính cá nhân.",
        "dimension": "TF",
        "positive_trait": "T",
        "context_field": "Logic toán học & Tính toán kết cấu",
    },
    {
        "id": 12,
        "text": "Khi thiết kế công trình hoặc phát triển phần mềm, bạn đặc biệt quan tâm đến trải nghiệm tiện nghi, cảm xúc và sự hài lòng của người dùng.",
        "dimension": "TF",
        "positive_trait": "F",
        "context_field": "Trải nghiệm người dùng & Nhân văn",
    },
    {
        "id": 13,
        "text": "Bạn đánh giá cao các lập luận dựa trên dữ liệu định lượng, bằng chứng thực nghiệm và tư duy phản biện sắc bén.",
        "dimension": "TF",
        "positive_trait": "T",
        "context_field": "Khoa học dữ liệu & Phản biện",
    },
    {
        "id": 14,
        "text": "Bạn quan tâm sâu sắc đến việc bảo vệ môi trường, tính bền vững xã hội và giảm thiểu khí thải giao thông vì tương lai cộng đồng.",
        "dimension": "TF",
        "positive_trait": "F",
        "context_field": "Bền vững môi trường & Xã hội",
    },
    {
        "id": 15,
        "text": "Trong công việc kỹ thuật, sự công bằng, minh bạch và tuân thủ nghiêm ngặt quy chế quan trọng hơn việc nhân nhượng tình cảm.",
        "dimension": "TF",
        "positive_trait": "T",
        "context_field": "Kỷ luật & Nguyên tắc",
    },
    {
        "id": 16,
        "text": "Bạn luôn lập kế hoạch chi tiết, phân chia giai đoạn thi công rõ ràng và hoàn thành công việc trước hạn định deadline.",
        "dimension": "JP",
        "positive_trait": "J",
        "context_field": "Quản lý tiến độ dự án",
    },
    {
        "id": 17,
        "text": "Bạn có khả năng ứng biến nhanh nhạy, xử lý tốt các sự cố kỹ thuật phát sinh đột xuất ngay tại hiện trường.",
        "dimension": "JP",
        "positive_trait": "P",
        "context_field": "Xử lý sự cố & Ứng biến",
    },
    {
        "id": 18,
        "text": "Bạn luôn duy trì không gian làm việc ngăn nắp, hệ thống thư mục file tài liệu, bản vẽ kỹ thuật có cấu trúc bài bản.",
        "dimension": "JP",
        "positive_trait": "J",
        "context_field": "Tổ chức & Trật tự",
    },
    {
        "id": 19,
        "text": "Bạn thích để ngỏ các phương án để có thể thay đổi linh hoạt theo diễn biến thực tế của dự án.",
        "dimension": "JP",
        "positive_trait": "P",
        "context_field": "Thích ứng linh hoạt",
    },
    {
        "id": 20,
        "text": "Bạn cảm thấy yên tâm và làm việc tự tin nhất khi có hướng dẫn vận hành chuẩn (SOP) và quy trình từng bước rõ ràng.",
        "dimension": "JP",
        "positive_trait": "J",
        "context_field": "Quy trình chuẩn hóa",
    },
]

UTC_MAJORS_DATA: Dict[str, Dict[str, Any]] = {
    "7480201": {
        "name": "Công nghệ thông tin",
        "faculty": "Khoa Công nghệ thông tin",
        "degree_type": "Tích hợp Cử nhân - Kỹ sư (180 TC)",
        "career_prospects": [
            "Kỹ sư phát triển phần mềm, ứng dụng Web / Mobile",
            "Chuyên viên an toàn thông tin & Quản trị mạng",
            "Kiến trúc sư giải pháp CNTT trong giao thông thông minh",
        ],
    },
    "7480101": {
        "name": "Khoa học máy tính",
        "faculty": "Khoa Công nghệ thông tin",
        "degree_type": "Tích hợp Cử nhân - Kỹ sư (180 TC)",
        "career_prospects": [
            "Kỹ sư AI / Machine Learning & Khoa học Dữ liệu",
            "Chuyên gia phát triển thuật toán và tối ưu hóa hệ thống",
            "Chuyên gia nghiên cứu R&D công nghệ mới",
        ],
    },
    "7460112": {
        "name": "Toán ứng dụng",
        "faculty": "Khoa Khoa học cơ bản",
        "degree_type": "Cử nhân (140 TC)",
        "career_prospects": [
            "Chuyên viên phân tích định lượng tài chính & rủi ro",
            "Chuyên viên phân tích dữ liệu lớn (Data Analyst / Big Data)",
            "Chuyên gia tối ưu hóa mạng lưới vận tải",
        ],
    },
    "7520218": {
        "name": "Kỹ thuật robot và trí tuệ nhân tạo",
        "faculty": "Khoa Điện - Điện tử",
        "degree_type": "Tích hợp Cử nhân - Kỹ sư (180 TC)",
        "career_prospects": [
            "Kỹ sư thiết kế và điều khiển hệ thống Robot công nghiệp",
            "Kỹ sư thị giác máy tính và xe tự hành (Autonomous Vehicles)",
            "Kỹ sư tích hợp hệ thống tự động hóa thông minh",
        ],
    },
    "7520219": {
        "name": "Hệ thống giao thông thông minh",
        "faculty": "Khoa Điện - Điện tử / CNTT",
        "degree_type": "Tích hợp Cử nhân - Kỹ sư (180 TC)",
        "career_prospects": [
            "Kỹ sư vận hành Trung tâm điều hành giao thông đô thị (ITS)",
            "Chuyên viên phân tích hệ thống thu phí không dừng và giám sát an toàn",
            "Kỹ sư hạ tầng công nghệ số giao thông thông minh",
        ],
    },
    "7520216": {
        "name": "Kỹ thuật điều khiển và tự động hoá",
        "faculty": "Khoa Điện - Điện tử",
        "degree_type": "Tích hợp Cử nhân - Kỹ sư (180 TC)",
        "career_prospects": [
            "Kỹ sư lập trình điều khiển PLC, SCADA, DCS trong nhà máy",
            "Kỹ sư vận hành dây chuyền tự động hóa công nghiệp",
            "Chuyên gia thiết kế hệ thống điều khiển giao thông đường sắt / cảng biển",
        ],
    },
    "7520207": {
        "name": "Kỹ thuật điện tử - viễn thông",
        "faculty": "Khoa Điện - Điện tử",
        "degree_type": "Tích hợp Cử nhân - Kỹ sư (180 TC)",
        "career_prospects": [
            "Kỹ sư thiết kế phần cứng vi mạch, thiết bị IoT",
            "Kỹ sư tối ưu hóa mạng viễn thông không dây (5G/6G)",
            "Kỹ sư hệ thống thông tin tín hiệu đường sắt & hàng không",
        ],
    },
    "7520201": {
        "name": "Kỹ thuật điện",
        "faculty": "Khoa Điện - Điện tử",
        "degree_type": "Tích hợp Cử nhân - Kỹ sư (180 TC)",
        "career_prospects": [
            "Kỹ sư thiết kế và vận hành trạm biến áp, lưới điện quốc gia",
            "Kỹ sư năng lượng tái tạo (điện gió, điện mặt trời)",
            "Kỹ sư cung cấp điện công trình giao thông và đường sắt đô thị (Metro)",
        ],
    },
    "7520114": {
        "name": "Kỹ thuật cơ điện tử",
        "faculty": "Khoa Cơ khí",
        "degree_type": "Tích hợp Cử nhân - Kỹ sư (180 TC)",
        "career_prospects": [
            "Kỹ sư phát triển hệ thống cơ điện tử thông minh và cảm biến",
            "Kỹ sư tự động hóa dây chuyền sản xuất công nghiệp 4.0",
            "Kỹ sư R&D thiết bị y tế và máy bay không người lái (UAV)",
        ],
    },
    "7520130": {
        "name": "Kỹ thuật ô tô",
        "faculty": "Khoa Cơ khí",
        "degree_type": "Tích hợp Cử nhân - Kỹ sư (180 TC)",
        "career_prospects": [
            "Kỹ sư thiết kế, thử nghiệm và cải tiến xe ô tô & xe điện (EV)",
            "Kỹ sư giám sát quy trình sản xuất, lắp ráp tại các tập đoàn ô tô",
            "Chuyên gia kiểm định an toàn kỹ thuật phương tiện cơ giới",
        ],
    },
    "7520103": {
        "name": "Kỹ thuật cơ khí",
        "faculty": "Khoa Cơ khí",
        "degree_type": "Tích hợp Cử nhân - Kỹ sư (180 TC)",
        "career_prospects": [
            "Kỹ sư thiết kế chế tạo máy và thiết bị nâng chuyển",
            "Kỹ sư gia công cơ khí chính xác CNC và CAD/CAM/CAE",
            "Kỹ sư vận hành bảo dưỡng máy xây dựng công trình giao thông",
        ],
    },
    "7520116": {
        "name": "Kỹ thuật cơ khí động lực",
        "faculty": "Khoa Cơ khí",
        "degree_type": "Tích hợp Cử nhân - Kỹ sư (180 TC)",
        "career_prospects": [
            "Kỹ sư đầu máy - toa xe đường sắt và tàu điện cao tốc",
            "Kỹ sư máy tàu thủy và phương tiện giao thông chuyên dụng",
            "Chuyên gia thử nghiệm động cơ đốt trong và động cơ hybrid",
        ],
    },
    "7520115": {
        "name": "Kỹ thuật nhiệt",
        "faculty": "Khoa Cơ khí",
        "degree_type": "Tích hợp Cử nhân - Kỹ sư (180 TC)",
        "career_prospects": [
            "Kỹ sư thiết kế hệ thống điều hòa không khí và thông gió công trình (HVAC)",
            "Kỹ sư vận hành nhà máy nhiệt điện và quản lý năng lượng",
            "Chuyên viên kỹ thuật kho lạnh công nghiệp và chuỗi lạnh logistics",
        ],
    },
    "7580205": {
        "name": "Kỹ thuật xây dựng công trình giao thông",
        "faculty": "Khoa Công trình",
        "degree_type": "Tích hợp Cử nhân - Kỹ sư (180 TC)",
        "career_prospects": [
            "Kỹ sư thiết kế cầu đường bộ, cầu vượt nhịp lớn, đường cao tốc",
            "Chỉ huy trưởng công trường thi công cầu hầm, đường sắt tốc độ cao",
            "Chuyên gia tư vấn giám sát chất lượng công trình giao thông quốc gia",
        ],
    },
    "7580201": {
        "name": "Kỹ thuật xây dựng",
        "faculty": "Khoa Công trình",
        "degree_type": "Tích hợp Cử nhân - Kỹ sư (180 TC)",
        "career_prospects": [
            "Kỹ sư thiết kế kết cấu nhà cao tầng, công trình dân dụng & công nghiệp",
            "Kỹ sư quản lý thi công và an toàn lao động công trình",
            "Chuyên viên kiểm định chất lượng và thẩm tra thiết kế xây dựng",
        ],
    },
    "7580101": {
        "name": "Kiến trúc",
        "faculty": "Khoa Công trình",
        "degree_type": "Tích hợp Cử nhân - Kỹ sư (180 TC)",
        "career_prospects": [
            "Kiến trúc sư thiết kế công trình dân dụng, nhà ga, cầu cảnh quan",
            "Chuyên viên quy hoạch không gian kiến trúc cảnh quan đô thị",
            "Chuyên gia thiết kế nội thất và diễn họa 3D kiến trúc",
        ],
    },
    "7580210": {
        "name": "Kỹ thuật cơ sở hạ tầng",
        "faculty": "Khoa Công trình",
        "degree_type": "Tích hợp Cử nhân - Kỹ sư (180 TC)",
        "career_prospects": [
            "Kỹ sư quy hoạch và thiết kế hệ thống cấp thoát nước đô thị",
            "Kỹ sư công trình ngầm đô thị và hệ thống tuynel kỹ thuật",
            "Chuyên gia quản lý và bảo trì tài sản hạ tầng kỹ thuật thành phố",
        ],
    },
    "7580106": {
        "name": "Quản lý đô thị và công trình",
        "faculty": "Khoa Công trình",
        "degree_type": "Tích hợp Cử nhân - Kỹ sư (180 TC)",
        "career_prospects": [
            "Chuyên viên quản lý trật tự và quy hoạch phát triển đô thị",
            "Giám đốc quản lý vận hành tòa nhà cao tầng và khu đô thị thông minh",
            "Chuyên viên lập dự án đầu tư phát triển hạ tầng",
        ],
    },
    "7580202": {
        "name": "Kỹ thuật xây dựng công trình thuỷ",
        "faculty": "Khoa Công trình",
        "degree_type": "Tích hợp Cử nhân - Kỹ sư (180 TC)",
        "career_prospects": [
            "Kỹ sư thiết kế cảng biển, âu tàu, đường thủy nội địa",
            "Kỹ sư công trình chỉnh trị sông ngòi và chống xói lở bờ biển",
            "Chuyên viên kỹ thuật giàn khoan dầu khí và công trình biển",
        ],
    },
    "7510104": {
        "name": "Công nghệ kỹ thuật giao thông",
        "faculty": "Khoa Công trình",
        "degree_type": "Tích hợp Cử nhân - Kỹ sư (180 TC)",
        "career_prospects": [
            "Kỹ sư công nghệ thi công vật liệu mới trong hạ tầng giao thông",
            "Chuyên viên thí nghiệm kiểm định cơ lý đất đá và vật liệu xây dựng",
            "Kỹ sư tư vấn giải pháp kỹ thuật công trình giao thông",
        ],
    },
    "7520320": {
        "name": "Kỹ thuật môi trường",
        "faculty": "Khoa Môi trường và An toàn giao thông",
        "degree_type": "Tích hợp Cử nhân - Kỹ sư (180 TC)",
        "career_prospects": [
            "Kỹ sư thiết kế hệ thống xử lý nước thải, khí thải và chất thải rắn",
            "Chuyên gia đánh giá tác động môi trường (ĐTM) cho dự án hạ tầng",
            "Chuyên viên kiểm toán năng lượng và phát triển bền vững ESG",
        ],
    },
    "7510605": {
        "name": "Logistics và quản lý chuỗi cung ứng",
        "faculty": "Khoa Vận tải - Kinh tế / Cơ khí",
        "degree_type": "Cử nhân (140 TC)",
        "career_prospects": [
            "Chuyên viên điều phối vận tải đa phương thức quốc tế",
            "Quản lý kho bãi, trung tâm phân phối (Distribution Center)",
            "Chuyên gia hoạch định chuỗi cung ứng và mua hàng (Procurement)",
        ],
    },
    "7840101": {
        "name": "Khai thác vận tải",
        "faculty": "Khoa Vận tải - Kinh tế",
        "degree_type": "Cử nhân (140 TC)",
        "career_prospects": [
            "Điều độ viên khai thác vận tải đường bộ, đường sắt, hàng không",
            "Chuyên viên tổ chức điều hành mạng lưới xe buýt và metro đô thị",
            "Quản lý đội xe và an toàn giao thông doanh nghiệp vận tải",
        ],
    },
    "7840104": {
        "name": "Kinh tế vận tải",
        "faculty": "Khoa Vận tải - Kinh tế",
        "degree_type": "Cử nhân (140 TC)",
        "career_prospects": [
            "Chuyên viên phân tích giá cước và tài chính doanh nghiệp vận tải",
            "Chuyên viên lập phương án kinh doanh dịch vụ logistics",
            "Chuyên gia thẩm định dự án đầu tư phương tiện và tuyến vận tải",
        ],
    },
    "7580301": {
        "name": "Kinh tế xây dựng",
        "faculty": "Khoa Quản lý Xây dựng",
        "degree_type": "Tích hợp Cử nhân - Kỹ sư (180 TC)",
        "career_prospects": [
            "Kỹ sư định giá xây dựng (Quantity Surveyor - QS)",
            "Chuyên viên lập và thẩm tra dự toán, tổng mức đầu tư dự án",
            "Chuyên gia đấu thầu và quản lý hợp đồng xây dựng FIDIC",
        ],
    },
    "7580302": {
        "name": "Quản lý xây dựng",
        "faculty": "Khoa Quản lý Xây dựng",
        "degree_type": "Tích hợp Cử nhân - Kỹ sư (180 TC)",
        "career_prospects": [
            "Giám đốc quản lý dự án xây dựng (Project Manager)",
            "Chuyên viên giám sát tiến độ và chất lượng công trình",
            "Chuyên viên tư vấn quản trị rủi ro đầu tư bất động sản & hạ tầng",
        ],
    },
    "7340101": {
        "name": "Quản trị kinh doanh",
        "faculty": "Khoa Vận tải - Kinh tế",
        "degree_type": "Cử nhân (140 TC)",
        "career_prospects": [
            "Chuyên viên phát triển kinh doanh và chiến lược doanh nghiệp",
            "Quản lý tiếp thị số và truyền thông thương hiệu (Marketing)",
            "Khởi nghiệp và điều hành doanh nghiệp công nghệ / thương mại",
        ],
    },
    "7340201": {
        "name": "Tài chính - Ngân hàng",
        "faculty": "Khoa Vận tải - Kinh tế",
        "degree_type": "Cử nhân (140 TC)",
        "career_prospects": [
            "Chuyên viên tín dụng tài trợ dự án hạ tầng tại ngân hàng thương mại",
            "Chuyên viên phân tích đầu tư chứng khoán và quản lý quỹ",
            "Chuyên viên tài chính doanh nghiệp (Corporate Finance)",
        ],
    },
    "7340301": {
        "name": "Kế toán",
        "faculty": "Khoa Vận tải - Kinh tế",
        "degree_type": "Cử nhân (140 TC)",
        "career_prospects": [
            "Kế toán viên tổng hợp, kế toán dự án xây lắp công trình",
            "Kiểm toán viên nội bộ và kiểm toán độc lập tại các hãng kiểm toán",
            "Chuyên viên tư vấn chính sách thuế doanh nghiệp",
        ],
    },
    "7310101": {
        "name": "Kinh tế",
        "faculty": "Khoa Vận tải - Kinh tế",
        "degree_type": "Cử nhân (140 TC)",
        "career_prospects": [
            "Chuyên viên nghiên cứu và dự báo kinh tế vĩ mô",
            "Chuyên viên hoạch định chính sách phát triển vùng và giao thông",
            "Chuyên viên phân tích thị trường đầu tư tài chính",
        ],
    },
    "7810103": {
        "name": "Quản trị dịch vụ du lịch và lữ hành",
        "faculty": "Khoa Vận tải - Kinh tế",
        "degree_type": "Cử nhân (140 TC)",
        "career_prospects": [
            "Chuyên viên điều hành tour du lịch và lữ hành quốc tế",
            "Quản lý chuỗi dịch vụ vận chuyển hành khách du lịch chất lượng cao",
            "Chuyên viên marketing du lịch và sự kiện (MICE)",
        ],
    },
}

MBTI_PROFILES: Dict[str, Dict[str, Any]] = {
    "INTJ": {
        "type_name": "Nhà Kiến thiết Hệ thống (Mastermind)",
        "archetype_group": "Nhà Phân tích (Analysts)",
        "summary": "Bạn sở hữu tư duy chiến lược sắc bén, khả năng nhìn thấy cấu trúc phức tạp và khát khao tối ưu hóa các hệ sinh thái công nghệ quy mô lớn.",
        "strengths": [
            "Tư duy logic hệ thống sâu sắc và tầm nhìn dài hạn",
            "Khả năng thiết kế kiến trúc phần mềm và thuật toán phức tạp",
            "Độc lập, kiên định và quyết đoán dựa trên dữ liệu",
        ],
        "work_style": "Thích làm việc độc lập hoặc lãnh đạo chiến lược, giải quyết những bài toán kỹ thuật hóc búa nhất.",
        "suitable_environment": "Phòng thí nghiệm R&D, trung tâm thiết kế kiến trúc phần mềm, quy hoạch hệ thống giao thông thông minh.",
        "top_majors": [
            {"code": "7480101", "score": 98, "reason": "Tư duy toán thuật toán và AI là thế mạnh tự nhiên của INTJ."},
            {"code": "7480201", "score": 95, "reason": "Khả năng xây dựng kiến trúc hệ thống phần mềm quy mô lớn."},
            {"code": "7520218", "score": 92, "reason": "Phát triển thuật toán điều khiển cho Robot và xe tự hành."},
            {"code": "7520219", "score": 90, "reason": "Quy hoạch kiến trúc hệ thống giao thông thông minh tích hợp."},
        ],
    },
    "INTP": {
        "type_name": "Nhà Khoa học Tiên phong (Thinker)",
        "archetype_group": "Nhà Phân tích (Analysts)",
        "summary": "Bạn là người say mê khám phá chân lý khoa học, phân tích bản chất quy luật và tìm ra các phương pháp cải tiến đột phá.",
        "strengths": [
            "Khả năng trừu tượng hóa và mô hình hóa toán học xuất sắc",
            "Tư duy phản biện độc lập, không chấp nhận rập khuôn",
            "Năng khiếu bóc tách mã nguồn và tìm ra giải pháp cốt lõi",
        ],
        "work_style": "Yêu thích nghiên cứu sâu, phân tích dữ liệu lớn và tối ưu hóa giải thuật kỹ thuật.",
        "suitable_environment": "Viện nghiên cứu, các công ty công nghệ cao, môi trường thuật toán và công nghệ vi mạch.",
        "top_majors": [
            {"code": "7460112", "score": 97, "reason": "Tư duy toán học thuần túy và phân tích mô hình định lượng."},
            {"code": "7480101", "score": 95, "reason": "Nghiên cứu khoa học máy tính và các mô hình học sâu (Deep Learning)."},
            {"code": "7480201", "score": 91, "reason": "Lập trình backend chuyên sâu và an ninh mạng."},
            {"code": "7520207", "score": 88, "reason": "Nghiên cứu lý thuyết xử lý tín hiệu và vi mạch số."},
        ],
    },
    "ENTJ": {
        "type_name": "Nhà Điều hành Chiến lược (Commander)",
        "archetype_group": "Nhà Phân tích (Analysts)",
        "summary": "Bạn là thủ lĩnh bẩm sinh với quyết tâm cao độ, tầm nhìn bao quát và khả năng biến các dự án kỹ thuật đồ sộ thành hiện thực.",
        "strengths": [
            "Kỹ năng lãnh đạo, chỉ huy và ra quyết định dứt khoát",
            "Tổ chức dự án quy mô lớn với tiến độ và chi phí tối ưu",
            "Khả năng kết nối giữa công nghệ kỹ thuật và mục tiêu kinh doanh",
        ],
        "work_style": "Thích đứng ở vị trí điều hành, quản trị dự án, đàm phán hợp đồng lớn và dẫn dắt đội ngũ kỹ sư.",
        "suitable_environment": "Ban quản lý dự án hạ tầng lớn, tổng công ty xây dựng giao thông, tập đoàn công nghệ.",
        "top_majors": [
            {"code": "7580302", "score": 96, "reason": "Điều hành toàn diện các đại dự án xây dựng hạ tầng kỹ thuật."},
            {"code": "7510605", "score": 94, "reason": "Chiến lược quản trị chuỗi cung ứng và logistics đa phương thức."},
            {"code": "7340101", "score": 92, "reason": "Năng lực lãnh đạo doanh nghiệp và hoạch định chiến lược kinh doanh."},
            {"code": "7580205", "score": 89, "reason": "Chỉ huy trưởng thi công các tuyến cao tốc, cầu vượt nhịp lớn."},
        ],
    },
    "ENTP": {
        "type_name": "Nhà Đổi mới Công nghệ (Visionary)",
        "archetype_group": "Nhà Phân tích (Analysts)",
        "summary": "Bạn luôn tràn đầy năng lượng, đam mê đổi mới sáng tạo, yêu thích tranh biện trí tuệ và thử nghiệm những giải pháp đi trước thời đại.",
        "strengths": [
            "Tư duy đổi mới sáng tạo, nhìn ra cơ hội trong thách thức",
            "Kỹ năng giao tiếp và thuyết phục đồng đội tuyệt vời",
            "Thích ứng cực nhanh với các công nghệ mới nổi",
        ],
        "work_style": "Thích khởi nghiệp công nghệ, thử nghiệm nguyên mẫu (prototype) và giải quyết các bài toán liên ngành.",
        "suitable_environment": "Phòng thí nghiệm đổi mới sáng tạo, start-up công nghệ giao thông, tư vấn giải pháp kỹ thuật.",
        "top_majors": [
            {"code": "7520218", "score": 96, "reason": "Sáng tạo các ứng dụng Robot và giải pháp AI ứng dụng đột phá."},
            {"code": "7480201", "score": 93, "reason": "Phát triển các nền tảng ứng dụng công nghệ số thông minh."},
            {"code": "7510605", "score": 90, "reason": "Ứng dụng chuyển đổi số và công nghệ tự động hóa trong Logistics."},
            {"code": "7520114", "score": 88, "reason": "Phát triển các thiết bị cơ điện tử thông minh tích hợp IoT."},
        ],
    },
    "ISTJ": {
        "type_name": "Kỹ sư Kỷ luật & Trách nhiệm (Inspector)",
        "archetype_group": "Nhà Thực thi (Sentinels)",
        "summary": "Bạn là biểu tượng của sự chuẩn mực, tính kỷ luật cao, làm việc với độ tin cậy tuyệt đối và tôn trọng các tiêu chuẩn kỹ thuật khắt khe.",
        "strengths": [
            "Tỉ mỉ, cẩn trọng, kiểm soát sai số kỹ thuật cực kỳ chuẩn xác",
            "Tuân thủ quy chuẩn xây dựng, tiêu chuẩn an toàn và pháp luật",
            "Đáng tin cậy, trách nhiệm cao độ với cam kết công việc",
        ],
        "work_style": "Làm việc theo quy trình chuẩn hóa, tính toán bài bản từng bước, kiểm soát chất lượng chặt chẽ.",
        "suitable_environment": "Công trường xây dựng, ban kiểm định chất lượng công trình, phòng kế toán kiểm toán.",
        "top_majors": [
            {"code": "7580205", "score": 98, "reason": "Tính kỷ luật và độ an toàn chịu lực là sinh mệnh của ngành Cầu đường."},
            {"code": "7580301", "score": 95, "reason": "Định giá dự toán chi tiết, minh bạch và chính xác theo định mức."},
            {"code": "7340301", "score": 94, "reason": "Tuân thủ chặt chẽ chuẩn mực kế toán và pháp luật tài chính."},
            {"code": "7580201", "score": 92, "reason": "Thiết kế kết cấu bê tông cốt thép và quản lý thi công chuẩn mực."},
        ],
    },
    "ISFJ": {
        "type_name": "Người Bảo vệ & Tận tâm (Protector)",
        "archetype_group": "Nhà Thực thi (Sentinels)",
        "summary": "Bạn chu đáo, kiên nhẫn, luôn hướng đến việc phụng sự an toàn và chăm lo chu toàn cho cộng đồng và hệ thống hạ sinh thái.",
        "strengths": [
            "Quan tâm sâu sắc đến an toàn lao động và sức khỏe môi trường",
            "Kiên trì, tỉ mỉ trong việc giám sát và duy trì trật tự",
            "Lắng nghe, thấu cảm và hỗ trợ đồng đội tận tụy",
        ],
        "work_style": "Thích môi trường ổn định, công việc có ý nghĩa bảo vệ sức khỏe con người và cộng đồng.",
        "suitable_environment": "Ban an toàn lao động, trung tâm kiểm định môi trường, phòng quản trị dịch vụ du lịch lữ hành.",
        "top_majors": [
            {"code": "7520320", "score": 96, "reason": "Bảo vệ môi trường sống, kiểm soát ô nhiễm nước thải và khí thải giao thông."},
            {"code": "7580210", "score": 91, "reason": "Quản lý hạ tầng cấp thoát nước và môi trường sống dân sinh."},
            {"code": "7810103", "score": 89, "reason": "Chăm sóc trải nghiệm du khách và tổ chức dịch vụ tận tâm."},
            {"code": "7340301", "score": 87, "reason": "Quản lý chứng từ sổ sách minh bạch và chu toàn."},
        ],
    },
    "ESTJ": {
        "type_name": "Chỉ huy Trưởng Hiện trường (Executive)",
        "archetype_group": "Nhà Thực thi (Sentinels)",
        "summary": "Bạn có năng lực tổ chức trật tự xuất sắc, kỷ luật thép, giao tiếp rõ ràng và thúc đẩy cả công trường làm việc đúng tiến độ.",
        "strengths": [
            "Năng lực điều hành hiện trường thi công và giao việc dứt khoát",
            "Tối ưu hóa quy trình, loại bỏ lãng phí và đảm bảo trật tự",
            "Thực tế, coi trọng kết quả cụ thể và độ bền vững thực tế",
        ],
        "work_style": "Chỉ huy trực tiếp tại công trường, điều hành chuỗi cung ứng, điều động phương tiện vận tải nhịp nhàng.",
        "suitable_environment": "Hiện trường thi công cầu đường, trung tâm logistics cảng biển, tổng công ty xây dựng.",
        "top_majors": [
            {"code": "7580205", "score": 97, "reason": "Chỉ huy công trường cầu đường, hầm đường bộ quy mô lớn."},
            {"code": "7840101", "score": 95, "reason": "Tổ chức điều hành luồng tuyến vận tải và điều độ đội xe nhịp nhàng."},
            {"code": "7580302", "score": 93, "reason": "Giám sát tiến độ, hợp đồng và chất lượng thi công dự án."},
            {"code": "7510605", "score": 90, "reason": "Tổ chức vận hành kho bãi và mạng lưới phân phối logistics."},
        ],
    },
    "ESFJ": {
        "type_name": "Người Điều phối Kết nối (Consul)",
        "archetype_group": "Nhà Thực thi (Sentinels)",
        "summary": "Bạn thân thiện, giàu lòng hợp tác, giỏi xây dựng tinh thần đồng đội và tổ chức các dịch vụ phục vụ con người hiệu quả.",
        "strengths": [
            "Kỹ năng kết nối con người và tạo dựng môi trường làm việc tích cực",
            "Tổ chức sự kiện, chăm sóc khách hàng và đối tác chu đáo",
            "Tôn trọng cam kết, giữ chữ tín trong giao dịch kinh doanh",
        ],
        "work_style": "Thích làm việc trực tiếp với khách hàng, quản trị nhân sự và điều hành dịch vụ công chúng.",
        "suitable_environment": "Khách sạn, công ty lữ hành, phòng kinh doanh vận tải, ban quan hệ đối ngoại.",
        "top_majors": [
            {"code": "7810103", "score": 97, "reason": "Tổ chức dịch vụ lữ hành, sự kiện và chăm sóc khách du lịch hoàn hảo."},
            {"code": "7340101", "score": 93, "reason": "Quản trị quan hệ khách hàng và tiếp thị dịch vụ vận tải."},
            {"code": "7840104", "score": 89, "reason": "Kinh doanh dịch vụ vận chuyển hành khách và chăm sóc đối tác."},
            {"code": "7340201", "score": 87, "reason": "Tư vấn tài chính khách hàng cá nhân và doanh nghiệp."},
        ],
    },
    "ISTP": {
        "type_name": "Bậc thầy Kỹ thuật Cơ khí (Craftsman)",
        "archetype_group": "Nhà Khám phá (Explorers)",
        "summary": "Bạn có đôi bàn tay khéo léo, tư duy cơ học nhạy bén, đam mê tháo lắp, sửa chữa và tối ưu hóa các cỗ máy phức tạp.",
        "strengths": [
            "Hiểu sâu sắc nguyên lý cơ khí, động cơ đốt trong và hệ thống truyền lực",
            "Bình tĩnh tuyệt đối khi chẩn đoán và khắc phục sự cố máy móc",
            "Thực tế, thích tự tay thao tác lắp ráp thực nghiệm hơn lý thuyết",
        ],
        "work_style": "Làm việc với công cụ, thiết bị chẩn đoán, xe cộ, robot cơ khí và các hệ thống máy móc chuyển động.",
        "suitable_environment": "Xưởng sản xuất ô tô, trung tâm bảo dưỡng máy bay/tàu hỏa, phòng thí nghiệm động lực học.",
        "top_majors": [
            {"code": "7520130", "score": 99, "reason": "Đam mê thiết kế, chẩn đoán động cơ và nâng cấp xe ô tô/xe điện."},
            {"code": "7520103", "score": 96, "reason": "Chế tạo máy móc, gia công cơ khí chính xác và thiết bị nâng chuyển."},
            {"code": "7520116", "score": 94, "reason": "Kỹ thuật đầu máy toa xe và phương tiện động lực chuyên dụng."},
            {"code": "7520114", "score": 91, "reason": "Kết hợp hoàn hảo giữa cơ khí tinh vi và vi mạch điều khiển."},
        ],
    },
    "ISFP": {
        "type_name": "Kiến trúc sư Không gian Nghệ thuật (Artist)",
        "archetype_group": "Nhà Khám phá (Explorers)",
        "summary": "Bạn sở hữu cảm quan thẩm mỹ tinh tế, yêu cái đẹp hài hòa và mong muốn tạo dựng những công trình giàu cảm xúc thẩm mỹ.",
        "strengths": [
            "Cảm thụ không gian, màu sắc, ánh sáng và vật liệu tinh tế",
            "Tư duy tạo hình kiến trúc gắn liền với thiên nhiên và con người",
            "Linh hoạt, lắng nghe và tôn trọng tính độc bản của thiết kế",
        ],
        "work_style": "Làm việc với bản vẽ phối cảnh 3D, mô hình kiến trúc và thiết kế cảnh quan không gian đô thị.",
        "suitable_environment": "Văn phòng kiến trúc, công ty thiết kế nội thất cảnh quan, xưởng sáng tác.",
        "top_majors": [
            {"code": "7580101", "score": 99, "reason": "Khả năng sáng tạo kiến trúc công trình và cầu cảnh quan giàu thẩm mỹ."},
            {"code": "7580106", "score": 92, "reason": "Quy hoạch không gian đô thị hài hòa, xanh và đáng sống."},
            {"code": "7580210", "score": 87, "reason": "Thiết kế cảnh quan công viên, hạ tầng xanh đô thị."},
            {"code": "7520320", "score": 85, "reason": "Tạo dựng môi trường sinh thái bền vững cho cộng đồng."},
        ],
    },
    "ESTP": {
        "type_name": "Chuyên gia Hành động & Ứng biến (Dynamo)",
        "archetype_group": "Nhà Khám phá (Explorers)",
        "summary": "Bạn tràn đầy năng lượng, dũng cảm, phản xạ cực nhanh trước sự cố và thích đối mặt với thử thách ngoài hiện trường thực địa.",
        "strecripts": [],
        "strengths": [
            "Phản xạ xử lý khủng hoảng và sự cố hiện trường xuất sắc",
            "Dám nghĩ dám làm, không ngại lăn xả vào những công trình hiểm trở",
            "Năng động, đàm phán linh hoạt và giải quyết tình huống nhanh gọn",
        ],
        "work_style": "Không thích ngồi bàn giấy, luôn có mặt tại tuyến đường hầm, cầu cảng đang thi công hoặc trạm điều độ.",
        "suitable_environment": "Hiện trường thi công cao tốc hẻo lánh, bến cảng container tấp nập, đội cứu hộ kỹ thuật.",
        "top_majors": [
            {"code": "7580205", "score": 96, "reason": "Thi công vượt sông lớn, xuyên hầm núi hiểm trở đầy thử thách."},
            {"code": "7840101", "score": 93, "reason": "Ứng phó linh hoạt trong điều độ luồng tuyến vận tải phức tạp."},
            {"code": "7520130", "score": 90, "reason": "Thử nghiệm xe thực địa (test drive) và kiểm tra vận hành khắc nghiệt."},
            {"code": "7580202", "score": 88, "reason": "Thi công công trình thủy, đê chắn sóng và công trình biển gian nan."},
        ],
    },
    "ESFP": {
        "type_name": "Đại sứ Năng động & Trải nghiệm (Performer)",
        "archetype_group": "Nhà Khám phá (Explorers)",
        "summary": "Bạn nhiệt huyết, cởi mở, giàu năng lượng truyền cảm hứng và luôn muốn mang lại trải nghiệm sống động, hấp dẫn cho mọi người.",
        "strengths": [
            "Kỹ năng thuyết trình, hoạt náo và truyền lửa tự nhiên",
            "Nhanh nhạy nắm bắt tâm lý khách hàng và xu hướng thị trường",
            "Linh hoạt, hòa đồng và thích nghi dễ dàng với môi trường mới",
        ],
        "work_style": "Thích giao tiếp với khách hàng, quảng bá dịch vụ, tổ chức các tour du lịch trải nghiệm hấp dẫn.",
        "suitable_environment": "Trung tâm dịch vụ du lịch, hãng hàng không, phòng marketing sự kiện giải trí.",
        "top_majors": [
            {"code": "7810103", "score": 98, "reason": "Ngành du lịch lữ hành là sân khấu tỏa sáng của năng lượng ESFP."},
            {"code": "7340101", "score": 92, "reason": "Quảng bá thương hiệu, tiếp thị sản phẩm và dịch vụ sáng tạo."},
            {"code": "7840104", "score": 88, "reason": "Phát triển các gói dịch vụ vận chuyển du khách trải nghiệm cao cấp."},
            {"code": "7310101", "score": 84, "reason": "Nắm bắt tâm lý hành vi người tiêu dùng và phân tích thị trường."},
        ],
    },
    "INFJ": {
        "type_name": "Nhà Tư tưởng & Khát vọng Xã hội (Counselor)",
        "archetype_group": "Nhà Ngoại giao (Diplomats)",
        "summary": "Bạn có tầm nhìn xa trông rộng, lý tưởng cao đẹp về một xã hội văn minh, an toàn và phát triển bền vững trong tương lai.",
        "strengths": [
            "Thấu hiểu sâu sắc tác động xã hội lâu dài của các chính sách",
            "Khả năng nghiên cứu quy hoạch giao thông nhân văn và thông minh",
            "Kiên trì, tận tụy theo đuổi các giải pháp công ích vì con người",
        ],
        "work_style": "Nghiên cứu chiến lược quy hoạch, hoạch định chính sách phát triển bền vững và đào tạo giáo dục.",
        "suitable_environment": "Viện chiến lược giao thông, tổ chức phi chính phủ (NGO), viện quy hoạch đô thị.",
        "top_majors": [
            {"code": "7580106", "score": 97, "reason": "Hoạch định thành phố thông minh phục vụ cuộc sống hạnh phúc của cư dân."},
            {"code": "7520320", "score": 95, "reason": "Kiến tạo môi trường sống trong lành và giao thông xanh không phát thải."},
            {"code": "7310101", "score": 90, "reason": "Nghiên cứu kinh tế phát triển và chính sách giao thông công cộng bình đẳng."},
            {"code": "7580101", "score": 88, "reason": "Thiết kế kiến trúc đô thị giàu tính nhân văn và bản sắc văn hóa."},
        ],
    },
    "INFP": {
        "type_name": "Nhà Sáng tạo Nhân bản (Healer)",
        "archetype_group": "Nhà Ngoại giao (Diplomats)",
        "summary": "Bạn giàu lòng trắc ẩn, yêu thích sự hài hòa giữa công nghệ và thiên nhiên, đề cao những giá trị đạo đức và nhân văn trong kỹ thuật.",
        "strengths": [
            "Tư duy độc đáo, giàu trí tưởng tượng và nhạy cảm với cái đẹp",
            "Tận tâm với các dự án phục vụ cộng đồng và bảo vệ hành tinh",
            "Tôn trọng sự đa dạng, chu đáo trong thiết kế công trình công cộng",
        ],
        "work_style": "Thích làm việc độc lập hoặc trong nhóm nhỏ có chung lý tưởng cao đẹp về bảo vệ môi trường.",
        "suitable_environment": "Văn phòng kiến trúc sinh thái, trung tâm bảo tồn di sản, tổ chức môi trường quốc tế.",
        "top_majors": [
            {"code": "7580101", "score": 96, "reason": "Sáng tạo những công trình kiến trúc xanh, hòa hợp tuyệt đối với tự nhiên."},
            {"code": "7520320", "score": 94, "reason": "Cống hiến hết mình cho các giải pháp bảo vệ đất, nước và không khí."},
            {"code": "7580210", "score": 89, "reason": "Thiết kế hạ tầng thân thiện với người đi bộ và người khuyết tật."},
            {"code": "7810103", "score": 86, "reason": "Phát triển mô hình du lịch sinh thái bảo vệ thiên nhiên bản địa."},
        ],
    },
    "ENFJ": {
        "type_name": "Người Dẫn dắt & Khởi xướng (Protagonist)",
        "archetype_group": "Nhà Ngoại giao (Diplomats)",
        "summary": "Bạn là người truyền cảm hứng mạnh mẽ, thấu hiểu con người, có tài gắn kết các kỹ sư và chuyên gia kinh tế cùng chung một mục tiêu.",
        "strengths": [
            "Kỹ năng lãnh đạo truyền cảm hứng và xây dựng văn hóa đội ngũ",
            "Khả năng truyền thông, giải thích các vấn đề kỹ thuật dễ hiểu với công chúng",
            "Tầm nhìn phát triển con người và tổ chức vững mạnh",
        ],
        "work_style": "Lãnh đạo các tổ chức giao thông, quản lý quan hệ cộng đồng trong các dự án hạ tầng lớn.",
        "suitable_environment": "Ban quản lý dự án cộng đồng, trung tâm truyền thông công nghệ, cơ quan đào tạo.",
        "top_majors": [
            {"code": "7340101", "score": 96, "reason": "Xây dựng đội ngũ nhân sự vững mạnh và văn hóa doanh nghiệp tiến bộ."},
            {"code": "7580106", "score": 92, "reason": "Quản lý phát triển cộng đồng đô thị gắn kết và văn minh."},
            {"code": "7810103", "score": 90, "reason": "Kết nối văn hóa, lãnh đạo các chương trình giao lưu du lịch quốc tế."},
            {"code": "7580302", "score": 88, "reason": "Điều phối hài hòa lợi ích giữa các bên liên quan trong dự án xây dựng."},
        ],
    },
    "ENFP": {
        "type_name": "Nhà Khởi nghiệp Đổi mới (Campaigner)",
        "archetype_group": "Nhà Ngoại giao (Diplomats)",
        "summary": "Bạn tràn đầy ý tưởng mới, nhiệt huyết, giao tiếp lôi cuốn và luôn muốn ứng dụng công nghệ để giải quyết các thách thức xã hội.",
        "strengths": [
            "Tư duy mở rộng, kết nối những ý tưởng dường như không liên quan",
            "Kỹ năng thuyết phục nhà đầu tư và truyền cảm hứng cộng đồng",
            "Linh hoạt, thích nghi nhanh với mô hình kinh doanh số mới",
        ],
        "work_style": "Thích khởi nghiệp các nền tảng công nghệ di chuyển (Mobility-as-a-Service), ứng dụng thông minh.",
        "suitable_environment": "Vườn ươm khởi nghiệp, công ty công nghệ giao thông thông minh, phòng sáng tạo kinh doanh.",
        "top_majors": [
            {"code": "7340101", "score": 95, "reason": "Khởi nghiệp kinh doanh mô hình mới trong thời đại kinh tế số."},
            {"code": "7480201", "score": 91, "reason": "Phát triển các ứng dụng phần mềm tiện ích cho người tiêu dùng."},
            {"code": "7510605", "score": 89, "reason": "Sáng tạo các giải pháp logistics chặng cuối (Last-mile delivery) mới lạ."},
            {"code": "7580101", "score": 87, "reason": "Sáng tạo không gian kiến trúc độc đáo, kích thích cảm hứng sáng tạo."},
        ],
    },
}


IN_DEPTH_MBTI_DATA: Dict[str, Dict[str, Any]] = {
    "INTJ": {
        "weaknesses": [
            "Đôi khi quá cầu toàn về mặt cấu trúc giải pháp, dẫn đến tiến độ bị chậm so với yêu cầu gấp",
            "Có xu hướng giải quyết bài toán độc lập, ít chủ động chia sẻ khó khăn với thành viên khác",
            "Thiếu kiên nhẫn khi phải lặp lại các quy trình thủ công mang tính hành chính",
        ],
        "teamwork_style": "Thích làm việc với các thành viên có năng lực chuyên môn cao, trao đổi súc tích và giải quyết việc dựa trên dữ liệu.",
        "leadership_style": "Lãnh đạo bằng tư duy chiến lược, định hướng kiến trúc tổng thể và trao toàn quyền chủ động thực thi cho cấp dưới.",
        "learning_style": "Tự nghiên cứu tài liệu kỹ thuật chuyên sâu, đào sâu bản chất toán học và thuật toán cốt lõi.",
        "career_trajectories": [
            {"phase": "Khởi đầu (1 - 2 năm)", "roles": ["Kỹ sư phát triển phần mềm Backend", "Kỹ sư dữ liệu Junior", "Kỹ sư thuật toán"], "milestone": "Làm chủ kiến trúc hệ thống và quy trình kỹ thuật chuẩn."},
            {"phase": "Phát triển (3 - 5 năm)", "roles": ["Kiến trúc sư giải pháp (Solution Architect)", "Tech Lead hệ thống", "Chuyên gia AI"], "milestone": "Thiết kế và tối ưu hóa hệ thống công nghệ quy mô lớn."},
            {"phase": "Chuyên gia (5+ năm)", "roles": ["Giám đốc công nghệ (CTO)", "Chuyên gia trưởng chuyển đổi số"], "milestone": "Quyết định toàn diện lộ trình công nghệ và chiến lược hệ thống."},
        ],
    },
    "INTP": {
        "weaknesses": [
            "Dễ sa đà vào tối ưu hóa lý thuyết vi mô mà quên mất thời hạn bàn giao dự án",
            "Thường cảm thấy nhàm chán khi hệ thống đã đi vào giai đoạn bảo trì ổn định",
            "Khó giải thích các ý tưởng kỹ thuật trừu tượng cho người không chuyên",
        ],
        "teamwork_style": "Đóng vai trò chuyên gia phản biện học thuật, chỉ ra các lỗ hổng logic tiềm ẩn trong thiết kế.",
        "leadership_style": "Lãnh đạo theo phong cách tự do học thuật, truyền cảm hứng khám phá chân lý kỹ thuật.",
        "learning_style": "Thực nghiệm độc lập, tháo rời và tái tạo lại các hệ thống phần mềm/phần cứng để hiểu bản chất.",
        "career_trajectories": [
            {"phase": "Khởi đầu (1 - 2 năm)", "roles": ["Kỹ sư nghiên cứu R&D", "Lập trình viên thuật toán", "Kỹ sư vi mạch"], "milestone": "Hoàn thiện kỹ năng nghiên cứu và giải quyết bài toán cốt lõi."},
            {"phase": "Phát triển (3 - 5 năm)", "roles": ["Chuyên gia nghiên cứu cao cấp", "Nhà khoa học dữ liệu (Data Scientist)", "Chuyên gia mật mã an ninh mạng"], "milestone": "Đề xuất các bằng sáng chế hoặc giải pháp công nghệ tiên phong."},
            {"phase": "Chuyên gia (5+ năm)", "roles": ["Trưởng phòng nghiên cứu & phát triển (Head of R&D)", "Giáo sư / Giảng viên cao cấp"], "milestone": "Dẫn dắt các đề tài nghiên cứu trọng điểm quốc gia."},
        ],
    },
    "ENTJ": {
        "weaknesses": [
            "Có xu hướng áp đặt tiêu chuẩn khắt khe lên đồng đội, dễ gây căng thẳng trong nhóm",
            "Đôi khi đánh giá thấp yếu tố cảm xúc và sự mệt mỏi của nhân sự hiện trường",
            "Khó chấp nhận sự thỏa hiệp về mặt chất lượng dự án",
        ],
        "teamwork_style": "Thích nắm quyền điều phối, phân chia công việc rõ ràng theo mốc thời gian và đòi hỏi kỷ luật cao.",
        "leadership_style": "Quyết đoán, truyền cảm hứng bằng kết quả thực tế, tập trung tuyệt đối vào mục tiêu chiến lược.",
        "learning_style": "Học qua các case-study thực tế, đồ án tổng hợp và tham gia các cuộc thi khởi nghiệp, dự án lớn.",
        "career_trajectories": [
            {"phase": "Khởi đầu (1 - 2 năm)", "roles": ["Kỹ sư quản lý dự án Junior", "Chuyên viên phân tích chuỗi cung ứng", "Trợ lý chỉ huy công trường"], "milestone": "Nắm vững quy trình quản lý dự án, tiến độ và chi phí."},
            {"phase": "Phát triển (3 - 5 năm)", "roles": ["Chỉ huy trưởng công trình", "Trưởng phòng vận hành Logistics", "Giám đốc dự án công nghệ"], "milestone": "Điều hành các dự án lớn từ khâu đấu thầu đến bàn giao."},
            {"phase": "Chuyên gia (5+ năm)", "roles": ["Giám đốc điều hành (CEO)", "Phó Tổng Giám đốc phụ trách kỹ thuật/vận hành"], "milestone": "Quản trị toàn diện chiến lược tăng trưởng và phát triển doanh nghiệp."},
        ],
    },
    "ENTP": {
        "weaknesses": [
            "Nảy ra quá nhiều ý tưởng mới cùng lúc nhưng dễ bỏ dở khâu hoàn thiện chi tiết",
            "Dễ tranh luận quá mức với giảng viên hoặc đồng đội chỉ để kiểm tra giới hạn logic",
            "Thiếu kiên nhẫn với các công việc mang tính lặp đi lặp lại hàng ngày",
        ],
        "teamwork_style": "Khuấy động tinh thần sáng tạo, đưa ra các góc nhìn đột phá giải quyết bế tắc kỹ thuật.",
        "leadership_style": "Khuyến khích đổi mới sáng tạo, mở đường cho những ý tưởng táo bạo chưa từng có tiền lệ.",
        "learning_style": "Học qua tranh luận phản biện, thử nghiệm các công nghệ mới nhất và giải đề bài mở.",
        "career_trajectories": [
            {"phase": "Khởi đầu (1 - 2 năm)", "roles": ["Kỹ sư giải pháp đổi mới sáng tạo", "Product Owner Junior", "Kỹ sư R&D Robot"], "milestone": "Tạo ra các nguyên mẫu (Prototype) giải pháp kỹ thuật khả thi."},
            {"phase": "Phát triển (3 - 5 năm)", "roles": ["Giám đốc sản phẩm công nghệ (Product Manager)", "Trưởng nhóm sáng tạo giải pháp"], "milestone": "Đưa sản phẩm công nghệ đột phá ra thị trường thành công."},
            {"phase": "Chuyên gia (5+ năm)", "roles": ["Nhà sáng lập Startup công nghệ", "Giám đốc đổi mới sáng tạo (Chief Innovation Officer)"], "milestone": "Xây dựng hệ sinh thái công nghệ và gọi vốn đầu tư thành công."},
        ],
    },
    "INFJ": {
        "weaknesses": [
            "Dễ bị kiệt sức tinh thần do quan tâm quá nhiều đến áp lực của người khác",
            "Khó từ chối các yêu cầu giúp đỡ dù bản thân đang quá tải deadline",
            "Đôi khi lý tưởng hóa quá mức tính nhân văn của các dự án kỹ thuật",
        ],
        "teamwork_style": "Lắng nghe sâu sắc, hòa giải xung đột trong nhóm và hướng tới mục tiêu phụng sự cộng đồng.",
        "leadership_style": "Lãnh đạo phục vụ (Servant Leadership), thấu hiểu tâm lý và hỗ trợ tối đa cho từng thành viên.",
        "learning_style": "Học hiệu quả khi hiểu được ý nghĩa xã hội và giá trị nhân văn của ngành học đối với cuộc sống.",
        "career_trajectories": [
            {"phase": "Khởi đầu (1 - 2 năm)", "roles": ["Kỹ sư môi trường đô thị", "Chuyên viên thiết kế trải nghiệm người dùng (UX)", "Kỹ sư an toàn giao thông"], "milestone": "Đóng góp các giải pháp giảm thiểu rủi ro và tăng tiện ích cho xã hội."},
            {"phase": "Phát triển (3 - 5 năm)", "roles": ["Chuyên gia tư vấn phát triển bền vững", "Trưởng nhóm nghiên cứu giải pháp xanh", "Chuyên gia an toàn giao thông đô thị"], "milestone": "Tham gia xây dựng các chính sách và tiêu chuẩn bền vững."},
            {"phase": "Chuyên gia (5+ năm)", "roles": ["Cố vấn chiến lược giao thông xanh", "Giám đốc phát triển bền vững (CSO)"], "milestone": "Định hướng các chương trình quốc gia về giao thông không phát thải."},
        ],
    },
    "INFP": {
        "weaknesses": [
            "Dễ cảm thấy nản lòng khi làm việc trong môi trường áp lực cao và cạnh tranh khốc liệt",
            "Khó đưa ra quyết định khi phải đánh đổi giữa tính nhân văn và hiệu quả kinh tế",
            "Ngại va chạm và có xu hướng né tránh các cuộc tranh luận căng thẳng",
        ],
        "teamwork_style": "Tạo bầu không khí hòa hợp, tôn trọng sự khác biệt cá nhân và bảo vệ các giá trị cốt lõi.",
        "leadership_style": "Dẫn dắt bằng sự chân thành, khích lệ tiềm năng ẩn giấu của từng cộng sự.",
        "learning_style": "Học theo cảm hứng cá nhân, kết hợp nghệ thuật, không gian mở và tính thẩm mỹ vào kỹ thuật.",
        "career_trajectories": [
            {"phase": "Khởi đầu (1 - 2 năm)", "roles": ["Kiến trúc sư ý tưởng", "Chuyên viên thiết kế cảnh quan", "Chuyên viên truyền thông tuyển sinh"], "milestone": "Hình thành phong cách sáng tác kiến trúc và tư duy thiết kế riêng biệt."},
            {"phase": "Phát triển (3 - 5 năm)", "roles": ["Kiến trúc sư chủ trì thiết kế", "Chuyên gia quy hoạch không gian nhân văn"], "milestone": "Chủ trì các đồ án công trình nhà ga, cầu cảnh quan mang tính biểu tượng."},
            {"phase": "Chuyên gia (5+ năm)", "roles": ["Kiến trúc sư trưởng", "Giám đốc nghệ thuật công trình"], "milestone": "Được công nhận qua các giải thưởng kiến trúc trong nước và quốc tế."},
        ],
    },
    "ENFJ": {
        "weaknesses": [
            "Có xu hướng nhận quá nhiều trách nhiệm cộng đồng vượt quá sức lực bản thân",
            "Dễ bị ảnh hưởng tâm lý khi xảy ra bất đồng nội bộ không thể hòa giải",
            "Đôi khi can thiệp quá sâu vào công việc của cấp dưới vì muốn giúp đỡ",
        ],
        "teamwork_style": "Kết nối các thành viên, truyền lửa nhiệt huyết và xây dựng văn hóa đội nhóm gắn kết chặt chẽ.",
        "leadership_style": "Lãnh đạo lôi cuốn (Charismatic Leadership), khích lệ tinh thần đồng đội hướng tới mục tiêu cao cả.",
        "learning_style": "Thảo luận nhóm, thuyết trình bảo vệ đồ án và tham gia các hoạt động ngoại khóa, đoàn hội.",
        "career_trajectories": [
            {"phase": "Khởi đầu (1 - 2 năm)", "roles": ["Chuyên viên phát triển nhân tài kỹ thuật", "Điều phối viên dự án hợp tác quốc tế", "Chuyên viên quan hệ doanh nghiệp"], "milestone": "Xây dựng mạng lưới kết nối đối tác và hỗ trợ sinh viên."},
            {"phase": "Phát triển (3 - 5 năm)", "roles": ["Trưởng phòng nhân sự tập đoàn kỹ thuật", "Giám đốc chương trình đào tạo & phát triển"], "milestone": "Xây dựng chiến lược phát triển nguồn nhân lực chất lượng cao."},
            {"phase": "Chuyên gia (5+ năm)", "roles": ["Giám đốc nhân sự (CHRO)", "Phó Hiệu trưởng / Lãnh đạo tổ chức giáo dục"], "milestone": "Định hướng văn hóa tổ chức và phát triển các thế hệ nhân tài kế cận."},
        ],
    },
    "ENFP": {
        "weaknesses": [
            "Dễ bị phân tâm bởi nhiều cơ hội mới trước khi kịp hoàn tất dự án hiện tại",
            "Không thích các công việc liên quan đến tính toán số liệu chi tiết kéo dài",
            "Dễ cảm thấy ngột ngạt trong các môi trường kỹ thuật quá gò bó theo khuôn mẫu",
        ],
        "teamwork_style": "Tạo nguồn năng lượng tích cực, liên tục đề xuất các phương án tiếp cận mới mẻ và độc đáo.",
        "leadership_style": "Lãnh đạo truyền cảm hứng, khuyến khích tự do thử nghiệm và đón nhận sự thay đổi.",
        "learning_style": "Học qua trải nghiệm thực địa, tham gia các ngày hội công nghệ và thử thách thiết kế nhanh.",
        "career_trajectories": [
            {"phase": "Khởi đầu (1 - 2 năm)", "roles": ["Chuyên viên Marketing dịch vụ vận tải số", "Chuyên viên truyền thông công nghệ", "Nhà sáng tạo nội dung số"], "milestone": "Lan tỏa các giải pháp công nghệ di chuyển thông minh đến cộng đồng."},
            {"phase": "Phát triển (3 - 5 năm)", "roles": ["Giám đốc Marketing công nghệ (CMO)", "Trưởng bộ phận trải nghiệm khách hàng (CX)"], "milestone": "Xây dựng các chiến dịch truyền thông thương hiệu giao thông quy mô lớn."},
            {"phase": "Chuyên gia (5+ năm)", "roles": ["Cố vấn chiến lược thương hiệu & trải nghiệm số", "Doanh nhân khởi nghiệp"], "milestone": "Xây dựng các nền tảng số có hàng triệu người dùng thường xuyên."},
        ],
    },
    "ISTJ": {
        "weaknesses": [
            "Có xu hướng kháng cự lại các phương pháp mới nếu chưa có quy chuẩn thực chứng",
            "Đôi khi cứng nhắc trong việc áp dụng quy chế, thiếu sự linh hoạt trong tình huống khẩn cấp",
            "Khó chấp nhận sự chậm trễ hoặc sai sót dù là nhỏ nhất của đồng đội",
        ],
        "teamwork_style": "Đảm bảo tính chính xác, thực hiện đúng cam kết về thời gian và tuân thủ tuyệt đối quy trình kỹ thuật.",
        "leadership_style": "Lãnh đạo theo nguyên tắc và sự gương mẫu, đề cao tính ổn định, tin cậy và minh bạch.",
        "learning_style": "Học theo giáo trình bài bản, giải bài tập kỹ thuật có hệ thống và ghi chép chi tiết.",
        "career_trajectories": [
            {"phase": "Khởi đầu (1 - 2 năm)", "roles": ["Kỹ sư kiểm định chất lượng công trình", "Kỹ sư giám sát thi công", "Chuyên viên kế toán tài chính vận tải"], "milestone": "Thành thạo các tiêu chuẩn quốc gia TCVN, ASTM và quy chuẩn kỹ thuật."},
            {"phase": "Phát triển (3 - 5 năm)", "roles": ["Kỹ sư trưởng kiểm định an toàn", "Trưởng phòng quản trị chất lượng (QA/QC)", "Kế toán trưởng công ty vận tải"], "milestone": "Đảm bảo chất lượng và hồ sơ pháp lý hoàn hảo cho các đại dự án."},
            {"phase": "Chuyên gia (5+ năm)", "roles": ["Giám đốc quản lý rủi ro và tuân thủ", "Chuyên gia giám định công trình quốc gia"], "milestone": "Thẩm định các dự án trọng điểm cấp nhà nước và quốc tế."},
        ],
    },
    "ISFJ": {
        "weaknesses": [
            "Thường chịu đựng áp lực một mình và ngại nói lên ý kiến trái chiều",
            "Dễ bị kiệt sức do vừa lo việc chuyên môn vừa hỗ trợ hậu cần cho cả nhóm",
            "Khó thích ứng ngay khi có sự thay đổi quy trình đột ngột từ cấp trên",
        ],
        "teamwork_style": "Chăm sóc chu đáo từng chi tiết kỹ thuật, hỗ trợ đồng đội âm thầm và giữ gìn sự gắn kết nội bộ.",
        "leadership_style": "Lãnh đạo bảo trợ, tạo dựng môi trường an toàn, ổn định và đầy đủ điều kiện làm việc cho cộng sự.",
        "learning_style": "Học tập kiên trì, từng bước làm chủ kiến thức nền tảng và tích lũy kinh nghiệm qua thực hành.",
        "career_trajectories": [
            {"phase": "Khởi đầu (1 - 2 năm)", "roles": ["Kỹ sư quản lý hồ sơ chất lượng công trình", "Chuyên viên điều hành dịch vụ logistics", "Chuyên viên an toàn lao động"], "milestone": "Vận hành trơn tru các quy trình hậu cần và đảm bảo an toàn tuyệt đối."},
            {"phase": "Phát triển (3 - 5 năm)", "roles": ["Trưởng phòng điều độ vận tải", "Trưởng ban an toàn vệ sinh lao động dự án"], "milestone": "Xây dựng hệ thống an toàn đạt chuẩn ISO quốc tế."},
            {"phase": "Chuyên gia (5+ năm)", "roles": ["Giám đốc vận hành hậu cần (Logistics Operations Director)", "Cố vấn an toàn công trình"], "milestone": "Tối ưu hóa chi phí vận hành và giữ vững văn hóa an toàn bền vững."},
        ],
    },
    "ESTJ": {
        "weaknesses": [
            "Dễ nóng vội và bực bội khi người khác làm việc chậm chạp hoặc không đúng quy trình",
            "Có thể tạo cảm giác áp đặt, thiếu đồng cảm với khó khăn cá nhân của nhân sự",
            "Thiếu kiên nhẫn khi phải lắng nghe các ý tưởng lý thuyết chưa thấy rõ tính khả thi",
        ],
        "teamwork_style": "Thiết lập trật tự, phân công nhiệm vụ cụ thể, theo dõi sát sao tiến độ và đốc thúc công việc.",
        "leadership_style": "Chỉ huy quyết liệt, kỷ luật thép, giải quyết dứt điểm các vướng mắc tại công trường và dự án.",
        "learning_style": "Học qua các dự án quản lý thực tế, thực hành điều phối hiện trường và xử lý số liệu tiến độ.",
        "career_trajectories": [
            {"phase": "Khởi đầu (1 - 2 năm)", "roles": ["Kỹ sư thi công hiện trường", "Chuyên viên quản lý chuỗi cung ứng", "Điều phối viên đội xe"], "milestone": "Quản lý tốt tổ đội thi công và luân chuyển hàng hóa không tắc nghẽn."},
            {"phase": "Phát triển (3 - 5 năm)", "roles": ["Chỉ huy phó / Chỉ huy trưởng công trình", "Trưởng phòng kế hoạch & tiến độ", "Giám đốc trung tâm phân phối"], "milestone": "Hoàn thành các dự án vượt tiến độ và tối ưu chi phí dự toán."},
            {"phase": "Chuyên gia (5+ năm)", "roles": ["Tổng chỉ huy dự án hạ tầng quốc gia", "Phó Tổng Giám đốc phụ trách thi công/vận hành"], "milestone": "Chỉ đạo các công trình trọng điểm quy mô hàng nghìn tỷ đồng."},
        ],
    },
    "ESFJ": {
        "weaknesses": [
            "Dễ bị căng thẳng khi môi trường làm việc xảy ra xung đột gay gắt",
            "Có xu hướng phụ thuộc vào sự công nhận và đánh giá của người xung quanh",
            "Khó đưa ra các quyết định xử lý kỷ luật nghiêm khắc đối với cấp dưới",
        ],
        "teamwork_style": "Xây dựng tinh thần đồng đội nồng ấm, quan tâm đến phúc lợi và sự an tâm của từng thành viên.",
        "leadership_style": "Lãnh đạo gắn kết, tạo động lực làm việc thông qua sự ghi nhận công bằng và chăm lo đời sống.",
        "learning_style": "Học nhóm, giao lưu trao đổi kiến thức với bạn bè và tham gia tích cực các hội thảo chuyên ngành.",
        "career_trajectories": [
            {"phase": "Khởi đầu (1 - 2 năm)", "roles": ["Chuyên viên chăm sóc khách hàng doanh nghiệp vận tải", "Chuyên viên quản lý hợp đồng logistics", "Điều phối viên dịch vụ khách hàng"], "milestone": "Xây dựng mối quan hệ tin cậy bền vững với các đối tác vận tải lớn."},
            {"phase": "Phát triển (3 - 5 năm)", "roles": ["Trưởng phòng dịch vụ khách hàng (Customer Service Manager)", "Trưởng phòng quan hệ đối tác logistics"], "milestone": "Nâng cao chỉ số hài lòng khách hàng (CSAT) và giữ chân đối tác chiến lược."},
            {"phase": "Chuyên gia (5+ năm)", "roles": ["Giám đốc quan hệ khách hàng chiến lược (Chief Customer Officer)", "Giám đốc đối ngoại"], "milestone": "Đàm phán và duy trì các liên minh logistics toàn cầu."},
        ],
    },
    "ISTP": {
        "weaknesses": [
            "Không thích các cam kết dài hạn ràng buộc hoặc các kế hoạch quá chi tiết từ trước",
            "Có xu hướng kiệm lời, ngại chia sẻ cảm xúc và đôi khi tạo cảm giác xa cách",
            "Dễ chán nản khi phải tuân theo các quy tắc hành chính mang tính hình thức",
        ],
        "teamwork_style": "Thực chiến, xắn tay áo vào giải quyết ngay các sự cố kỹ thuật hóc búa nhất tại hiện trường.",
        "leadership_style": "Lãnh đạo qua hành động thực tế (Lead by Example), không dài dòng lý thuyết, tập trung vào hiệu quả.",
        "learning_style": "Thực hành tại xưởng cơ khí, phòng thí nghiệm điện tử, tháo lắp máy móc thực tế và kiểm tra linh kiện.",
        "career_trajectories": [
            {"phase": "Khởi đầu (1 - 2 năm)", "roles": ["Kỹ sư vận hành & bảo dưỡng máy xây dựng", "Kỹ sư chẩn đoán kỹ thuật ô tô", "Kỹ sư cơ điện tử thực địa"], "milestone": "Chẩn đoán và khắc phục nhanh chóng mọi sự cố cơ - điện - thủy lực."},
            {"phase": "Phát triển (3 - 5 năm)", "roles": ["Trưởng nhóm kỹ thuật bảo dưỡng", "Chuyên gia hiệu chuẩn thiết bị chính xác", "Kỹ sư trưởng xưởng sản xuất"], "milestone": "Tối ưu hóa tuổi thọ thiết bị và giảm thiểu thời gian chết (Downtime) của dây chuyền."},
            {"phase": "Chuyên gia (5+ năm)", "roles": ["Chuyên gia cao cấp hệ thống thiết bị giao thông", "Giám đốc dịch vụ kỹ thuật"], "milestone": "Làm chủ công nghệ các dòng phương tiện hiện đại như tàu cao tốc, xe điện tự hành."},
        ],
    },
    "ISFP": {
        "weaknesses": [
            "Dễ cảm thấy áp lực khi bị giới hạn trong các khuôn mẫu kỹ thuật cứng nhắc",
            "Ngại va chạm và có xu hướng thu mình lại khi gặp phải sự chỉ trích gay gắt",
            "Khó lập kế hoạch tài chính hoặc thời gian biểu dài hạn chặt chẽ",
        ],
        "teamwork_style": "Đóng góp các góc nhìn thẩm mỹ tinh tế, tạo ra các sản phẩm công nghệ có trải nghiệm thị giác đẹp mắt.",
        "leadership_style": "Tôn trọng không gian sáng tạo cá nhân, hỗ trợ cộng sự phát triển phong cách độc đáo riêng.",
        "learning_style": "Học qua trực quan sinh động, mô hình 3D, bản vẽ phối cảnh và ứng dụng thực tế có tính mỹ thuật.",
        "career_trajectories": [
            {"phase": "Khởi đầu (1 - 2 năm)", "roles": ["Kiến trúc sư phối cảnh 3D", "Chuyên viên thiết kế giao diện ứng dụng (UI Designer)", "Kỹ sư thiết kế nội thất nhà ga/phương tiện"], "milestone": "Tạo ra các sản phẩm thiết kế có tính thẩm mỹ và công năng cao."},
            {"phase": "Phát triển (3 - 5 năm)", "roles": ["Trưởng nhóm thiết kế mỹ thuật công nghiệp", "Chuyên gia thiết kế nhận diện thương hiệu công trình"], "milestone": "Định hình ngôn ngữ thiết kế cho các dòng sản phẩm giao thông hiện đại."},
            {"phase": "Chuyên gia (5+ năm)", "roles": ["Giám đốc sáng tạo thiết kế (Design Director)", "Kiến trúc sư trưởng cảnh quan"], "milestone": "Tạo nên những dấu ấn kiến trúc giao thông giàu bản sắc và giá trị nghệ thuật."},
        ],
    },
    "ESTP": {
        "weaknesses": [
            "Có xu hướng hành động trước khi tính toán kỹ lưỡng mọi rủi ro tiềm ẩn",
            "Thiếu kiên nhẫn với các buổi họp dài dòng và các báo cáo lý thuyết khô khan",
            "Dễ bỏ qua các quy định an toàn nếu cảm thấy chúng làm chậm tiến độ xử lý việc",
        ],
        "teamwork_style": "Nhanh nhẹn, năng động, thúc đẩy hành động ngay tức khắc và phá tan các bế tắc trong công việc.",
        "leadership_style": "Chỉ huy thực chiến tại chỗ, phản ứng thần tốc với các biến cố phát sinh và chịu trách nhiệm cao.",
        "learning_style": "Học qua các tình huống mô phỏng khẩn cấp, đi thực tế tại các công trường và cảng biển sôi động.",
        "career_trajectories": [
            {"phase": "Khởi đầu (1 - 2 năm)", "roles": ["Kỹ sư giám sát an toàn hiện trường", "Điều độ viên khai thác cảng biển / nhà ga", "Kỹ sư thử nghiệm xe thử nghiệm"], "milestone": "Ứng phó xuất sắc trước mọi sự cố phát sinh tại hiện trường."},
            {"phase": "Phát triển (3 - 5 năm)", "roles": ["Trưởng ban điều hành hiện trường", "Giám đốc khai thác bến cảng", "Trưởng phòng vận tải đường bộ"], "milestone": "Nâng cao năng suất xếp dỡ và luân chuyển hàng hóa cảng biển lên mức kỷ lục."},
            {"phase": "Chuyên gia (5+ năm)", "roles": ["Giám đốc điều hành khai thác hạ tầng (COO)", "Phó Tổng Giám đốc vận hành cảng quốc tế"], "milestone": "Chỉ đạo các chiến lược khai thác logistics quy mô liên vùng."},
        ],
    },
    "ESFP": {
        "weaknesses": [
            "Dễ bị cuốn vào những niềm vui trước mắt mà lơ là các mục tiêu học tập dài hạn",
            "Không thích đối mặt với các số liệu phân tích khô khan, mang tính lặp đi lặp lại",
            "Dễ bối rối khi phải giải quyết các cuộc khủng hoảng kéo dài đòi hỏi sự kiên nhẫn cao",
        ],
        "teamwork_style": "Tạo niềm vui và động lực cho cả nhóm, biến các buổi làm việc kỹ thuật căng thẳng trở nên hào hứng.",
        "leadership_style": "Lãnh đạo truyền cảm hứng bằng năng lượng tích cực, đưa mọi người lại gần nhau và cùng tiến bước.",
        "learning_style": "Học qua thực tế tương tác, trò chơi hóa kiến thức (Gamification) và thuyết trình trước đám đông.",
        "career_trajectories": [
            {"phase": "Khởi đầu (1 - 2 năm)", "roles": ["Chuyên viên phát triển kinh doanh dịch vụ giao thông thông minh", "Chuyên viên truyền thông thương hiệu UTC", "Điều phối viên sự kiện công nghệ"], "milestone": "Quảng bá mạnh mẽ các thành tựu khoa học công nghệ giao thông đến đại chúng."},
            {"phase": "Phát triển (3 - 5 năm)", "roles": ["Trưởng phòng phát triển thị trường công nghệ", "Giám đốc quan hệ công chúng (PR Manager)"], "milestone": "Mở rộng thị phần các dịch vụ giao thông số và công nghệ vận tải mới."},
            {"phase": "Chuyên gia (5+ năm)", "roles": ["Giám đốc thương mại (Chief Commercial Officer)", "Phó Tổng Giám đốc kinh doanh & đối ngoại"], "milestone": "Định vị thương hiệu doanh nghiệp công nghệ giao thông hàng đầu thị trường."},
        ],
    },
}


from src.repositories.major_repository import major_repository
from src.ml.llm.loader import llm_client


def calculate_mbti_result(
    answers: List[MBTIAnswerItem],
    student_name: Optional[str] = None,
    session_id: Optional[str] = None,
    cccd: Optional[str] = None,
    include_ai_advice: bool = False,
) -> MBTIResultData:
    import uuid

    active_session_id = session_id or f"mbti_{uuid.uuid4().hex[:12]}"

    scores: Dict[str, float] = {
        "E": 0.0,
        "I": 0.0,
        "S": 0.0,
        "N": 0.0,
        "T": 0.0,
        "F": 0.0,
        "J": 0.0,
        "P": 0.0,
    }

    q_map = {q["id"]: q for q in MBTI_QUESTIONS}

    normalized_answers = (
        [MBTIAnswerItem(question_id=int(k), score=int(v)) for k, v in answers.items()]
        if isinstance(answers, dict)
        else answers
    )

    for ans in normalized_answers:
        q = q_map.get(ans.question_id)
        if not q:
            continue

        pos_trait = q["positive_trait"]
        dim = q["dimension"]
        if dim == "EI":
            neg_trait = "I" if pos_trait == "E" else "E"
        elif dim == "SN":
            neg_trait = "N" if pos_trait == "S" else "S"
        elif dim == "TF":
            neg_trait = "F" if pos_trait == "T" else "T"
        else:
            neg_trait = "P" if pos_trait == "J" else "J"

        val = ans.score
        if val == 5:
            scores[pos_trait] += 2.0
        elif val == 4:
            scores[pos_trait] += 1.0
        elif val == 3:
            scores[pos_trait] += 0.5
            scores[neg_trait] += 0.5
        elif val == 2:
            scores[neg_trait] += 1.0
        elif val == 1:
            scores[neg_trait] += 2.0

    def calc_pair_pct(a_val: float, b_val: float) -> tuple[float, float]:
        total = a_val + b_val
        if total == 0:
            return 50.0, 50.0
        pct_a = round((a_val / total) * 100, 1)
        pct_b = round(100.0 - pct_a, 1)
        return pct_a, pct_b

    e_pct, i_pct = calc_pair_pct(scores["E"], scores["I"])
    s_pct, n_pct = calc_pair_pct(scores["S"], scores["N"])
    t_pct, f_pct = calc_pair_pct(scores["T"], scores["F"])
    j_pct, p_pct = calc_pair_pct(scores["J"], scores["P"])

    letter_1 = "E" if e_pct >= i_pct else "I"
    letter_2 = "S" if s_pct >= n_pct else "N"
    letter_3 = "T" if t_pct >= f_pct else "F"
    letter_4 = "J" if j_pct >= p_pct else "P"

    mbti_type = f"{letter_1}{letter_2}{letter_3}{letter_4}"

    profile = MBTI_PROFILES.get(mbti_type)
    if not profile:
        profile = MBTI_PROFILES["INTJ"]

    recommended_majors: List[MajorRecommendation] = []
    for item in profile["top_majors"]:
        code = item["code"]
        db_major = major_repository.get_major(code)
        static_major = UTC_MAJORS_DATA.get(code, {})

        major_name = db_major["major_name"] if db_major else static_major.get("name", "Ngành đào tạo UTC")
        faculty = db_major["faculty"] if db_major else static_major.get("faculty", "Trường Đại học GTVT")
        faculty_code = db_major.get("faculty_code") if db_major else None
        benchmark_score = db_major.get("benchmark_score") if db_major else None
        benchmark_year = db_major.get("benchmark_year") if db_major else None
        degree_type = db_major.get("degree_type") if db_major else static_major.get("degree_type", "Cử nhân / Kỹ sư tích hợp")
        career_prospects = static_major.get("career_prospects", [])

        slug = {
            "7480201": "cntt",
            "7510605": "logistics",
            "7520216": "tu-dong-hoa",
            "7480101": "khoa-hoc-may-tinh",
            "7520218": "robot-ai",
            "7580205": "cau-duong",
            "7340101": "quan-tri-kinh-doanh",
            "7310101": "kinh-te",
        }.get(code, code)

        recommended_majors.append(
            MajorRecommendation(
                major_code=code,
                major_name=major_name,
                slug=slug,
                faculty=faculty,
                faculty_code=faculty_code,
                degree_type=degree_type,
                match_score=item["score"],
                reason=item["reason"],
                benchmark_score=benchmark_score,
                benchmark_year=benchmark_year,
                career_prospects=career_prospects,
            )
        )

    ai_advice = None
    if include_ai_advice:
        try:
            major_names = ", ".join([m.major_name for m in recommended_majors[:3]])
            prompt = (
                f"Thí sinh {student_name or 'bạn'} có nhóm tính cách {mbti_type} ({profile['type_name']}). "
                f"Các ngành phù hợp tại Đại học GTVT (UTC) là: {major_names}. "
                f"Hãy đóng vai chuyên gia tư vấn tuyển sinh UTC, viết 1 đoạn nhận xét ngắn (khoảng 3-4 câu) "
                f"truyền cảm hứng và phân tích lý do tính cách này sẽ phát huy tốt nhất tại UTC."
            )
            messages = [{"role": "user", "content": prompt}]
            resp = llm_client.generate(messages=messages, max_tokens=256, temperature=0.7)
            choices = resp.get("choices", [])
            if choices:
                ai_advice = choices[0].get("message", {}).get("content", "").strip()
        except Exception:
            ai_advice = None

    dimension_scores = DimensionScore(
        extraversion=e_pct,
        introversion=i_pct,
        sensing=s_pct,
        intuition=n_pct,
        thinking=t_pct,
        feeling=f_pct,
        judging=j_pct,
        perceiving=p_pct,
    )

    in_depth = IN_DEPTH_MBTI_DATA.get(mbti_type, IN_DEPTH_MBTI_DATA["INTJ"])

    trajectories = [
        CareerTrajectoryItem(
            phase=t["phase"],
            roles=t["roles"],
            milestone=t["milestone"],
        )
        for t in in_depth.get("career_trajectories", [])
    ]

    return MBTIResultData(
        result_id=None,
        student_name=student_name,
        session_id=active_session_id,
        cccd=cccd,
        mbti_type=mbti_type,

        type_name=profile["type_name"],
        archetype_group=profile["archetype_group"],
        personality_summary=profile["summary"],
        strengths=profile["strengths"],
        weaknesses=in_depth.get("weaknesses", []),
        work_style=profile["work_style"],
        teamwork_style=in_depth.get("teamwork_style"),
        leadership_style=in_depth.get("leadership_style"),
        learning_style=in_depth.get("learning_style"),
        suitable_environment=profile["suitable_environment"],
        dimension_scores=dimension_scores,
        recommended_majors=recommended_majors,
        career_trajectories=trajectories,
        ai_advice=ai_advice,
    )
