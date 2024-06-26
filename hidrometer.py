def main():
    import pandas as pd
    import seaborn as sns
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from statsmodels.formula.api import ols
    import streamlit as st


    data_fields = [
        "applicationID", "applicationName", "data_boardVoltage", "data_counter", 
        "devEUI", "fCnt", "fPort", "host", "nodeName", "rxInfo_altitude_0", 
        "rxInfo_altitude_1", "rxInfo_latitude_0", "rxInfo_latitude_1", 
        "rxInfo_loRaSNR_0", "rxInfo_loRaSNR_1", "rxInfo_longitude_0", 
        "rxInfo_longitude_1", "rxInfo_mac_0", "rxInfo_mac_1", "rxInfo_name_0", 
        "rxInfo_name_1", "rxInfo_rssi_0", "rxInfo_rssi_1", "time", "txInfo_adr", 
        "txInfo_codeRate", "txInfo_dataRate_bandwidth", "txInfo_dataRate_modulation", 
        "txInfo_dataRate_spreadFactor", "txInfo_frequency"
    ]

    df_hidrometer = pd.read_csv(r'data/Hidrometer.csv', header=3, usecols=data_fields)
    df_hidrometer["time"] = pd.to_datetime(df_hidrometer["time"])

    dfs_hidrometer_per_node = {app_id: df_node for app_id, df_node in df_hidrometer.groupby("devEUI")}
    ids = list(dfs_hidrometer_per_node.keys())


    colors = sns.color_palette("husl", len(ids))

    ncols = 3
    nrows = (len(ids) + ncols - 1) // ncols

    st.title("Análise da quantidade de água no hidrometro")
    fig, axes = plt.subplots(ncols=ncols, nrows=nrows, figsize=(20, nrows*5))
    axes = axes.flatten()
    for ax, id in zip(axes,ids):
        df_hidrometer = dfs_hidrometer_per_node[id]
        sns.lineplot(ax=ax, x="time", y="data_counter", data=df_hidrometer, label=id, color=colors.pop(0))
        ax.set_xlabel("Tempo (h)")
        ax.set_ylabel("Quantidade de água (L)")
        ax.set_title("Volume do hidrometro ao longo do tempo") 
        ax.legend(loc='upper left')
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        ax.grid(True)
    st.pyplot(plt.gcf())

    st.title("Estatísticas da quantidade de água no hidrometro")
    data_volume = []
    print("Intervalo de tempo total: {:.2f}".format((df_hidrometer["time"].max() - df_hidrometer["time"].min()).total_seconds()/60))
    for id in ids:
        max_volume = dfs_hidrometer_per_node[id]["data_counter"].max()
        min_volume = dfs_hidrometer_per_node[id]["data_counter"].min()

        data_volume.append([id, max_volume, min_volume])

    df_estatisticas = pd.DataFrame(data_volume, columns=["Device ID", "Max Volume", "Min Volume"])
    st.table(df_estatisticas)

    colors = sns.color_palette("husl", len(ids))

    st.title("Voltagem da placa ao longo do tempo")
    fig, axes = plt.subplots(ncols=ncols, nrows=nrows, figsize=(20, nrows*5))
    axes = axes.flatten()
    for ax, id in zip(axes, ids):
        df_hidrometer_id = dfs_hidrometer_per_node[id]
        sns.lineplot(ax=ax, x="time", y="data_boardVoltage", data=df_hidrometer_id, label=id, color=colors.pop(0))
        ax.set_ylabel("Voltagem da placa (V)")
        ax.set_xlabel("Tempo (m)")
        ax.set_title("Voltagem da placa x Tempo") 
        ax.legend(loc='upper left')
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        ax.grid(True)
    st.pyplot(plt.gcf())

    st.title("Última Voltagem para cada Device")
    lista_voltagem = []
    for id in ids:
        ultima_voltagem = dfs_hidrometer_per_node[id]["data_boardVoltage"].iloc[-1]
        lista_voltagem.append([id, ultima_voltagem])

    df_voltagem = pd.DataFrame(lista_voltagem, columns=["Device ID", "Última Voltagem"])
    def color_voltagem(val):
        color = 'red' if val < 2 else 'white'
        return f'color: {color}'

    styled_df = df_voltagem.style.map(color_voltagem, subset=['Última Voltagem'])
    st.dataframe(styled_df)

if __name__ == "__main__":
    main()