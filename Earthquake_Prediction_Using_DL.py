# -*- coding: utf-8 -*-
"""AIDS_PROJECT.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JKQoowmds7rMTYUuAW3XKIZPf-7tkKCx
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping


from sklearn.metrics import mean_absolute_error, mean_squared_error
# %matplotlib inline

df = pd.read_csv("earthquake_1995-2023.csv")

df.head()

print(df.info())
print(df.isna().sum())
df['date_time'] = pd.to_datetime(df['date_time'], format="%d-%m-%Y %H:%M", errors='coerce')
df.head()
df = df.dropna(subset=['date_time'])

df['year'] = df['date_time'].dt.year
df['month'] = df['date_time'].dt.month
df['day'] = df['date_time'].dt.day
df['hour'] = df['date_time'].dt.hour

cols_to_drop = ['title', 'date_time', 'location']
df_model = df.drop(columns=cols_to_drop)
df_model = df_model.drop(columns=['alert', 'net','continent','country'])
df_model.head()

sns.set(style='whitegrid', context='talk')

plt.figure(figsize=(10,6))
sns.histplot(df['magnitude'], kde=True, bins=30, color='royalblue')
plt.title("Distribution of Earthquake Magnitude", fontsize=16)
plt.xlabel("Magnitude", fontsize=14)
plt.ylabel("Count", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,8))
scatter = plt.scatter(df['longitude'], df['latitude'],
                      c=df['magnitude'], cmap='viridis', alpha=0.7, s=50)
cbar = plt.colorbar(scatter, label="Magnitude")
cbar.ax.tick_params(labelsize=12)
plt.title("Geographical Distribution of Earthquakes", fontsize=16)
plt.xlabel("Longitude", fontsize=14)
plt.ylabel("Latitude", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,8))
numeric_df = df_model.select_dtypes(include=np.number)
corr = numeric_df.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", annot_kws={"size": 10})
plt.title("Correlation Heatmap", fontsize=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()

features = ['cdi', 'mmi', 'tsunami', 'sig', 'nst', 'dmin', 'gap', 'depth', 'latitude', 'longitude', 'year', 'month', 'day', 'hour']
target = 'magnitude'


df_model = df_model.dropna(subset=features + [target])

X = df_model[features].values
y = df_model[target].values


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = Sequential([
    Dense(128, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    BatchNormalization(),
    Dropout(0.3),

    Dense(64, activation='relu'),
    BatchNormalization(),
    Dropout(0.3),

    Dense(32, activation='relu'),
    BatchNormalization(),
    Dropout(0.2),

    Dense(1)
])


model.compile(optimizer='adam', loss='mse', metrics=['mae'])

model.summary()

early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

history = model.fit(X_train_scaled, y_train,
                    epochs=100,
                    batch_size=32,
                    validation_split=0.2,
                    callbacks=[early_stop],
                    verbose=1)

# Plot Loss vs. Epochs
plt.figure(figsize=(10,5))
plt.plot(history.history['loss'], label='Training Loss', marker='o')
plt.plot(history.history['val_loss'], label='Validation Loss', marker='o')
plt.xlabel("Epoch")
plt.ylabel("Mean Squared Error Loss")
plt.title("Training vs. Validation Loss")
plt.legend()
plt.show()

# Plot Mean Absolute Error vs. Epochs
plt.figure(figsize=(10,5))
plt.plot(history.history['mae'], label='Training MAE', marker='o')
plt.plot(history.history['val_mae'], label='Validation MAE', marker='o')
plt.xlabel("Epoch")
plt.ylabel("Mean Absolute Error")
plt.title("Training vs. Validation MAE")
plt.legend()
plt.show()

test_loss, test_mae = model.evaluate(X_test_scaled, y_test, verbose=0)
print(f"Test MSE Loss: {test_loss:.4f}")
print(f"Test MAE: {test_mae:.4f}")


rmse = np.sqrt(test_loss)
print(f"Test RMSE: {rmse:.4f}")

y_pred = model.predict(X_test_scaled).flatten()


plt.figure(figsize=(8,6))
plt.scatter(y_test, y_pred, alpha=0.6, color='navy')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], ls="--", color='red')
plt.xlabel("Actual Magnitude")
plt.ylabel("Predicted Magnitude")
plt.title("Actual vs Predicted Earthquake Magnitudes")
plt.show()


residuals = y_test - y_pred
plt.figure(figsize=(8,6))
sns.histplot(residuals, kde=True, color='teal', bins=30)
plt.title("Distribution of Prediction Residuals")
plt.xlabel("Residual (Actual - Predicted)")
plt.show()

model.save("earthquake_prediction_model.h5")
print("Model saved as earthquake_prediction_model.h5")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from datetime import datetime

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping
import kerastuner as kt


df = pd.read_csv("earthquake_1995-2023.csv")


df['date_time'] = pd.to_datetime(df['date_time'], format="%d-%m-%Y %H:%M", errors='coerce')
df = df.dropna(subset=['date_time'])
df = df.sort_values('date_time')

df.head()

df['time_diff'] = df['date_time'].diff().dt.total_seconds() / 3600.0
df['time_diff'].fillna(0, inplace=True)

coords = df[['latitude','longitude']]
kmeans = KMeans(n_clusters=5, random_state=42).fit(coords)
df['region_cluster'] = kmeans.labels_

df = pd.get_dummies(df, columns=['region_cluster'], prefix='region', drop_first=True)

df['date_time'] = pd.to_datetime(df['date_time'], format="%d-%m-%Y %H:%M", errors='coerce')
df = df.dropna(subset=['date_time'])
df = df.sort_values('date_time')

df['year'] = df['date_time'].dt.year
df['month'] = df['date_time'].dt.month
df['day'] = df['date_time'].dt.day
df['hour'] = df['date_time'].dt.hour


print(df[['date_time', 'year', 'month', 'day', 'hour']].head())

sequence_length = 5


base_features = ['cdi', 'mmi', 'tsunami', 'sig', 'nst', 'dmin', 'gap', 'depth', 'latitude', 'longitude',
                 'year', 'month', 'day', 'hour', 'time_diff']


region_cols = [col for col in df.columns if col.startswith('region_')]
features = base_features + region_cols

target = 'magnitude'
df_model = df[features + [target]].dropna()


from sklearn.preprocessing import StandardScaler
scaler_features = StandardScaler()
df_model[features] = scaler_features.fit_transform(df_model[features])


def create_sequences(data, seq_length, feature_cols, target_col):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[feature_cols].iloc[i:i+seq_length].values)
        y.append(data[target_col].iloc[i+seq_length])
    return np.array(X), np.array(y)

X_seq, y_seq = create_sequences(df_model, sequence_length, features, target)
print("Sequence shape:", X_seq.shape)
print("Target shape:", y_seq.shape)

def build_model(hp):
    model = Sequential()

    model.add(LSTM(units=hp.Int("lstm_units_1", min_value=32, max_value=128, step=32),
                   activation='tanh',
                   return_sequences=True,
                   input_shape=(X_seq.shape[1], X_seq.shape[2])))
    model.add(Dropout(hp.Float("dropout_1", min_value=0.1, max_value=0.5, step=0.1)))


    if hp.Boolean("second_lstm"):
        model.add(LSTM(units=hp.Int("lstm_units_2", min_value=32, max_value=128, step=32),
                       activation='tanh'))
        model.add(Dropout(hp.Float("dropout_2", min_value=0.1, max_value=0.5, step=0.1)))


    model.add(Dense(50, activation='relu'))
    model.add(Dense(1))

    model.compile(optimizer=tf.keras.optimizers.Adam(
                        learning_rate=hp.Float("lr", min_value=1e-4, max_value=1e-2, sampling="LOG", default=1e-3)),
                  loss='mse',
                  metrics=['mae'])
    return model


tuner = kt.RandomSearch(build_model,
                        objective='val_loss',
                        max_trials=5,
                        executions_per_trial=2,
                        directory='kt_dir',
                        project_name='earthquake_lstm')


tuner.search(X_seq, y_seq, epochs=30, validation_split=0.2,
             callbacks=[EarlyStopping(monitor='val_loss', patience=5)], verbose=1)


best_model = tuner.get_best_models(num_models=1)[0]
best_model.summary()

history = best_model.fit(X_seq, y_seq, epochs=50, batch_size=32,
                         validation_split=0.2,
                         callbacks=[EarlyStopping(monitor='val_loss', patience=10)], verbose=1)

import matplotlib.pyplot as plt

# Plot Loss Curves
plt.figure(figsize=(10,6))
plt.plot(history.history['loss'], label='Training Loss', marker='o')
plt.plot(history.history['val_loss'], label='Validation Loss', marker='o')
plt.xlabel("Epochs", fontsize=14)
plt.ylabel("MSE Loss", fontsize=14)
plt.title("Training vs. Validation Loss", fontsize=16)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()

# Plot MAE Curves
plt.figure(figsize=(10,6))
plt.plot(history.history['mae'], label='Training MAE', marker='o')
plt.plot(history.history['val_mae'], label='Validation MAE', marker='o')
plt.xlabel("Epochs", fontsize=14)
plt.ylabel("MAE", fontsize=14)
plt.title("Training vs. Validation MAE", fontsize=16)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()

y_pred = best_model.predict(X_seq).flatten()


import plotly.express as px

fig = px.scatter(x=y_seq, y=y_pred, labels={'x': 'Actual Magnitude', 'y': 'Predicted Magnitude'},
                 title="Actual vs Predicted Earthquake Magnitudes",
                 template="plotly_white")

fig.add_trace(go.Scatter(x=[min(y_seq), max(y_seq)],
                         y=[min(y_seq), max(y_seq)],
                         mode='lines', name='Ideal', line=dict(color='red', dash='dash')))
fig.show()

df_plot = df.copy()
fig_ts = px.scatter(df_plot, x='date_time', y='magnitude', color='mmi', hover_data=['depth'],
                    title="Interactive Earthquake Magnitude Time Series",
                    labels={'date_time': 'Date', 'magnitude': 'Magnitude'})
fig_ts.update_traces(marker=dict(size=8))
fig_ts.update_layout(font=dict(size=14))
fig_ts.show()


fig_map = px.scatter_mapbox(df_plot, lat="latitude", lon="longitude",
                            hover_name="title",
                            hover_data=["magnitude", "depth", "time_diff"],
                            color="magnitude", size="magnitude",
                            color_continuous_scale=px.colors.cyclical.IceFire,
                            size_max=15, zoom=1,
                            title="Interactive Geographical Distribution of Earthquakes")
fig_map.update_layout(mapbox_style="open-street-map", font=dict(size=14))
fig_map.show()

def preprocess_new_sample(new_sample_df):
    """
    new_sample_df : a pandas DataFrame that contains the same raw columns
                    you used in your original dataframe (including date_time).
    Returns a preprocessed DataFrame containing the engineered features.
    """

    new_sample_df['date_time'] = pd.to_datetime(new_sample_df['date_time'], format="%d-%m-%Y %H:%M", errors='coerce')


    new_sample_df = new_sample_df.sort_values('date_time')


    new_sample_df['year'] = new_sample_df['date_time'].dt.year
    new_sample_df['month'] = new_sample_df['date_time'].dt.month
    new_sample_df['day'] = new_sample_df['date_time'].dt.day
    new_sample_df['hour'] = new_sample_df['date_time'].dt.hour


    new_sample_df['time_diff'] = new_sample_df['date_time'].diff().dt.total_seconds() / 3600.0
    new_sample_df['time_diff'].fillna(0, inplace=True)


    if 'region_cluster' not in new_sample_df.columns:
        new_sample_df['region_cluster'] = kmeans.predict(new_sample_df[['latitude', 'longitude']])
        new_sample_df = pd.get_dummies(new_sample_df, columns=['region_cluster'], prefix='region', drop_first=True)


    base_features = ['cdi', 'mmi', 'tsunami', 'sig', 'nst', 'dmin', 'gap', 'depth',
                     'latitude', 'longitude', 'year', 'month', 'day', 'hour', 'time_diff']
    region_cols = [col for col in new_sample_df.columns if col.startswith('region_')]
    feat_list = base_features + region_cols

    return new_sample_df[feat_list]

def format_sequence(data, seq_length):
    """
    data : numpy array of shape (num_samples, num_features)
    seq_length : size of the sliding window.

    Returns a sequence of data ready to feed into the time-series model.
    """
    X_seq = []
    for i in range(len(data) - seq_length):
        X_seq.append(data[i:i+seq_length])
    return np.array(X_seq)

def predict_earthquake(new_sample_df, model, seq_length):
    """
    new_sample_df: pandas DataFrame containing new earthquake events with raw columns.
    model: a trained model ready for inference.
    seq_length: integer, the sequence length used during training.

    This function:
    - Applies preprocessing to the new sample DataFrame,
    - Converts the features to numpy array,
    - If needed formats the data as a sequence,
    - Returns predictions.
    """

    processed = preprocess_new_sample(new_sample_df)


    processed_scaled = scaler_features.transform(processed.values)


    X_seq_new = format_sequence(processed_scaled, seq_length)


    predictions = model.predict(X_seq_new).flatten()

    return predictions

train_size = int(len(X_seq) * 0.8)
X_train, X_test = X_seq[:train_size], X_seq[train_size:]
y_train, y_test = y_seq[:train_size], y_seq[train_size:]

print("Training sequence shape:", X_train.shape)
print("Test sequence shape:", X_test.shape)

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


y_pred_test = best_model.predict(X_test).flatten()

mse = mean_squared_error(y_test, y_pred_test)
mae = mean_absolute_error(y_test, y_pred_test)
r2 = r2_score(y_test, y_pred_test)

print("Test MSE:  {:.4f}".format(mse))
print("Test MAE:  {:.4f}".format(mae))
print("Test R²:   {:.4f}".format(r2))

import matplotlib.pyplot as plt
import seaborn as sns


residuals = y_test - y_pred_test


plt.figure(figsize=(10,6))
sns.histplot(residuals, kde=True, color='navy')
plt.title("Residuals Distribution")
plt.xlabel("Residual (Actual - Predicted)")
plt.ylabel("Frequency")
plt.show()


plt.figure(figsize=(10,6))
plt.plot(residuals, marker='o', linestyle='--', color='darkorange')
plt.title("Residuals Over Test Sequences")
plt.xlabel("Test Sequence Index")
plt.ylabel("Residual")
plt.show()

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


if "region_cluster" not in df.columns:

    coords = df[['latitude', 'longitude']]
    kmeans = KMeans(n_clusters=5, random_state=42)

    df['region_cluster'] = kmeans.fit_predict(coords)


print("Unique clusters:", df["region_cluster"].unique())


clusters = df["region_cluster"].iloc[sequence_length:].reset_index(drop=True)


y_pred_full = best_model.predict(X_seq).flatten()


df_metrics = pd.DataFrame({
    "Actual": y_seq,
    "Predicted": y_pred_full,
    "Region": clusters
})

for cluster in sorted(df_metrics['Region'].unique()):
    subset = df_metrics[df_metrics['Region'] == cluster]
    mse_cluster = mean_squared_error(subset["Actual"], subset["Predicted"])
    mae_cluster = mean_absolute_error(subset["Actual"], subset["Predicted"])
    r2_cluster = r2_score(subset["Actual"], subset["Predicted"])
    print(f"Cluster {cluster}: MSE = {mse_cluster:.4f}, MAE = {mae_cluster:.4f}, R² = {r2_cluster:.4f}")

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional

def build_bidirectional_model():
    model = Sequential()

    model.add(Bidirectional(LSTM(64, return_sequences=True),
                            input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dropout(0.3))

    model.add(Bidirectional(LSTM(32)))
    model.add(Dropout(0.3))

    model.add(Dense(50, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

model_bi = build_bidirectional_model()
history_bi = model_bi.fit(X_train, y_train, epochs=30, batch_size=32, validation_split=0.2,
                          callbacks=[EarlyStopping(monitor='val_loss', patience=5)],
                          verbose=1)

from tensorflow.keras.layers import GRU

def build_gru_model():
    model = Sequential()
    model.add(GRU(64, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dropout(0.3))
    model.add(GRU(32))
    model.add(Dropout(0.3))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

model_gru = build_gru_model()
history_gru = model_gru.fit(X_train, y_train, epochs=30, batch_size=32, validation_split=0.2,
                            callbacks=[EarlyStopping(monitor='val_loss', patience=5)],
                            verbose=1)

best_model.save("earthquake_prediction_model.h5")
print("Saved best tuned model as earthquake_prediction_model.h5")

import pandas as pd
import matplotlib.pyplot as plt


results = {
    "Tuned LSTM": {
         "min_val_loss": min(history.history['val_loss']),
         "min_val_mae": min(history.history['val_mae'])
    },
    "Bidirectional LSTM": {
         "min_val_loss": min(history_bi.history['val_loss']),
         "min_val_mae": min(history_bi.history['val_mae'])
    },
    "GRU": {
         "min_val_loss": min(history_gru.history['val_loss']),
         "min_val_mae": min(history_gru.history['val_mae'])
    }
}


df_results = pd.DataFrame(results).T
print("Validation Metrics for Each Model:")
print(df_results)

models = list(df_results.index)
val_loss = df_results["min_val_loss"].values
val_mae = df_results["min_val_mae"].values

plt.figure(figsize=(12, 5))

# Plot Validation Loss
plt.subplot(1, 2, 1)
plt.bar(models, val_loss, color='skyblue')
plt.ylabel("Min Validation Loss (MSE)")
plt.title("Validation Loss Comparison")
plt.xticks(rotation=45)

# Plot Validation MAE
plt.subplot(1, 2, 2)
plt.bar(models, val_mae, color='salmon')
plt.ylabel("Min Validation MAE")
plt.title("Validation MAE Comparison")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

!pip install streamlit





!pip install keras-tuner

