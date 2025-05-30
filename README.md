# Signature Verification System
Hệ thống xác thực chữ ký sử dụng các kỹ thuật xử lý ảnh tiên tiến để nhận diện và so sánh chữ ký viết tay.

# 🎯 Tính năng chính
- Xác thực chữ ký: So sánh chữ ký đầu vào với cơ sở dữ liệu

- Lưu trữ chữ ký: Thêm chữ ký mới vào hệ thống

- Cập nhật chữ ký: Chỉnh sửa thông tin chữ ký đã lưu

- Quản lý danh sách: Xem tất cả chữ ký trong hệ thống

# 🔧 Công nghệ sử dụng
## Xử lý ảnh
- **OpenCV**: Thư viện xử lý ảnh chính

- **scikit-image**: SSIM và Local Binary Pattern

- **NumPy**: Xử lý ma trận và mảng

## Backend
- **FastAPI**: Framework web async

- **PostgreSQL**: Cơ sở dữ liệu

- **asyncpg**: Driver PostgreSQL async