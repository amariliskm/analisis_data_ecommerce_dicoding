import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the title and subheader of your Streamlit app
st.title(
    "E-commerce Insights"
)


# Load the cleaned data from a CSV file
df_order_items = pd.read_csv(f"https://drive.google.com/uc?id=1bHuR_lcv1czJ0yoStRJYzLH-K4Bs6HML")
orders = pd.read_csv(f"https://drive.google.com/uc?id=1VYEArGUX640lxJgQYfQHGlfyoshd5R8a")

#1
st.subheader("Category barang yang paling banyak dibeli dan paling sedikit diminati")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(45, 15))
df_category = df_order_items.groupby(by="product_category_name_english")["product_id"].count().reset_index() #jumlah pembelian
df_category = df_category.rename(columns={"product_category_name_english": "category", "product_id": "orders"})

# fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors = ["#102cd4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="orders", y="category", data=df_category.sort_values(by="orders", ascending=False).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Category Terlaris", loc="center", fontsize=15)
ax[0].tick_params(axis ='y', labelsize=12)

sns.barplot(x="orders", y="category", data=df_category.sort_values(by="orders", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Category Sedikit Peminat", loc="center", fontsize=15)
ax[1].tick_params(axis='y', labelsize=12)

plt.suptitle("Category Terlaris dan Sedikit Peminat berdasarkan Total Pembelian", fontsize=20)
sns.despine()
st.pyplot(fig)

#3
st.subheader("Payment Value dari Tiap Payment Type")
fig = plt.figure(figsize=[10, 5])
df_payment = orders.groupby(by="payment_type")["payment_value"].mean().reset_index()
# plt.figure(figsize=(10, 5))

colors = ["#102cd4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x="payment_type",
    y="payment_value",
    data=df_payment.sort_values(by="payment_value", ascending = False),
    palette=colors
)
plt.title("Payment Tyoe", loc="center", fontsize=15)
plt.ylabel("nilai transaksi")
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)
sns.despine()
st.pyplot(fig)

fig = plt.figure(figsize=[15, 8])
df_payment = orders.groupby(by="payment_type")["order_id"].nunique().reset_index()
palette_color = sns.color_palette('Blues')

plt.pie(df_payment["order_id"], labels=df_payment["payment_type"], colors=palette_color, autopct='%.0f%%')
plt.title("Payment Type Distribution")
sns.despine()
st.pyplot(fig)

#4
st.subheader("Perbandingan Penjualan Tahun 2017 dan 2018")
fig = plt.figure(figsize=[15, 8])
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

# Extract month and year from the 'order_purchase_timestamp'
orders['nomor_bulan'] = orders['order_purchase_timestamp'].dt.strftime('%m')
orders['year'] = orders['order_purchase_timestamp'].dt.year

# Group by month and year, and count unique order IDs
df_tanggal_penjualan = orders.groupby(['nomor_bulan', 'year'])['order_id'].nunique().reset_index()
df_tanggal_penjualan['nomor_bulan'] = df_tanggal_penjualan['nomor_bulan'].astype(int)
df_tanggal_penjualan = df_tanggal_penjualan[df_tanggal_penjualan['nomor_bulan'] < 9]

# Define month names
month_names = {
    1: 'Jan',
    2: 'Feb',
    3: 'Mar',
    4: 'Apr',
    5: 'Mei',
    6: 'Jun',
    7: 'Jul',
    8: 'Aug'
}
df_tanggal_penjualan['nama_bulan'] = df_tanggal_penjualan['nomor_bulan'].map(month_names)

# Create a bar plot using Seaborn
custom_palette = ["#0DA6D1", "#102cd4"]
sns.set(style="whitegrid")
sns.barplot(x='nama_bulan', y='order_id', hue='year', data=df_tanggal_penjualan, palette=custom_palette)
st.pyplot(fig)

#5
st.subheader("Penjualan Perbulan")
fig = plt.figure(figsize=[20, 8])
df_tanggal =  orders.groupby(by=["month","year"]).order_id.nunique().reset_index()
df_tanggal["month"] = pd.to_datetime(df_tanggal["month"], format='%m-%Y')
# plt.figure(figsize=(20, 6))

ax = sns.lineplot(x='month', y='order_id', data=df_tanggal, estimator=None,linewidth=3)
ax.set(xticks=df_tanggal.month.values)

plt.title("Tren Pertumbuhan Penjualan", loc="center", fontsize=18)
plt.ylabel("total order")
plt.xlabel(None)
ax.grid(False)
for tick in ax.get_xticklabels():
    tick.set_rotation(45)
sns.despine()
st.pyplot(fig)

#6
st.subheader("Hari dan bagian hari yang paling aktif menjual")
fig = plt.figure(figsize=[15, 8])
df_bagian_hari = orders.groupby(by="waktu_hari_pembelian")["order_id"].nunique().reset_index()
df_bagian_hari.rename(columns={
    "order_id": "total_orders"
}, inplace=True)

# plt.figure(figsize=(10, 5))

colors = ["#D3D3D3", "#D3D3D3", "#102cd4", "#D3D3D3"]

sns.barplot(
    x="waktu_hari_pembelian",
    y="total_orders",
    data=df_bagian_hari.sort_values(by="total_orders"),
    palette=colors
)
plt.title("persebaran pembelian berdasarkan bagian hari", loc="center", fontsize=15)
plt.ylabel("total order")
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)
sns.despine()
st.pyplot(fig)

#----
df_hari = orders.groupby(by="hari_pembelian").order_id.nunique().sort_values(ascending=False).reset_index()
fig = plt.figure(figsize=[15, 8])
df_hari.rename(columns={
    "order_id": "total_orders"
}, inplace=True)
# plt.figure(figsize=(10, 5))

colors = ["#D3D3D3", "#D3D3D3","#D3D3D3", "#D3D3D3","#D3D3D3", "#D3D3D3", "#102cd4"]

sns.barplot(
    x="hari_pembelian",
    y="total_orders",
    data=df_hari.sort_values(by="total_orders"),
    palette=colors
)
plt.title("persebaran pembelian berdasarkan hari", loc="center", fontsize=15)
plt.ylabel("total order")
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)
sns.despine()
st.pyplot(fig)
