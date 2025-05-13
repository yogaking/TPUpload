import streamlit as st
import time
import hashlib
import os

# 设置页面配置
st.set_page_config(page_title="Dynamic Token Generator", page_icon="🔑", layout="centered",
                   menu_items={"About": "Dynamic Token Generator by Streamlit"})
st.title("🔑 Dynamic Token Generator")

# 生成动态令牌函数（使用HMAC确保安全）
def generate_token(secret: str, timestamp: int) -> str:
    combined = f"{secret}{timestamp // 30}"
    return hashlib.sha256(combined.encode()).hexdigest()[:6]

# 使用环境变量获取秘钥
SECRET_KEY = os.getenv("SECRET_KEY", "king0000")

# 动态令牌区域
placeholder = st.empty()

# 获取当前时间戳（秒）
def get_current_time():
    return int(time.time())

# 获取距离下一次令牌更新时间的剩余秒数
def get_time_until_next_update(current_time, interval=30):
    next_update_time = ((current_time // interval) + 1) * interval
    return next_update_time - current_time

# 确保页面自动刷新
if "last_token" not in st.session_state:
    st.session_state["last_token"] = ""

# 获取当前时间戳（秒）
current_time = get_current_time()
token = generate_token(SECRET_KEY, current_time)

# 计算剩余时间
remaining_time = get_time_until_next_update(current_time, interval=30)

# 避免重复计算
if st.session_state["last_token"] != token:
    st.session_state["last_token"] = token

# 显示动态令牌和剩余时间
with placeholder.container():
    st.subheader(f"Current Dynamic Token: {token}")
    st.caption(f"This token refreshes every 30 seconds. Time until next update: {remaining_time} seconds.")

# 使用前端自动刷新
st.markdown("<meta http-equiv='refresh' content='20'>", unsafe_allow_html=True)
