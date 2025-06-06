
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
import requests
import pandas as pd

URL = (
    "https://finance.yahoo.com/quote/BTC-USD/history/"
    "?period1=1591388783&period2=1749155168&filter=history&frequency=1d"
)

session = requests.Session()
session.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",

})

res = session.get(URL)
# print("Status code:", res.status_code)

soup = BeautifulSoup(res.text, "html.parser")

table = soup.find('table')


# for i in table.find_all('tr'):
#     print(i.text)

all_rows = table.find_all("tr")

header_cells = all_rows[0].find_all("th")
column_names = []
for th in header_cells:

    visible_texts = th.find_all(string=True, recursive=False)
    if visible_texts:
        label = "".join(visible_texts).strip()
    else:
        label = th.get_text(strip=True)
    column_names.append(label)



data_rows = []
for row in all_rows[1:]:
    cells = row.find_all("td")
    if len(cells) == len(column_names):
        row_data = [td.get_text(strip=True) for td in cells]
        data_rows.append(row_data)


df = pd.DataFrame(data_rows, columns=column_names)

df["Date"] = pd.to_datetime(df["Date"])

numeric_cols = ["Open", "High", "Low", "Close", "Adj Close"]
for col in numeric_cols:

    df[col] = df[col].astype('|S').replace(",", "").astype(float)

df["Volume"] = df["Volume"].str.replace(",", "")


df.head()



plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='Date', y='Close')
plt.title('Bitcoin Closing Price Over Time')
plt.xlabel('Date')
plt.ylabel('Closing Price (USD)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plotting the volume over time
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='Date', y='Volume')
plt.title('Bitcoin Trading Volume Over Time')
plt.xlabel('Date')
plt.ylabel('Volume')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Scatter plot of High vs Low price
plt.figure(figsize=(8, 8))
sns.scatterplot(data=df, x='Low', y='High')
plt.title('High vs Low Price')
plt.xlabel('Low Price (USD)')
plt.ylabel('High Price (USD)')
plt.show()

# Distribution of Closing Prices (Histogram)
plt.figure(figsize=(8, 6))
sns.histplot(data=df, x='Close', bins=30, kde=True)
plt.title('Distribution of Bitcoin Closing Prices')
plt.xlabel('Closing Price (USD)')
plt.ylabel('Frequency')
plt.show()

