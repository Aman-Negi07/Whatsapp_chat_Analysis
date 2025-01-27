from urlextract import URLExtract
from wordcloud import WordCloud
extractor=URLExtract()
import pandas as pd
from collections import Counter
import emoji
    
def fetch_stats(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]

    #fetch num of messages
    num_msg=df.shape[0]
    words=[]
    #fetch num of words

    for msg in df['message']:
        words.extend(msg.split())


    #fetch num of media
    num_media=df[df['message']=='<Media omitted>\n'].shape[0]

    #fetch num of links
    links=[]
    for msg in df["message"]:
        links.extend(extractor.find_urls(msg))

    return num_msg,len(words),num_media,links

def fetch_most_busy_user(df):
    x=df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'user':'name','count':'percent'})
    return x,df


def create_word_cloud(selected_user,df):
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    if selected_user!="Overall":
        df=df[df['user']==selected_user]

    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']


    def remove_stop_words(msg):
        y=[]
        for word in msg.lower().split():
            if word not in stop_words:
                y.append(word)

        return " ".join(y)
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'].apply(remove_stop_words)
    df_wc=wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    if selected_user!="Overall":
        df=df[df['user']==selected_user]

    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']

    words=[]
    for i in temp['message']:
        for word in i.lower().split():
            if word not in stop_words:
                words.append(word)
    return pd.DataFrame(Counter(words).most_common(20))


def emoji_helper(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]

    emojis=[]
    for msg in df['message']:
        emojis.extend([c for c in msg if emoji.is_emoji(c)])
    
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_timeline(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time']=time
    return timeline   


def daily_timeline(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    daily_timeline=df.groupby('daily').count()['message'].reset_index()
    return daily_timeline

def week_act_map(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    return df['day_name'].value_counts()

def monthly_act_map(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    return df['month'].value_counts()


def act_heat_map(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    
    act_heatmap=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return act_heatmap
