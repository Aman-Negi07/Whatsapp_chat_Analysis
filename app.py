import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)

    #fetch unique user
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):
        st.title("Top Statistics")
        num_messages,words,num_media,links=helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        
        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Total Media")
            st.title(num_media)
        
        with col4:
            st.header("Total Links Shared")
            st.title(len(links))

        # Monthly Timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Daily Timeline
        st.title("Daily Timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['daily'],daily_timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Activity Map
        st.title("Activity Map")
        col1,col2=st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day=helper.week_act_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        with col2:
            st.header("Most Busy Month")
            busy_month=helper.monthly_act_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap=helper.act_heat_map(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)





        # Display all links in the sidebar
        if len(links) > 0:
            dropdown_options = [f"{(link)}: {link}" for link in links]
            selected_link = st.sidebar.selectbox("Select a link to view details", dropdown_options)

        else:
            st.sidebar.subheader("No links shared.")

        #finding the most busy user in the group(Only Group level)
        if selected_user=="Overall":
            st.title("Most Busy Users")
            x,new_df=helper.fetch_most_busy_user(df)
            fig, ax=plt.subplots(figsize=(10, 8))

            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        

        #WordCloud
        st.title('Word Cloud')
        df_wc=helper.create_word_cloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #Most_Common_Words

        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)

        #Emoji Analysis
        st.title("Emoji Analyser")
        emoji_df=helper.emoji_helper(selected_user,df)
        col1,col2=st.columns(2)

        with col1:
             st.dataframe(emoji_df)
        rcParams['font.family'] = 'Segoe UI Emoji'  # For Windows
        with col2:
            fig, ax = plt.subplots()
            ax.pie(
                emoji_df[1].head(),  # Values for the pie chart
                labels=emoji_df[0].head(),  # Emoji labels
                autopct="%0.2f%%"  # Percentage format
            )
            st.pyplot(fig)


    