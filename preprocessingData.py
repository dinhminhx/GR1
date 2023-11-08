import pandas as pd
import warnings
# Ẩn warning
warnings.filterwarnings("ignore", category=FutureWarning)

# Đọc dữ liệu từ tệp CSV
data = pd.read_csv('stockdata.csv')

# Chuyển cột "timestamp" sang kiểu dữ liệu datetime
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Tạo một danh sách các symbols duy nhất trong dữ liệu
symbols = data['symbol'].unique()

# Tạo một DataFrame chung để lưu toàn bộ dữ liệu
combined_data = pd.DataFrame(columns=data.columns)

# Lặp qua từng symbol
for symbol in symbols:
    symbol_data = data[data['symbol'] == symbol]

    # Tạo một DataFrame với dải ngày duy nhất cho biểu đồ hiện tại
    unique_dates = symbol_data['timestamp'].unique()

    # Tạo một dải ngày từ ngày đầu tiên đến ngày cuối cùng cho biểu đồ hiện tại
    date_range = pd.date_range(start=unique_dates.min(), end=unique_dates.max(), freq='D')

    # Tạo một danh sách các DataFrame con
    symbol_data_list = []

    # Thêm các dòng dữ liệu bị thiếu bằng nội suy tuyến tính
    for date in date_range:
        if date not in symbol_data['timestamp'].values:
            previous_date = symbol_data[symbol_data['timestamp'] < date].iloc[-1]
            next_date = symbol_data[symbol_data['timestamp'] > date].iloc[0]

            interpolation_factor = (date - previous_date['timestamp']).days / (next_date['timestamp'] - previous_date['timestamp']).days

            interpolated_row = {
                'symbol': symbol,
                'timestamp': date,
                'open': round(previous_date['open'] + (next_date['open'] - previous_date['open']) * interpolation_factor, 2),
                'high': round(previous_date['high'] + (next_date['high'] - previous_date['high']) * interpolation_factor, 2),
                'low': round(previous_date['low'] + (next_date['low'] - previous_date['low']) * interpolation_factor, 2),
                'close': round(previous_date['close'] + (next_date['close'] - previous_date['close']) * interpolation_factor, 2),
                'volume': int(previous_date['volume'] + (next_date['volume'] - previous_date['volume']) * interpolation_factor)
            }

            symbol_data_list.append(interpolated_row)

    # Sắp xếp lại dữ liệu theo ngày cho biểu đồ hiện tại
    symbol_data = pd.concat([symbol_data, pd.DataFrame(symbol_data_list, columns=data.columns)])
    symbol_data = symbol_data.sort_values(by='timestamp')
    symbol_data = symbol_data.reset_index(drop=True)
    # Kết hợp dữ liệu của biểu đồ hiện tại vào DataFrame chung
    combined_data = pd.concat([combined_data, symbol_data], ignore_index=True)

# Lưu toàn bộ dữ liệu vào một tệp CSV
print("Done")
combined_data.to_csv('combined_stock_data.csv', index=False)
