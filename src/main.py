"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def print_recommendations(profile_name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Helper function to print recommendations for a user profile."""
    print(f"\n{'='*70}")
    print(f"Profile: {profile_name}")
    print(f"Preferences: {user_prefs}")
    print(f"{'='*70}\n")

    recommendations = recommend_songs(user_prefs, songs, k=k)

    print(f"Top {k} recommendations:\n")
    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"{i}. {song['title']} by {song['artist']}")
        print(f"   Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']:.2f}")
        print(f"   Score: {score:.2f}")
        print(f"   Because: {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Test Profile 1: High-Energy Pop Fan
    print_recommendations(
        "High-Energy Pop Fan",
        {"genre": "pop", "mood": "happy", "energy": 0.8},
        songs
    )

    # Test Profile 2: Chill Lofi Listener
    print_recommendations(
        "Chill Lofi Study Session",
        {"genre": "lofi", "mood": "chill", "energy": 0.4, "likes_acoustic": True},
        songs
    )

    # Test Profile 3: Intense Rock Enthusiast
    print_recommendations(
        "Intense Rock Enthusiast",
        {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False},
        songs
    )

    # Test Profile 4: Relaxed Acoustic Vibes
    print_recommendations(
        "Relaxed Acoustic Vibes",
        {"genre": "jazz", "mood": "relaxed", "energy": 0.35, "likes_acoustic": True},
        songs
    )

    # Test Profile 5: Energetic EDM Party Mode
    print_recommendations(
        "Energetic EDM Party Mode",
        {"genre": "edm", "mood": "energetic", "energy": 0.95, "likes_acoustic": False, "valence": 0.75},
        songs
    )

    # Test Profile 6: Sad Blues Listener (edge case - conflicting energy/mood)
    print_recommendations(
        "Melancholic Blues (Edge Case)",
        {"genre": "blues", "mood": "sad", "energy": 0.3},
        songs
    )


if __name__ == "__main__":
    main()
