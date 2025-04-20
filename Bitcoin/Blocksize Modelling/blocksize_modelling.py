import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

df = pd.read_csv("monero_data4.xlsx")

# Convert 'year' and 'month' columns to datetime format
df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))

# Plot
plt.figure(figsize=(7, 4))
plt.plot(df['date'], df['cumulative_size_in_MB'], linestyle='-')
plt.title('Cumulative Size in MB over Time')
plt.xlabel('Date')
plt.ylabel('Cumulative Size (MB)')
plt.grid(True)
plt.tight_layout()
plt.show()


'''
>>> df
    currency  month  year  monthly_growth_in_MB  cumulative_size_in_MB  number_of_tx  size_of_tx       date
0     Monero      4  2014                 15.25                  15.25           590    0.025847 2014-04-01
1     Monero      5  2014                159.60                 174.85         16859    0.009467 2014-05-01
2     Monero      6  2014                424.98                 599.83         85813    0.004952 2014-06-01
3     Monero      7  2014                202.63                 802.46         60795    0.003333 2014-07-01
4     Monero      8  2014                227.67                1030.13         54302    0.004193 2014-08-01
..       ...    ...   ...                   ...                    ...           ...         ...        ...
114   Monero     10  2023               1666.12              120309.84        678454    0.002456 2023-10-01
115   Monero     11  2023               1742.91              122052.75        704528    0.002474 2023-11-01
116   Monero     12  2023               2089.41              124142.16        870243    0.002401 2023-12-01
117   Monero      1  2024               1676.27              125818.43        682934    0.002455 2024-01-01
118   Monero      2  2024               1846.80              127665.23        757855    0.002437 2024-02-01
'''


df['size_of_tx'] = df['monthly_growth_in_MB'] / df['number_of_tx']

plt.figure(figsize=(7, 4))
plt.plot(df['date'], df['size_of_tx'], linestyle='-')
plt.title('Size per transaction')
plt.xlabel('Date')
plt.ylabel('Size per transaction in MB')
plt.grid(True)
plt.tight_layout()
plt.show()


df['size_of_tx_in_bytes'] = df['size_of_tx'] * 1000000

plt.figure(figsize=(7, 4))
plt.plot(df['date'], df['size_of_tx_in_bytes'], linestyle='-')
plt.title('Size per transaction')
plt.xlabel('Date')
plt.ylabel('Size per transaction in Bytes')
plt.grid(True)
plt.tight_layout()
plt.show()



# Number of transactions

plt.figure(figsize=(7, 4))
plt.plot(df['date'], df['number_of_tx'], linestyle='-')
plt.title('Absolute number of transactions per month')
plt.xlabel('Date')
plt.ylabel('No. of transactions')
plt.grid(True)
plt.tight_layout()
plt.show()


df = pd.read_excel("monero_data3.xlsx")


# Scenario 1

df['monthly_growth_in_bytes_scenario1'] = (df['bitcoin_tx_per_month'] * 2436.88)
df['monthly_growth_in_MB_scenario1'] = (df['bitcoin_tx_per_month'] * 2436.88) / 1000000
df['cumulative_size_in_MB_scenario1'] = df['monthly_growth_in_MB_scenario1'].astype(int).cumsum()

print(df)

# Plot scenario 1

plt.figure(figsize=(7, 4))
plt.plot(df['date'], df['cumulative_size_in_MB'], linestyle='-')
plt.plot(df['date'], df['cumulative_size_in_MB_scenario1'], linestyle='-')
plt.title('Cumulative size of blockchain in MB - Scenario 1')
plt.xlabel('Date')
plt.ylabel('Cum. Size of Blockchain')
plt.grid(True)
plt.tight_layout()
plt.show()


# Confirm linear scaling

df_after_2019 = df[df['date'] > '2021-01-01']
num_transactions = np.array(df_after_2019['number_of_tx'])
avg_transaction_size = np.array(df_after_2019['size_of_tx_in_bytes'])
plt.scatter(num_transactions, avg_transaction_size, color='blue', label='Data', s=20)

# Fit linear regression model

model = LinearRegression()
model.fit(num_transactions.reshape(-1, 1), avg_transaction_size)
pred = model.predict(num_transactions.reshape(-1, 1))
plt.plot(num_transactions, pred, color='black', label='Linear Regression')

# Plot model

plt.xlabel('Number of Transactions')
plt.ylabel('Average Transaction Size')
plt.title('Number of Transactions vs. Average Transaction Size')
plt.ylim(0, 4000)
plt.grid(True)
plt.show()


# Simulate data based on the slope

num_transactions = np.array(df_after_2019['number_of_tx'])
avg_transaction_size = np.array(df_after_2019['size_of_tx_in_bytes'])
num_transactions_simulated = np.array(df['bitcoin_tx_per_month'])

# Fit linear regression model to real data

model_real = LinearRegression()
model_real.fit(num_transactions.reshape(-1, 1), avg_transaction_size)
slope = model_real.coef_[0]

floor_value = 1000  # Adjust this as needed

# Simulate new transaction data based on the slope

avg_transaction_size_simulated = np.maximum(floor_value, slope * num_transactions_simulated)  # Use maximum to ensure non-negative values

# Simulate new transaction data based on the slope

#avg_transaction_size_simulated = slope * num_transactions_simulated  # Simulated average transaction size

# Create DataFrame for simulated data

df_simulated = pd.DataFrame({'num_transactions_simulated': num_transactions_simulated, 'avg_transaction_size_simulated': avg_transaction_size_simulated})

print(df_simulated)


# Calculate change rates

df_after_2019 = df[df['date'] > '2021-01-01']
num_transactions = np.array(df_after_2019['number_of_tx'])
avg_transaction_size = np.array(df_after_2019['size_of_tx_in_bytes'])

# Calculate rate of change (first derivative)

avg_transaction_size_change = np.diff(avg_transaction_size) / np.diff(num_transactions)

# Plot rate of change

plt.scatter(num_transactions[:-1], avg_transaction_size_change, color='darkblue', linestyle='None')
plt.xlabel('Number of Transactions')
plt.ylabel('Rate of Change of Transaction Size')
plt.title('Rate of Change of Transaction Size over Time')
plt.grid(True)
plt.show()

'''
In mathematical notation:
Rate of Change= Δ Transaction Size / Δ Number of Transactions

where:

Δ Transaction Size is the change in transaction size between consecutive data points.
Δ Number of Transactions is the change in the number of transactions between consecutive data points.

'''

# Scenario 2

df['monthly_growth_in_bytes_scenario2'] = (df['bitcoin_max_tx_per_month'] * 2436.88)
df['monthly_growth_in_MB_scenario2'] = (df['bitcoin_max_tx_per_month'] * 2436.88) / 1000000
df['cumulative_size_in_MB_scenario2'] = df['monthly_growth_in_MB_scenario2'].astype(int).cumsum()

print(df)


plt.figure(figsize=(7, 4))
plt.plot(df['date'], df['cumulative_size_in_MB'], linestyle='-')
plt.plot(df['date'], df['cumulative_size_in_MB_scenario2'], linestyle='-')
plt.title('Cumulative size of blockchain in MB - Scenario 2 - Max. Bitcoin TX')
plt.xlabel('Date')
plt.ylabel('Cum. Size of Blockchain')
plt.grid(True)
plt.tight_layout()
plt.show()
