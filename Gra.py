import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
# Chuẩn bị dữ liệu
df = pd.read_csv("C:/Users/User/Desktop/Mon_Hoc/PPNCKH/PP_NC_KH/datappnckhh_2024.csv")
df['time'] = pd.to_datetime(df['time'])
df.set_index('time', inplace=True)
features = ['dwpt', 'rhum']
target = 'temp'
# Chuẩn hóa dữ liệu
scaler = StandardScaler()
df[features] = scaler.fit_transform(df[features])
# Chia dữ liệu thành train và test
train_size = int(len(df) * 0.8)
train, test = df.iloc[:train_size], df.iloc[train_size:]
# Tạo dữ liệu cho Gradient Boosting Regression
X_train = train[features]
y_train = train[target]
X_test = test[features]
y_test = test[target]
# Xây dựng mô hình Gradient Boosting Regression
model_gbr = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
# Huấn luyện mô hình
model_gbr.fit(X_train, y_train)
# Dự báo trên tập kiểm tra
y_pred = model_gbr.predict(X_test)
# Đánh giá mô hình
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

# Vẽ biểu đồ so sánh giá trị dự báo với giá trị thực tế (sử dụng 500 mẫu đầu tiên)
plt.figure(figsize=(10, 6))

# Chọn 500 mẫu đầu tiên
y_test_subset = y_test[:500]
y_pred_subset = y_pred[:500]

# Vẽ biểu đồ
plt.plot(y_test_subset.index, y_test_subset, label='Giá trị thực tế', color='blue')
plt.plot(y_test_subset.index, y_pred_subset, label='Giá trị dự đoán', color='red', linestyle='--')

plt.xlabel('Thời gian')
plt.ylabel('Nhiệt độ')
plt.title('Biểu đồ thể hiện giá trị dự báo và giá trị thực tế (500 mẫu)')
plt.legend()

plt.tight_layout()


# Vẽ nhiệt độ
plt.plot(df.index, df['temp'], label='Nhiệt độ (temp)', color='blue')

plt.xlabel('Thời gian')
plt.ylabel('Giá trị')
plt.title('Biểu đồ thể hiện Nhiệt độ theo thời gian')
plt.show()

# Vẽ histogram của độ ẩm
plt.hist(df['rhum'], bins=30, color='green', alpha=0.7, edgecolor='black')

# Thêm các nhãn
plt.xlabel('Độ ẩm (%)')
plt.ylabel('Tần suất')
plt.title('Biểu đồ Histogram thể hiện Độ ẩm và Tần suất')

# Hiển thị biểu đồ
plt.tight_layout()
plt.show()

# Thêm các nhãn
plt.xlabel('Thời gian')
plt.ylabel('Giá trị')





