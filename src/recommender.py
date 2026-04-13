from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns top k recommended songs for the user."""
        # Convert UserProfile to dict for compatibility with score_song
        user_prefs = {
            'genre': user.favorite_genre,
            'mood': user.favorite_mood,
            'energy': user.target_energy,
            'likes_acoustic': user.likes_acoustic
        }

        # Score all songs
        scored_songs = []
        for song in self.songs:
            # Convert Song object to dict for score_song function
            song_dict = {
                'id': song.id,
                'title': song.title,
                'artist': song.artist,
                'genre': song.genre,
                'mood': song.mood,
                'energy': song.energy,
                'tempo_bpm': song.tempo_bpm,
                'valence': song.valence,
                'danceability': song.danceability,
                'acousticness': song.acousticness
            }
            score, _ = score_song(user_prefs, song_dict)
            scored_songs.append((song, score))

        # Sort by score and return top k Song objects
        sorted_songs = sorted(scored_songs, key=lambda x: x[1], reverse=True)
        return [song for song, _ in sorted_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns explanation for why a song was recommended."""
        user_prefs = {
            'genre': user.favorite_genre,
            'mood': user.favorite_mood,
            'energy': user.target_energy,
            'likes_acoustic': user.likes_acoustic
        }

        song_dict = {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'genre': song.genre,
            'mood': song.mood,
            'energy': song.energy,
            'tempo_bpm': song.tempo_bpm,
            'valence': song.valence,
            'danceability': song.danceability,
            'acousticness': song.acousticness
        }

        score, reasons = score_song(user_prefs, song_dict)
        explanation = f"Score: {score:.2f} - " + "; ".join(reasons)
        return explanation

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    songs = []
    print(f"Loading songs from {csv_path}...")

    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Convert numerical values to appropriate types
            song = {
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness'])
            }
            songs.append(song)

    print(f"Loaded {len(songs)} songs.")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []

    # Genre match: +2.0 points
    if song['genre'] == user_prefs.get('genre'):
        score += 2.0
        reasons.append(f"Genre match: {song['genre']} (+2.0)")

    # Mood match: +1.0 point
    if song['mood'] == user_prefs.get('mood'):
        score += 1.0
        reasons.append(f"Mood match: {song['mood']} (+1.0)")

    # Energy proximity: Calculate similarity score (max +1.5 points)
    # Closer energy values = higher score
    if 'energy' in user_prefs:
        energy_diff = abs(song['energy'] - user_prefs['energy'])
        energy_score = max(0, 1.5 * (1 - energy_diff))
        score += energy_score
        reasons.append(f"Energy similarity: {energy_score:.2f} (target: {user_prefs['energy']:.2f}, song: {song['energy']:.2f})")

    # Acousticness preference (optional): +0.5 or -0.5 points
    if 'likes_acoustic' in user_prefs:
        if user_prefs['likes_acoustic'] and song['acousticness'] > 0.6:
            score += 0.5
            reasons.append(f"High acousticness match (+0.5)")
        elif not user_prefs['likes_acoustic'] and song['acousticness'] < 0.3:
            score += 0.5
            reasons.append(f"Low acousticness match (+0.5)")

    # Valence bonus (optional): matches happiness preference
    if 'valence' in user_prefs:
        valence_diff = abs(song['valence'] - user_prefs['valence'])
        valence_score = max(0, 0.5 * (1 - valence_diff))
        score += valence_score
        if valence_score > 0.3:
            reasons.append(f"Valence similarity: {valence_score:.2f}")

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # Score all songs
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        # Create explanation string from reasons
        explanation = "; ".join(reasons) if reasons else "No matching features"
        scored_songs.append((song, score, explanation))

    # Sort by score (highest first) and return top k
    sorted_songs = sorted(scored_songs, key=lambda x: x[1], reverse=True)
    return sorted_songs[:k]
