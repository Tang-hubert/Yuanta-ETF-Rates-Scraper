import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re # 匯入正規表達式模組

def scrape_yuanta_etf_rates():
    """
    使用 Selenium 和 BeautifulSoup 爬取元大投信國內ETF交易費率，
    擷取資料日期，並將結果儲存為結構化的 JSON 和以日期命名的 Excel 檔案。
    """
    url = "https://www.yuantaetfs.com/TradeInfo/rate"
    
    # --- Selenium 設定 ---
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        
        # 等待目標表格容器元素載入完成
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.eachBox.on.each_table"))
        )
        
        print("目標網頁已成功載入，開始解析 HTML...")
        
        # 取得網頁原始碼
        html_content = driver.page_source
        
        # --- BeautifulSoup 解析 ---
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # --- 新增功能：擷取資料日期 ---
        data_date_str = "未知日期" # 給定預設值
        date_element = soup.find('div', class_='date')
        if date_element and date_element.p:
            # 使用正規表達式找出日期格式 YYYY/MM/DD
            match = re.search(r'\d{4}/\d{2}/\d{2}', date_element.p.text)
            if match:
                data_date_str = match.group(0)
        print(f"成功擷取資料日期: {data_date_str}")
        
        # 找到指定的 "國內ETF" 表格容器
        domestic_etf_table = soup.find('div', class_='eachBox on each_table')
        
        if not domestic_etf_table:
            print("錯誤：找不到指定的國內ETF表格。")
            return

        # 擷取表頭 (Header)
        header_elements = domestic_etf_table.select('div.thead div.tr div.td')
        headers = [header.text.strip() for header in header_elements]
        
        print(f"成功擷取表頭: {headers}")

        # 準備儲存表格資料的列表
        etf_table_data = []

        # 擷取表格內容 (Body)
        rows = domestic_etf_table.select('div.tbody div.tr')
        
        print(f"找到 {len(rows)} 筆 ETF 資料，開始擷取...")

        for index, row in enumerate(rows):
            row_data = {}
            
            # 處理基金名稱欄位
            fund_name_element = row.find('div', class_='td tt')
            if fund_name_element:
                fund_code_p = fund_name_element.find('p')
                fund_name_p = fund_name_element.find('p', class_='name')
                
                if fund_code_p and fund_name_p:
                    fund_code = fund_code_p.text.strip()
                    fund_name = fund_name_p.text.strip()
                    row_data[headers[0]] = f"{fund_code} {fund_name}"
                    print(f"正在處理第 {index+1} 筆: {row_data[headers[0]]}")
                else:
                    row_data[headers[0]] = "N/A"
            else:
                row_data[headers[0]] = "N/A"

            # 處理該列的其他欄位
            other_cols = row.find_all('div', class_='td', recursive=False)[1:]
            
            for i, col in enumerate(other_cols):
                header_index = i + 1
                if header_index < len(headers):
                    if col.span:
                        col.span.decompose()
                    row_data[headers[header_index]] = col.text.strip()
                else:
                    row_data[f"未知欄位_{header_index}"] = col.text.strip()

            etf_table_data.append(row_data)

        # --- 輸出檔案 ---
        if etf_table_data:
            # --- 修改：建立包含日期和表格資料的最終輸出結構 ---
            final_output = {
                "data_date": data_date_str,
                "etf_rates": etf_table_data
            }

            # 儲存為 JSON 檔案
            with open('yuanta_etf_rates.json', 'w', encoding='utf-8') as f:
                json.dump(final_output, f, ensure_ascii=False, indent=4)
            print("資料已成功儲存至 yuanta_etf_rates.json")

            # 儲存為 Excel 檔案 (檔名包含日期)
            df = pd.DataFrame(etf_table_data)
            # 將日期中的斜線替換，以符合檔名規則
            filename_date = data_date_str.replace('/', '-')
            excel_filename = f'yuanta_etf_rates_{filename_date}.xlsx'
            df.to_excel(excel_filename, index=False, engine='openpyxl')
            print(f"資料已成功儲存至 {excel_filename}")
        else:
            print("沒有擷取到任何資料。")

    except Exception as e:
        print(f"爬取過程中發生錯誤: {e}")
    finally:
        # 關閉瀏覽器
        driver.quit()

if __name__ == '__main__':
    scrape_yuanta_etf_rates()