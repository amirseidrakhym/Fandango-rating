"""
Есть ли кофликт интересов на веб-сайте, который продаёт билеты на фильмы и отображает рейтинги фильмов?

В качестве сайта для покупки билетов мы берем Fandango. Могут ли такие сайты как Fandango, отображать завышенные рейтинги, чтобы продавать больше билетов?
Fandango отображает два типа рейтингов:
 - STARS - Рейтинг в количестве звезд то 0 до 5,  отображаемсый на их веб-сайте
 - RATING - Действительный рейтинг, отображаемый в виде числа на странице фильма
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Сначала загружаем данные
fandango = pd.read_csv("fandango_scrape.csv")
plt.figure(figsize=(10,4),dpi=150)

# С помощью графика СкаттерПлот нарисуем график показывающий связь между колонками Рейтинг и Вотс. Закомментировал графики чтобы в будущем не мешало для выведения результа.
# first_graph = sns.scatterplot(data=fandango, x="RATING", y="VOTES")
corr = fandango.corr()

#Возьмем из стольбца Фильм только годы и создаем новую колонку с годами
title = 'Название фильма (Год)'
title = title.split('(')[-1].replace(')','')
fandango['YEAR'] = fandango['FILM'].apply(lambda title: title.split('(')[-1].replace(')',''))

#Фильмы по годам
count = fandango['YEAR'].value_counts()
# second_graph = sns.countplot(data=fandango, x='YEAR')

# Фильмы с самыми высокими количествами голосов.
largest10 = fandango.nlargest(10, 'VOTES')

# Выведем сумма фильмов которые нету ни одного голоса.
no_votes = fandango['VOTES'] == 0
no_votes_sum = no_votes.sum()

# Создаем новый дата фрейм с фильмами которые проголосованы
fan_reviewed = fandango[fandango['VOTES']>0]

# с помощью кдеплот мы можем увидеть визуальную разницу между настоящим рейтингом и старсом
# third_graph = sns.kdeplot(fan_reviewed, x='RATING', clip=[0,5], fill=True, label = 'True Rating')
# third_graph2 = sns.kdeplot(fan_reviewed, x='STARS', clip=[0,5], fill=True, label = 'Stars Displayed')

#Разница между настоящим рейингом и старсом
fan_reviewed['STARS_DIFF'] = fan_reviewed['STARS'] - fan_reviewed['RATING']
# fourth_graph = sns.countplot(data=fan_reviewed, x='STARS_DIFF', palette='magma')

#Загружаем новый файл с данными множество сайтов для покупки онлайн билетов
all_sites = pd.read_csv("all_sites_scores.csv")

# В этих данные есть данные с РоттенТомейдос. И в нем два стольбца. Стольбец под названием РоттенТомейдос это рейтинги критиков, а РоттенТомейдос это отзвывы обчных пользователей
#fifth_graph = sns.scatterplot(data=all_sites, x='RottenTomatoes', y='RottenTomatoes_User')

all_sites['Rotten_Diff'] = all_sites['RottenTomatoes'] - all_sites['RottenTomatoes_User']
rt_mean = all_sites['Rotten_Diff'].apply(abs).mean()

#sixth_graph = sns.histplot(data=all_sites, x='Rotten_Diff', kde=True, bins=25)

#Фильмы которые понравились пользователям но не понравились критикам
smallest5 = all_sites.nsmallest(5, 'Rotten_Diff')

#for Metacritic
#seventh_graph =  sns.scatterplot(data=all_sites, x='Metacritic', y='Metacritic_User')

#разница между голосами в МетаКритик и IMDB
# eighth_graph = sns.scatterplot(data=all_sites, x='Metacritic_user_vote_count', y='IMDB_user_vote_count')


#теперь соединим эти два данные. Fandango с остальными
df = pd.merge(fandango, all_sites, on='FILM', how='inner')

# Нормализируем колонки
df['RT_Norm'] = np.round(df['RottenTomatoes']/20, 1)
df['RTU_Norm'] = np.round(df['RottenTomatoes_User']/20, 1)
df['Meta_Norm'] = np.round(df['Metacritic']/20, 1)
df['Meta_U_Norm'] = np.round(df['Metacritic_User']/2, 1)
df['IMDB_Norm'] = np.round(df['IMDB']/2, 1)

#Собираем их в один датасет
norm_scores = df[['FILM', 'STARS','RATING','RT_Norm', 'RTU_Norm', 'Meta_Norm', 'Meta_U_Norm', 'IMDB_Norm']]

#С помощью этих графиков можно увидеть насколько завышены рейтинг Fandango в сравнении с остальными.
#ninth_graph = sns.kdeplot(data=norm_scores, clip=[0, 5], shade=True
last_graph = sns.histplot(norm_scores, bins=50)
print(last_graph)
print(plt.show())