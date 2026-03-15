# Use Case: Time Series Forecasting

This document shows how to use the data-science-lab skill for **time series forecasting** tasks.

---

## User Prompt Example

```
Forecast sales for the next 12 months using @[path/to/sales_data.csv].
Use ARIMA and Prophet.
Export results and create visualizations.
Follow the data-science-lab skill.
```

---

## Goal Interpretation

| User Goal | Task Type | Recommended Models |
|-----------|-----------|-------------------|
| "forecast" / "predict" (time series) | time series | ARIMA, Prophet, LSTM |

---

## Example: Sales Forecasting

### Step 1: Load & Prepare Data

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Generate sample sales data
np.random.seed(42)
dates = pd.date_range('2020-01-01', periods=48, freq='M')
trend = np.linspace(100, 200, 48)
seasonality = 20 * np.sin(np.linspace(0, 8 * np.pi, 48))
noise = np.random.normal(0, 10, 48)

sales = trend + seasonality + noise

df = pd.DataFrame({
    'date': dates,
    'sales': sales
})
df.set_index('date', inplace=True)

print(df.head())
```

### Step 2: Visualize Time Series

```python
plt.figure(figsize=(12, 5))
plt.plot(df.index, df['sales'], marker='o', linestyle='-')
plt.title('Monthly Sales')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.grid(True)
plt.savefig('images/sales_time_series.png', dpi=150)
plt.show()
```

### Step 3: Method 1 - ARIMA

```python
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Split data
train = df.iloc[:-12]
test = df.iloc[-12:]

# Fit ARIMA model
model = ARIMA(train['sales'], order=(1, 1, 1))
fitted = model.fit()

# Forecast
forecast = fitted.forecast(steps=12)

# Evaluate
mae = mean_absolute_error(test['sales'], forecast)
rmse = np.sqrt(mean_squared_error(test['sales'], forecast))
print(f'ARIMA - MAE: {mae:.2f}, RMSE: {rmse:.2f}')
```

### Step 4: Method 2 - Exponential Smoothing

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Holt-Winters
hw_model = ExponentialSmoothing(
    train['sales'], 
    seasonal_periods=12,
    trend='add',
    seasonal='add'
)
hw_fitted = hw_model.fit()
hw_forecast = hw_fitted.forecast(12)

mae_hw = mean_absolute_error(test['sales'], hw_forecast)
rmse_hw = np.sqrt(mean_squared_error(test['sales'], hw_forecast))
print(f'Holt-Winters - MAE: {mae_hw:.2f}, RMSE: {rmse_hw:.2f}')
```

### Step 5: Compare Forecasts

```python
plt.figure(figsize=(12, 6))

# Plot historical
plt.plot(df.index, df['sales'], label='Historical', color='blue')

# Plot forecasts
plt.plot(test.index, forecast, label='ARIMA', color='red', linestyle='--')
plt.plot(test.index, hw_forecast, label='Holt-Winters', color='green', linestyle='--')

plt.axvline(x=train.index[-1], color='gray', linestyle=':', label='Train/Test Split')
plt.title('Sales Forecast Comparison')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.legend()
plt.grid(True)
plt.savefig('images/forecast_comparison.png', dpi=150)
plt.show()
```

### Step 6: Export Results

```python
results = pd.DataFrame({
    'date': test.index,
    'actual': test['sales'].values,
    'arima_forecast': forecast.values,
    'hw_forecast': hw_forecast.values
})
results.to_csv('results/forecast_results.csv', index=False)
print("Results saved to results/forecast_results.csv")
```

---

## Summary

| Model | Pros | Cons |
|-------|------|------|
| ARIMA | Interpretable, handles trends | Assumes stationarity |
| Holt-Winters | Captures seasonality | Requires enough data |
| Prophet (not shown) | Handles holidays, missing data | Requires installation |
| LSTM (not shown) | Captures complex patterns | Requires lots of data, slow |
