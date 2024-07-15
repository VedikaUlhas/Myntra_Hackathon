import requests
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
import numpy as np

# Function to fetch YouTube data using API
def fetch_youtube_data(api_key, query):
    url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&q={query}&part=snippet&type=video"
    response = requests.get(url)
    return response.json()

# Example usage: Fetch YouTube data
api_key = 'AIzaSyBOSM6KO7af3cPtcwjCoLkb-qdh0-ACdiI'
query = 'Myntra'
youtube_data = fetch_youtube_data(api_key, query)

# Define the base class
Base = declarative_base()

# Define the Users table
class User(Base):
    __tablename__ = 'Users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    email = Column(String(100))
    phone = Column(String(15))

# Define the YouTubeVideos table
class YouTubeVideo(Base):
    __tablename__ = 'YouTubeVideos'
    video_id = Column(String(50), primary_key=True)
    title = Column(String(255))
    description = Column(Text)
    view_count = Column(Integer)
    like_count = Column(Integer)
    dislike_count = Column(Integer)
    comment_count = Column(Integer)

# Define the YouTubeInteractions table
class YouTubeInteraction(Base):
    __tablename__ = 'YouTubeInteractions'
    interaction_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    video_id = Column(String(50), ForeignKey('YouTubeVideos.video_id'))
    interaction_type = Column(String(50))
    interaction_date = Column(TIMESTAMP)

    user = relationship('User')
    video = relationship('YouTubeVideo')

# Function to initialize database and session
def setup_database():
    engine = create_engine('postgresql+psycopg2://postgres:Sairam123@localhost/mydatabase')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

# Function for data processing and analysis
def process_data(youtube_data):
    items = youtube_data['items']
    processed_items = []

    for item in items:
        video_id = item['id']['videoId']
        snippet = item['snippet']
        title = snippet['title']
        description = snippet['description']
        # Add more fields if needed and if available in API response
        processed_items.append({
            'video_id': video_id,
            'title': title,
            'description': description,
            'view_count': 0,  # Placeholder if actual counts are not in the response
            'like_count': 0,
            'dislike_count': 0,
            'comment_count': 0
        })
    
    youtube_df = pd.DataFrame(processed_items)
    youtube_df.dropna(inplace=True)

    return youtube_df

# Function for recommendation system using collaborative filtering
def train_recommendation_system(interactions_df):
    # Create a user-video matrix
    user_video_matrix = interactions_df.pivot_table(index='user_id', columns='video_id', values='rating').fillna(0)

    # Calculate the cosine similarity
    similarity_matrix = cosine_similarity(user_video_matrix)
    similarity_df = pd.DataFrame(similarity_matrix, index=user_video_matrix.index, columns=user_video_matrix.index)

    return similarity_df

# Function to get recommendations for a user
def get_recommendations(user_id, similarity_df, interactions_df, num_recommendations=5):
    similar_users = similarity_df[user_id].sort_values(ascending=False).index[1:]
    recommended_videos = []

    for similar_user in similar_users:
        user_videos = interactions_df[interactions_df['user_id'] == similar_user]['video_id'].values
        recommended_videos.extend(user_videos)

        if len(recommended_videos) >= num_recommendations:
            break

    return recommended_videos[:num_recommendations]

# Main function to orchestrate the process
def main():
    # Fetch YouTube data
    api_key = 'AIzaSyBOSM6KO7af3cPtcwjCoLkb-qdh0-ACdiI'
    query = 'Myntra'
    youtube_data = fetch_youtube_data(api_key, query)

    # Initialize database session
    session = setup_database()

    # Process data
    processed_data = process_data(youtube_data)

    # Example interaction data
    interactions_df = pd.DataFrame({
        'user_id': [1, 2, 3, 4, 5],
        'video_id': ['vid1', 'vid2', 'vid3', 'vid4', 'vid5'],
        'rating': [3, 4, 2, 5, 3]
    })

    # Train recommendation system
    similarity_df = train_recommendation_system(interactions_df)

    # Get recommendations for a specific user
    user_id = 3
    recommendations = get_recommendations(user_id, similarity_df, interactions_df)

    print(f'Recommendations for user {user_id}: {recommendations}')

    # Close the session
    session.close()

if __name__ == "__main__":
    main()
