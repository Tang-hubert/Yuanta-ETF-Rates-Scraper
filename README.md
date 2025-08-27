# Yuanta ETF Rates Scraper (元大投信ETF費率爬蟲)

這是一個 Python 腳本，用於爬取[元大投信ETF交易資訊網](https://www.yuantaetfs.com/TradeInfo/rate)上國內ETF的交易費率，並將結果儲存為 JSON 和 Excel 檔案。

此專案使用 `Selenium` 處理動態載入的 JavaScript 內容，並使用 `BeautifulSoup` 解析 HTML 結構。

## ✨ 功能

-   爬取指定網站的「國內ETF」交易費率表格。
-   擷取頁面上的「資料日期」，並將其包含在輸出中。
-   將爬取結果匯出為結構化的 `JSON` 檔案。
-   將表格資料匯出為以日期命名的 `Excel (.xlsx)` 檔案。
-   使用 `uv` 進行高效的虛擬環境和套件管理。

## 🚀 環境設定與使用方式

請遵循以下步驟來設定並執行此爬蟲。

### **先決條件**

1.  **Python 3.11.9**: 建議使用 `pyenv` 來管理 Python 版本。
2.  **uv**: 一個極速的 Python 套件安裝與管理工具。若尚未安裝，請執行：
    ```bash
    # macOS / Linux
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
    (Windows 和其他安裝方式請參考 [uv 官方文件](https://github.com/astral-sh/uv))
3.  **Google Chrome 瀏覽器**。
4.  **ChromeDriver**: 請下載與您 Chrome 瀏覽器版本相符的 ChromeDriver。
    -   **查詢您的 Chrome 版本**: 在網址列輸入 `chrome://version/`
    -   **下載 ChromeDriver**: 前往 [Chrome for Testing availability](https://googlechromelabs.github.io/chrome-for-testing/) 官方儀表板下載對應的版本。
    -   下載後，請將 `chromedriver` 執行檔解壓縮，並確保它位於您的系統 `PATH` 路徑中（例如 `/usr/local/bin` 或 `C:\Windows\System32`），或者您也可以在程式碼中直接指定其路徑。

### **安裝與執行**

1.  **複製儲存庫 (Clone the repository)**
    ```bash
    git clone <your-repository-url>
    cd yuanta-etf-scraper
    ```

2.  **建立並啟用虛擬環境**
    此專案使用 `uv` 來管理環境。
    ```bash
    # 建立一個名為 .venv 的虛擬環境
    uv venv

    # 啟用虛擬環境
    # macOS / Linux
    source .venv/bin/activate
    # Windows (Command Prompt)
    # .venv\Scripts\activate.bat
    ```

3.  **安裝依賴套件**
    ```bash
    uv pip install -r requirements.txt
    ```

4.  **執行爬蟲**
    ```bash
    python scrape_yuanta.py
    ```

## 📂 輸出結果

執行成功後，您將在專案根目錄下看到兩個檔案：

1.  **`yuanta_etf_rates.json`**: 一個包含資料日期和費率表格的 JSON 檔案。
    ```json
    {
        "data_date": "2025/08/27",
        "etf_rates": [
            {
                "基金名稱": "0050 元大台灣50",
                "申購交易費率 (%)": "0",
                "贖回交易費率 (%)": "0",
                ...
            }
        ]
    }
    ```

2.  **`yuanta_etf_rates_YYYY-MM-DD.xlsx`**: 一個以資料日期命名的 Excel 檔案，其中包含完整的費率表格。

---

## 🤖 專案的 Prompt Engineering 範本

這個專案的爬蟲程式碼是透過一個結構化的 Prompt 生成的。一個好的 Prompt 能夠讓 AI 更精準地理解需求，生成高品質、可維護的程式碼。

### **通用爬蟲 Prompt 格式**

```
# 角色
你現在是一位專業的 Python 爬蟲工程師。

# 任務
請使用 [程式語言] 和 [指定的函式庫] 撰寫一個網路爬蟲程式，用來擷取 [目標網站的 URL] 上的資料。

# 擷取資料欄位
我需要從網站上擷取以下具體的資料點：
*   **[資料點 1]**: [簡短描述，以及它在 HTML 中的位置，例如：HTML 標籤、class 或 id]
*   **[資料點 2]**: [簡短描述，以及它在 HTML 中的位置，例如：HTML 標籤、class 或 id]
*   ... (依此類推)

# 程式需求
*   [可選] 如果網站內容是動態載入的 (使用 JavaScript)，請使用 [例如：Selenium 或 Playwright] 來處理。
*   [可選] 請處理可能發生的錯誤，例如某些欄位資料缺失的情況。
*   [可選] 如果需要爬取多個頁面，請說明分頁的邏輯。

# 輸出格式
請將擷取到的資料儲存為 [例如：CSV 檔案、JSON 檔案或 Markdown 表格]。

# 範例 HTML 結構 (可選，但強烈建議)
為了讓您更清楚地了解，以下是目標網頁部分內容的 HTML 結構範例：
'''html
<!-- 在這裡貼上您從瀏覽器開發者工具中複製的相關 HTML 程式碼片段 -->
'''
```

### **本專案使用的實際 Prompt**

```
# 角色
你現在是一位專業的 Python 爬蟲工程師。

# 任務
請使用 [Python] 和 [BeautifulSoup/Selenium] 撰寫一個網路爬蟲程式，用來擷取 [https://www.yuantaetfs.com/TradeInfo/rate] 上的資料。

# 擷取資料欄位
我需要從網站上擷取以下具體的資料[ETF交易費率 & 國內ETF]點：
*   資料時間: `<div class="date" data-v-e56b41ba> <p data-v-e56b41ba> "資料日期" </p> </div>`
*   表格內所有內容: 表格完整項目:`<div class="eachBox on each_table" data-v-e56b41ba>`
  *   表頭欄位: [基金名稱、申購交易費率 (%)、贖回交易費率 (%)、每基數申贖手續費 (元)、預收申購金額 (%)、申購贖回截止時間、贖回價金交付日]
  *   每一列資料: 以 `<div data-v-e56b41ba class="tr"> </div>` 為單位，擷取所有欄位的字串與數值。

# 程式需求
*   網站內容是動態載入的 (使用 JavaScript)，請使用 Selenium 來處理。
*   請處理可能發生的錯誤，例如某些欄位資料缺失的情況。

# 輸出格式
請將擷取到的資料儲存為 JSON 檔案與 Excel 檔案。JSON 格式需要將「資料時間」放在外層，內部再包含整個表格資料。

```

## 📜 授權

本專案採用 [MIT License](LICENSE) 授權。