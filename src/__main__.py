from db import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
import seaborn as sns


def duration_time_recognition(data):
    # df_select = data[['count_words', 'time_recognition']]
    # print(df_select)
    # Plot
    # sns.lmplot(data=df_select)
    data[['count_words', 'time_recognition', 'duration']] = data[
        ['count_words', 'time_recognition', 'duration']].astype(float)
    # coef = np.polyfit(data['time_recognition'], data['count_words'], 1)
    # poly1d_fn = np.poly1d(coef)
    m, b, *_ = linregress(data['time_recognition'], data['duration'])
    plt.title(f'y = {m:.2f}x {b:+.2f}')
    plt.axline(xy1=(0, b), slope=m, color='red')
    plt.scatter(data['time_recognition'], data['duration'])
    # plt.plot(data['time_recognition'], data['count_words'], 'yo', data['time_recognition'], poly1d_fn(data['time_recognition']))
    plt.xlabel("time recognition (sec)")
    plt.ylabel("duration (sec)")
    plt.savefig(f'img1_{m:.2f}.png')
    plt.show()
    print(data)
    print(data.dtypes)
    data[['count_words', 'time_recognition', 'duration']] = data[
        ['count_words', 'time_recognition', 'duration']].astype(float)
    print(data.dtypes)
    print(m, b, *_)
    print(data['time_recognition'].corr(data['duration']))
    mean_duration = data['duration'].mean()
    mean_time_recognition = data['time_recognition'].mean()
    mean_count_words = data['count_words'].mean()
    print(mean_duration)
    print(mean_time_recognition)
    print(mean_count_words)
    k2 = mean_duration / mean_time_recognition
    print(k2)
    print("-------------------")


def time_recognition_count_words(data):
    # df_select = data[['count_words', 'time_recognition']]
    # print(df_select)
    # Plot
    # sns.lmplot(data=df_select)
    data[['count_words', 'time_recognition', 'duration']] = data[
        ['count_words', 'time_recognition', 'duration']].astype(float)
    # coef = np.polyfit(data['time_recognition'], data['count_words'], 1)
    # poly1d_fn = np.poly1d(coef)
    m, b, *_ = linregress(data['time_recognition'], data['count_words'])
    print(m, b, *_)
    plt.title(f'y = {m:.2f}x {b:+.2f}')
    plt.axline(xy1=(0, b), slope=m, label=f'$y = {m:.1f}x {b:+.1f}$', color='red')
    plt.scatter(data['time_recognition'], data['count_words'])
    # plt.plot(data['time_recognition'], data['count_words'], 'yo', data['time_recognition'], poly1d_fn(data['time_recognition']))
    plt.xlabel("time recognition (sec)")
    plt.ylabel("count words")
    plt.savefig(f'img2_{m:.2f}.png')
    plt.show()
    print(data)
    print(data.dtypes)
    data[['count_words', 'time_recognition', 'duration']] = data[
        ['count_words', 'time_recognition', 'duration']].astype(float)
    print(data.dtypes)
    print(m, b, *_)
    print(data['time_recognition'].corr(data['count_words']))
    mean_duration = data['duration'].mean()
    mean_time_recognition = data['time_recognition'].mean()
    mean_count_words = data['count_words'].mean()
    print(mean_duration)
    print(mean_time_recognition)
    print(mean_count_words)
    k = mean_count_words / mean_time_recognition
    print(k)


def graph_3d(data):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(data['time_recognition'], data['count_words'], data['duration'])
    ax.set_xlabel("time recognition (sec)")
    ax.set_ylabel("count words")
    ax.set_zlabel("duration (sec)")
    plt.savefig(f'img3_{len(data)}.png')
    plt.show()


def corr(df):
    plt.figure(figsize=(12, 10), dpi=80)
    sns.heatmap(df.corr(), xticklabels=df.corr().columns, yticklabels=df.corr().columns, cmap='RdYlGn', center=0,
                annot=True)
    # Decorations
    plt.title('Correlogram of mtcars', fontsize=22)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig('corr.png')
    plt.show()


if __name__ == "__main__":
    connection = db_connection()
    column_names = ['filename', 'duration', 'count_words', 'time_recognition']
    data = get_data_from_sql_to_pd(connection, column_names)
    mas = list()
    mas.append(data)
    data = data.loc[data['time_recognition'] < 250]
    mas.append(data)
    for dat in mas:
        duration_time_recognition(dat)
        time_recognition_count_words(dat)
    graph_3d(data)
    corr(data)

