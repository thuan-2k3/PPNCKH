

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import calendar

# Tạo tùy chọn Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ẩn giao diện Chrome
chrome_options.add_argument("--disable-gpu")  # Tắt GPU (tăng hiệu suất trên một số hệ thống)
chrome_options.add_argument("--no-sandbox")  # Tùy chọn này cần thiết cho một số môi trường

# Khởi tạo dịch vụ Chrome và driver
chrome_service = ChromeService(executable_path='C:/Users/User/Desktop/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Đặt URL cơ bản
base_url = "https://meteostat.net/en/place/vn/quan-tan-phu?s=48900&t={}-{:02d}-{:02d}/{:02d}-{:02d}-{:02d}"

# Định nghĩa ngày bắt đầu
start_year = 2021
start_month = 6
start_day = 14

# Lặp qua từng năm từ 1991 đến 2024
for year in range(start_year, 2025):  # Đến hết năm 2024
    if year == start_year:
        month_range = range(start_month, 13)  # Bắt đầu từ tháng 7
        day_range = range(start_day, calendar.monthrange(year, start_month)[1] + 1)  # Bắt đầu từ ngày 6
    else:
        month_range = range(1, 13)  # Tất cả các tháng
        day_range = range(1, 32)  # Tất cả các ngày (sẽ kiểm tra ngày hợp lệ sau)

    for month in month_range:
        # Xác định số ngày trong tháng
        num_days = calendar.monthrange(year, month)[1]
        
        for day in day_range:
            if day > num_days:
                continue  # Bỏ qua các ngày không hợp lệ
            
            # Tạo URL cho từng ngày
            url = base_url.format(year, month, day, year, month, day)
            print(f"Đang crawl dữ liệu cho ngày: {year}-{month:02d}-{day:02d}")
            
            # Truy cập vào URL
            driver.get(url)

            # Đợi trang web tải xong
            # time.sleep(1)

            # Xử lý modal "Privacy Notice"
            try:
                accept_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div/div/div[3]/button[2]"))
                )
                accept_button.click()
                print("Đã xử lý modal 'Privacy Notice'")
            except Exception as e:
                print("Không tìm thấy modal 'Privacy Notice':", e)

            # Đợi cho nút button có thuộc tính data-bs-toggle="modal" xuất hiện
            try:
                modal_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/main/div/div/div/div[1]/div[1]/div[1]/button[1]"))
                )
                modal_button.click()  # Click vào nút để mở modal
                print("Đã click mở modal")
            except Exception as e:
                print("Không tìm thấy nút button có data-bs-toggle='modal':", e)

            # Đợi cho nút "Save" xuất hiện sau khi modal mở
            try:
                save_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/main/div/div/div/div[1]/div[3]/div[5]/div/div/div[3]/button"))
                )
                save_button.click()  # Click vào nút "Save"
                print("Đã click nút 'Save'")
            except Exception as e:
                print("Không tìm thấy nút 'Save':", e)

            # Đợi thêm thời gian để tải dữ liệu
            # time.sleep(1)

# Đóng driver
driver.quit()
print("Quá trình crawl đã hoàn tất.")