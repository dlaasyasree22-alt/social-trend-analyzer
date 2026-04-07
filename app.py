import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob

# Page config
st.set_page_config(page_title="YouTube Trends Analyzer", 
                   page_icon="📊", layout="wide")

# Title
st.title("📊 YouTube Trending Videos Analyzer")
st.markdown("### Explore what makes a video trend on YouTube!")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/youtube.csv', encoding='latin-1')
    def get_sentiment(title):
        analysis = TextBlob(str(title))
        if analysis.sentiment.polarity > 0:
            return 'Positive'
        elif analysis.sentiment.polarity < 0:
            return 'Negative'
        else:
            return 'Neutral'
    df['sentiment'] = df['title'].apply(get_sentiment)
    df['engagement_rate'] = (df['likes'] / df['views']) * 100
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")
countries = ['All'] + list(df['publish_country'].unique())
selected_country = st.sidebar.selectbox("Select Country", countries)
selected_day = st.sidebar.multiselect("Select Day", 
    df['published_day_of_week'].unique(),
    default=list(df['published_day_of_week'].unique()))

# Filter data
if selected_country != 'All':
    filtered_df = df[(df['publish_country'] == selected_country) & 
                     (df['published_day_of_week'].isin(selected_day))]
else:
    filtered_df = df[df['published_day_of_week'].isin(selected_day)]

# KPI metrics
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Videos", f"{len(filtered_df):,}")
col2.metric("Avg Views", f"{filtered_df['views'].mean():,.0f}")
col3.metric("Avg Likes", f"{filtered_df['likes'].mean():,.0f}")
col4.metric("Avg Engagement", f"{filtered_df['engagement_rate'].mean():.2f}%")

st.markdown("---")

# Row 1 charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top 10 Trending Channels")
    fig, ax = plt.subplots(figsize=(8,5))
    top_channels = filtered_df['channel_title'].value_counts().head(10)
    sns.barplot(x=top_channels.values, y=top_channels.index,
                hue=top_channels.index, palette='viridis', legend=False, ax=ax)
    ax.set_xlabel("Times Trending")
    st.pyplot(fig)

with col2:
    st.subheader("📅 Best Day to Post")
    fig, ax = plt.subplots(figsize=(8,5))
    day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    sns.countplot(data=filtered_df, x='published_day_of_week', 
                  order=day_order, hue='published_day_of_week',
                  palette='coolwarm', legend=False, ax=ax)
    ax.set_xlabel("Day")
    ax.set_ylabel("Count")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Row 2 charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("❤️ Sentiment Analysis")
    fig, ax = plt.subplots(figsize=(8,5))
    sns.countplot(data=filtered_df, x='sentiment',
                  hue='sentiment',
                  palette={'Positive':'green','Negative':'red','Neutral':'gray'},
                  legend=False, ax=ax)
    st.pyplot(fig)

with col2:
    st.subheader("👀 Views vs Likes")
    fig, ax = plt.subplots(figsize=(8,5))
    sns.scatterplot(data=filtered_df.sample(500), x='views', y='likes',
                    alpha=0.5, color='coral', ax=ax)
    st.pyplot(fig)

st.markdown("---")
st.markdown("Built with ❤️ by Laasya Sree | 2nd Year AI & DS")