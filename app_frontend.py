import streamlit as st
import urllib.request
import json

# 設定網頁標題與小圖示
st.set_page_config(page_title="我的專屬選股儀表板", page_icon="📈", layout="wide")

st.title("📈 我的行動選股 App 測試儀表板")
st.subheader("用純 Python 打造的手機/網頁雙用選股介面")

# ----------------------------------------------------
# 📡 核心：從我們剛剛建好的 FastAPI 去抓取最新 JSON 數據
# ----------------------------------------------------
@st.cache_data(ttl=2) # 讓網頁每2秒快取自動更新，才不會一直重抓
def fetch_api_data(endpoint):
    url = f"http://127.0.0.1:8000/{endpoint}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as res:
            return json.loads(res.read().decode('utf-8'))
    except Exception as e:
        return {"error": f"無法連接後端伺服器，請確保 app_api.py 還在黑畫面開著！\n詳細錯誤: {e}"}

# ----------------------------------------------------
# 🎛️ 前端介面：設計按鈕與功能切換
# ----------------------------------------------------
# 在左側欄建立一個好用的功能切換選單
option = st.sidebar.selectbox(
    '🎯 請選擇功能模組',
    ('🌐 首頁歡迎狀態', '📋 查看大腦完整股池', '🚨 跌破季線警示選股')
)

if option == '🌐 首頁歡迎狀態':
    st.info("💡 說明：這代表您的手機端成功向後端伺服器打招呼。")
    data = fetch_api_data("")
    st.write("🔧 後端回傳的原始資料：", data)
    
elif option == '📋 查看大腦完整股池':
    st.success("💡 說明：目前存在大腦 SQLite 資料庫裡的所有股票數據。")
    res_data = fetch_api_data("stocks")
    
    if "error" in res_data:
        st.error(res_data["error"])
    else:
        st.metric(label="📊 觀察個股總數", value=f"{res_data['count']} 檔")
        # 直接用 Streamlit 把 JSON 資料轉成高級的動態網頁表格！
        st.dataframe(res_data["data"], use_container_width=True)

elif option == '🚨 跌破季線警示選股':
    st.warning("💡 說明：App 選股引擎自動運算，單獨篩選出【目前現價 < 季線】的弱勢標的！")
    res_data = fetch_api_data("warning-stocks")
    
    if "error" in res_data:
        st.error(res_data["error"])
    else:
        st.metric(label="🔴 跌破季線警告股數", value=f"{res_data['warning_count']} 檔")
        
        # 顯示警示清單
        if res_data['warning_count'] == 0:
            st.balloons() # 沒股票跌破時放慶祝氣球！
            st.write("🟢 完美！目前沒有任何股票跌破季線，全數站在安全線上。")
        else:
            # 顯示表格，並放大呈現
            st.dataframe(res_data["data"], use_container_width=True)