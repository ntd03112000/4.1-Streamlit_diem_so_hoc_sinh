# Edit Cònfigurations --> streamlit.exe --> ở phần Run ngay tại script
#                     --> C:/Users/dung/Desktop/AIO/.venv/Scripts/streamlit.exe
#                     --> dòng dưới run "4.1 Streamlit_Điem_so_hoc_sinh.py"(tức tên file python hiện tại)
# NHẤN SHIFT + F10 ĐỂ CHẠY
import io
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Viết title
st.title("Phân tích dữ liệu điểm số học sinh")

# Box upload file
uploaded_file = st.file_uploader("Tải file lên tại đây!", type=["xlsx"])


# Tính điểm trung bình
def diem_trung_binh(scores):
    return sum(scores) / len(scores)


#  Phân loại điểm
def phan_loai_diem(scores):
    stat = {"9-10": 0, "7-8.9": 0, "5-6.9": 0, "<5": 0}
    for score in scores:
        if score >= 9:
            stat["9-10"] += 1
        elif score >= 7:
            stat["7-8.9"] += 1
        elif score >= 5:
            stat["5-6.9"] += 1
        else:
            stat["<5"] += 1
    return stat


# LƯU Ý: KHÔNG THỂ THAY THẾ LÀ != NONE,...

if uploaded_file is not None:
    # Đọc file
    df = pd.read_excel(uploaded_file)

    # df["Điểm số"] -->Lấy một cột từ DataFrame,
    #                  Kiểu dữ liệu: pandas.Series
    # .dropna()     -->Bỏ các giá trị trống / NaN
    # .astype(float)-->Ép kiểu về số thực
    # .tolist()     -->Chuyển từ Series → list Python
    scores = df["Điểm số"].dropna().astype(float).tolist()

    st.write("Tổng số học sinh: ", len(scores))
    st.write("Điểm trung bình: ", round(diem_trung_binh(scores)))

    labels = list(phan_loai_diem(scores).keys())
    values = list(phan_loai_diem(scores).values())

    # Xóa trường hợp value = 0% --> không hiện lên biểu đồ
    index_values_remove = [values.index(a) for a in values if a == 0]
    for x in index_values_remove:
        labels.pop(x)
        values.pop(x)
    print(values)

    # plt.subplots()--> Tạo ra một figure (đối tượng chứa toàn bộ hình vẽ)
    #                   và một hoặc nhiều axes (trục tọa độ để vẽ biểu đồ)
    # fig           --> Là đối tượng Figure, đại diện cho toàn bộ khung
    #                   hình vẽ, có thể dùng fig để chỉnh sửa các thuộc
    #                   tính tổng thể (ví dụ: kích thước, tiêu đề chung,
    #                   lưu hình bằng fig.savefig()
    # ax            --> Là đối tượng Axes, chính là vùng biểu đồ nơi bạn
    #                   vẽ dữ liệu (ví dụ: ax.plot(), ax.scatter(), ax.bar())
    fig, ax = plt.subplots(figsize=(3, 3))

    ax.pie(values, labels=labels, autopct="%.1f%%", startangle=90)

    # buf = io.BytesIO() --> Có nghĩa là bạn tạo ra một buffer (bộ nhớ đệm)
    #                        nằm trong RAM để lưu trữ dữ liệu nhị phân
    #                        (binary data) thay vì ghi ra file trên ổ cứng.
    buf =io.BytesIO()

    # fig.savefig(buf, format="png", dpi=300) --> Lưu biểu đồ Matplotlib (fig)
    #                                             vào bộ nhớ tạm (buf) thay vì
    #                                             file trên ổ cứng.
    #                                             dpi=300 giúp ảnh sắc nét
    #                                             hơn (thường dùng khi xuất
    #                                             báo cáo).
    fig.savefig(buf, format="png",dpi=500) # Lưu với dpi cao để ảnh sắc nét

    # Image.open(buf)       --> Dùng thư viện Pillow để đọc ảnh từ buffer.
    img = Image.open(buf)

    # st.image(img, width=750)-->  Hiển thị ảnh trong ứng dụng Streamlit,
    #                              với chiều rộng 750 pixel. Đây là cách
    #                              Streamlit render ảnh đã lưu từ Matplotlib.
    st.image(img,width=750)
    st.markdown("Biểu đồ phân bố điểm số.")