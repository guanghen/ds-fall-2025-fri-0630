import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


df_EC = pd.read_csv("movie_ratings_EC.csv")
df = pd.read_csv("movie_ratings.csv")
df_exploded = df.copy()
st.title("This is the MovieLens Data Analysis")
st.header("Use the filter in sidebar to show the specific dataset")
st.sidebar.header("Filter Options")
#Filter the age
age_range = st.sidebar.slider("Please select the age range", min_value=1, max_value=130, value=(0, 130))

#filter the occupation
occupation = sorted(df_EC["occupation"].unique())
occupations_selection = st.sidebar.multiselect("Please select the occupation you want to check (Leave empty as select all)", options = occupation, default = [])

#filter the gender
gender_selection = st.sidebar.selectbox("Please select gender", options = ["Both","Male","Female"])

#filter the genres
genres = sorted(df["genres"].unique())
all_genres_option = "All Genres"
genres.insert(0, all_genres_option)
selected_genre = st.sidebar.selectbox('Select a genre:',options=genres)

filtered_df = df_EC.copy()
#Modify the dataframe base on the filter
filtered_df = filtered_df[(filtered_df['age'] >= age_range[0]) & (filtered_df['age'] <= age_range[1])] #Deploy age filter
df = df[(df["age"]>=age_range[0]) & (df['age'] <= age_range[1])]
if occupations_selection:
    filtered_df = filtered_df[filtered_df['occupation'].isin(occupations_selection)] #Deploy genres filter
    df = df[df['occupation'].isin(occupations_selection)]

if gender_selection == "Male":
    filtered_df = filtered_df[filtered_df["gender"] == "M"]
    df = df[df["gender"] == "M"]

if gender_selection == "Female":
    filtered_df = filtered_df[filtered_df["gender"] == "F"] #Deploy gender filter
    df = df[df["gender"]=="F"]

if selected_genre != all_genres_option:
    df = df[df["genres"] == selected_genre]
    st.write(df)
else:
    st.write(filtered_df)

#begin data visiliaztion for answering question 1
st.header("Here is the chart for the breakdown of genres for the movies that were rated")
genre_counts = df_exploded['genres'].value_counts()
sns.set_style("whitegrid")
fig = plt.figure(figsize=(12, 8))
sns.barplot(x=genre_counts.values,y=genre_counts.index, palette = "Greens_r")
plt.title('Breakdown of Movie Genres', fontsize=16)
plt.xlabel('Number of Movies', fontsize=12)
plt.ylabel('Genre', fontsize=12)
st.pyplot(fig)
st.markdown("""
- Based on the chart shown above, we can see that drama, comedy, and action have the highest amount of ratings
""")
#for question 2
st.header("Here is the chart for the genres have the highest viewer satisfaction")
st.text("Only the genres that have more than 100 ratings would be count")
genres_stat = df_exploded.groupby("genres")["rating"].agg(["count","mean"])
popular_genres = genres_stat[genres_stat["count"]>=100]
popular_genres_sorted = popular_genres.sort_values(by='mean', ascending=False)
sns.set_style("whitegrid")
fig = plt.figure(figsize=(12, 8))
sns.barplot(x=popular_genres_sorted["mean"],y=popular_genres_sorted.index, palette = "viridis")
plt.title('Rating of the popular genres', fontsize=16)
plt.xlabel('Ratings', fontsize=12)
plt.ylabel('Genres', fontsize=12)
st.pyplot(fig)
st.markdown("""
- Based on the chart shown above, Film-Noir has the highest rating
- The ratings of the popular genres are all between the range 3.0 - 4.0
- The gap of each consecutive genres are pretty close
""")
#for question 3
st.header("The is the chart for the change of ratings across the year of movie release")
year_rating = df_EC.groupby("year")["rating"].mean().sort_index()
fig, ax = plt.subplots(figsize=(14, 7))
sns.lineplot(x=year_rating.index, y=year_rating.values, palette="Greens", marker='o', ax=ax)
ax.set_title('Average Movie Rating by Release Year', fontsize=16)
ax.set_xlabel('Release Year', fontsize=12)
ax.set_ylabel('Average Rating', fontsize=12)
ax.grid(True)
ax.set_xlim(year_rating.index.min() - 1, year_rating.index.max() + 1)
st.pyplot(fig)
st.markdown("""
- Ratings for early films fluctuate significantly (before approximately 1960). This might because the number of early movies is prtty small, one or two classic films with extremely high (or low) ratings can significantly affect the average score for that year, causing the data to appear erratic
- 1960-1985 The overall average score remains at a relatively high level. This may reflect a "golden age" of filmmaking 
- After 1985 The average score of the movie showed a continuous downward trend, dropping from about 3.8 points to around 3.3 points.""")

#for question 4: What are the 5 best-rated movies that have at least 50 ratings? At least 150 ratings?
st.header("The top 5 movies rating ")
movie_df = df_EC.groupby("title")["rating"].agg(['count', "mean"])
col1, col2 = st.columns(2)
with col1:
    st.text("This is Top 5 (≥50 ratings)")
    pupular_movie_df = movie_df[movie_df['count']>=50].sort_values(by = "mean", ascending=False).head(5)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax = sns.barplot(x=pupular_movie_df['mean'],y=pupular_movie_df.index, palette = "viridis")
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f', fontsize=12, padding=3)
    ax.set_xlim(right=max(pupular_movie_df['mean']) * 1.1)
    plt.title('Top 5 (≥50 ratings)', fontsize=16)
    plt.xlabel('Ratings', fontsize=12)
    plt.ylabel('movie title', fontsize=12)
    st.pyplot(fig)
with col2:
    st.text("This is Top 5 (≥150 ratings)")
    popular_150 = movie_df[movie_df['count'] >= 150].sort_values(by="mean", ascending=False).head(5)

    fig2, ax2 = plt.subplots(figsize=(6, 6))
    sns.barplot(x=popular_150['mean'], y=popular_150.index, palette="magma", ax=ax2)

    for container in ax2.containers:
        ax2.bar_label(container, fmt='%.2f', fontsize=12, padding=3)
    ax2.set_xlim(right=max(popular_150['mean']) * 1.1)
    ax2.set_title("Top 5 (≥150 ratings)", fontsize=16)
    ax2.set_xlabel("Ratings", fontsize=12)
    ax2.set_ylabel("Movie title", fontsize=12)
    st.pyplot(fig2)
st.markdown("""
    - For movies with ≥50 ratings, highly rated short films and classics such as A Close Shave (1995), Schindler's List (1993), 
    and Casablanca (1942) appear at the top, with average ratings above 4.4. This suggests that even less mainstream films with 
    smaller audiences can still achieve very high ratings if they are well-received  
    - For movies with ≥150 ratings, the list shifts slightly toward more widely recognized titles such as Shawshank Redemption 
    (1994) and Star Wars (1977). The ratings remain high (around 4.3-4.5), but the inclusion of these widely popular movies shows 
    how requiring a larger number of ratings favors films with broader audiences. 
    """)
    
    