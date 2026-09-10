import streamlit as st
import pandas as pd

# Cấu hình trang
st.set_page_config(page_title="Tính Tiền Tiết Kiệm", page_icon="💰", layout="centered")

# Tiêu đề ứng dụng
st.title("💰 Ứng Dụng Tính Lãi Bằng Tiết Kiệm")
st.write("Nhập thông tin bên dưới để tính toán số tiền nhận được sau kỳ hạn gửi.")

# Chia bố cục nhập liệu thành các cột
col1, col2 = st.columns(2)

with col1:
    principal = st.number_input(
        "Số tiền gửi gốc (VNĐ):", 
        min_value=0, 
        value=100_000_000, 
        step=1_000_000, 
        format="%d"
    )
    months = st.number_input(
        "Số tháng gửi:", 
        min_value=1, 
        value=12, 
        step=1
    )

with col2:
    rate_year = st.number_input(
        "Lãi suất (%/năm):", 
        min_value=0.0, 
        value=6.0, 
        step=0.1, 
        format="%.2f"
    )
    interest_type = st.radio(
        "Hình thức tính lãi:",
        ["Lãi kép (Lãi nhập gốc)", "Lãi đơn"]
    )

# Quy đổi lãi suất và thời gian
# Lãi suất tháng (%)
rate_month = (rate_year / 100) / 12

# Nút tính toán
if st.button("🚀 Tính Số Tiền", use_container_width=True):
    if interest_type == "Lãi đơn":
        # Công thức lãi đơn: Tổng tiền = Gốc + (Gốc * Lãi suất tháng * Số tháng)
        interest_amount = principal * rate_month * months
        total_amount = principal + interest_amount
    else:
        # Công thức lãi kép (nhập gốc hàng tháng): Tổng tiền = Gốc * (1 + Lãi suất tháng)^Số tháng
        total_amount = principal * ((1 + rate_month) ** months)
        interest_amount = total_amount - principal

    st.markdown("---")
    st.subheader("📊 Kết quả tính toán")

    # Hiển thị các chỉ số chính bằng st.metric
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("Tiền gốc", f"{principal:,.0f} VNĐ")
    m_col2.metric("Tiền lãi nhận được", f"{interest_amount:,.0f} VNĐ")
    m_col3.metric("Tổng tiền thu về", f"{total_amount:,.0f} VNĐ")

    # Bảng chi tiết tăng trưởng theo từng tháng
    st.subheader("📈 Bảng chi tiết theo từng tháng")
    monthly_data = []
    current_balance = principal

    for month in range(1, months + 1):
        if interest_type == "Lãi đơn":
            m_interest = principal * rate_month
            current_balance += m_interest
            total_interest_so_far = m_interest * month
        else:
            m_interest = current_balance * rate_month
            current_balance += m_interest
            total_interest_so_far = current_balance - principal

        monthly_data.append({
            "Tháng": month,
            "Tiền lãi trong tháng (VNĐ)": round(m_interest),
            "Lãi cộng dồn (VNĐ)": round(total_interest_so_far),
            "Tổng số dư (VNĐ)": round(current_balance)
        })

    df = pd.DataFrame(monthly_data)
    
    # Định dạng hiển thị bảng số tiền có dấu phân cách hàng nghìn
    st.dataframe(
        df.style.format({
            "Tiền lãi trong tháng (VNĐ)": "{:,.0f}",
            "Lãi cộng dồn (VNĐ)": "{:,.0f}",
            "Tổng số dư (VNĐ)": "{:,.0f}"
        }),
        use_container_width=True
    )

    # Biểu đồ tăng trưởng
    st.line_chart(df.set_index("Tháng")["Tổng số dư (VNĐ)"])
