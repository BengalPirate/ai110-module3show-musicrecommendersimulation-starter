# 🎵 Music Recommender Simulation

## Project Summary

**MoodMatch Recommender v1.0** is a content-based music recommendation system that suggests songs based on user taste profiles. This educational simulation demonstrates how platforms like Spotify and TikTok transform user preferences into personalized recommendations.

### What This System Does

This recommender:
- **Analyzes 25 songs** across diverse genres (pop, lofi, rock, jazz, EDM, metal, blues, classical, and more)
- **Scores each song** using a weighted algorithm that considers genre match (+2.0 pts), mood match (+1.0 pt), energy similarity (up to +1.5 pts), acousticness preference (+0.5 pts), and valence similarity (up to +0.5 pts)
- **Ranks songs** from highest to lowest score and returns the top 5 recommendations
- **Explains why** each song was recommended with transparent scoring breakdowns

### Key Learning Outcomes

Through building and testing this system, I explored:
- How **content-based filtering** works vs. collaborative filtering
- How **data imbalance** creates bias even when algorithms are mathematically fair
- How **weighted scoring** can create "filter bubbles" that limit musical discovery
- Why **transparency** matters in AI systems that influence what culture we consume

---

## How The System Works

This music recommender simulates how platforms like Spotify and TikTok predict what users will enjoy next. Real-world recommendation systems typically use two main approaches:

1. **Collaborative Filtering**: Uses behavior from other users (e.g., "people who liked Song A also liked Song B")
2. **Content-Based Filtering**: Uses song attributes like genre, mood, energy, and tempo to match user preferences

Our simulation uses a **content-based approach** with the following design:

### Song Features
Each song in our catalog includes:
- **Categorical**: genre, mood, artist, title
- **Numerical**: energy (0.0-1.0), tempo_bpm, valence (happiness), danceability, acousticness

### User Profile
The user profile captures taste preferences:
- `favorite_genre`: preferred music genre (e.g., "pop", "rock", "lofi")
- `favorite_mood`: desired emotional vibe (e.g., "happy", "chill", "intense")
- `target_energy`: energy level preference (0.0-1.0 scale)
- `likes_acoustic`: preference for acoustic vs. electronic sounds

### Scoring Algorithm ("Algorithm Recipe")
The recommender scores each song using a weighted point system:
- **+2.0 points** for exact genre match
- **+1.0 point** for exact mood match
- **Similarity score** based on energy proximity (closer = higher score)
- **Bonus/penalty** based on acousticness preference

### Ranking Process
1. Load all songs from the catalog (CSV file)
2. For each song, calculate a score using the user's profile
3. Sort songs by score (highest to lowest)
4. Return the top K recommendations with explanations

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

### Profile Comparison Experiments

**1. High-Energy Pop Fan vs. Chill Lofi Listener**
- **Pop Fan Results**: Top recommendation was "Sunrise City" (score: 4.47) - perfect genre + mood + energy match
- **Lofi Listener Results**: Top recommendations were all lofi tracks with high acousticness
- **Observation**: The system successfully differentiates between high-energy and low-energy preferences. Genre matching has strong influence (2.0 points) which helps surface the right category.

**2. Intense Rock vs. Energetic EDM**
- **Rock Profile**: "Storm Runner" scored 4.98 with perfect genre/mood/energy alignment
- **EDM Profile**: "Digital Dreams" scored 5.40 (highest across all tests) due to all factors aligning including valence
- **Observation**: Both prefer high energy (0.9+) but genre match correctly separates rock from EDM. The acousticness penalty/bonus also helps distinguish electronic (EDM) from guitar-driven (rock) music.

**3. Edge Case - Melancholic Blues with Low Energy**
- **Result**: "Rainy Day Blues" scored 4.48 - exactly what we'd expect
- **Observation**: The system handles users with sad moods appropriately. When only 1 song exists in the preferred genre, the system falls back to energy similarity, suggesting ambient and classical tracks with similar low energy levels.

### Weight Adjustment Experiments

**Baseline Weights**:
- Genre match: +2.0
- Mood match: +1.0
- Energy similarity: up to +1.5
- Acousticness bonus: +0.5
- Valence similarity: up to +0.5

**Finding**: Genre weight of 2.0 provides strong but not overwhelming influence. Songs can still rank high (3.0-4.0) without a genre match if they nail mood and energy. This creates a good balance between filtering by category and discovering cross-genre recommendations.

---

## Limitations and Risks

### Data Limitations
- **Small catalog**: Only 25 songs means limited variety and potential for repetitive recommendations
- **Genre imbalance**: Pop and lofi have more representation (3-4 songs each) while most genres have only 1 song, creating bias toward well-represented genres
- **No cultural context**: The system doesn't understand lyrics, language, cultural significance, or artist reputation

### Algorithmic Biases
- **Genre weight dominance**: The +2.0 genre bonus means users may get trapped in a "filter bubble" - always seeing their preferred genre even when other genres might match their mood/energy better
- **Energy-centric**: Heavy emphasis on energy similarity may ignore users who care more about tempo, danceability, or lyrical themes
- **Binary acousticness**: The 0.6 threshold for "high acousticness" is arbitrary and may misclassify songs
- **Cold start problem**: New users without established preferences get no personalization

### Fairness Concerns
- **Underrepresented genres**: A user who likes country, gothic, or classical music has very limited options (1 song each)
- **Mood diversity**: "Happy" is overrepresented compared to "sad," potentially marginalizing users seeking emotional depth
- **Artist diversity**: Some artists (LoRoom, Neon Echo) appear multiple times, creating potential for over-recommendation of certain artists

---

## Reflection

Read the complete [**Model Card**](model_card.md) for full documentation.

### What I Learned About Recommenders

This project fundamentally changed how I understand recommendation systems. I learned that **data becomes predictions through weighted scoring**—each song attribute (genre, mood, energy) contributes points based on how closely it matches user preferences, and the system simply ranks songs by total score. What seemed like "AI magic" is actually transparent mathematics: genre match (+2.0) + mood match (+1.0) + energy similarity (+1.5) = a personalized recommendation.

The most important insight was recognizing where **bias enters the system**. Even though my algorithm treats all genres mathematically equal, users who like pop or lofi have a better experience because those genres have more songs in the catalog. This taught me that fairness isn't just about writing unbiased code—it's about ensuring equal representation in the training data. A system can be algorithmically "fair" but still produce unfair outcomes if the dataset itself is imbalanced.

I was also surprised by the **filter bubble effect** I unintentionally created. By giving genre a +2.0 weight, I made it nearly impossible for pop fans to discover jazz, even when mood and energy perfectly aligned. Real platforms like Spotify face this same challenge: how do you balance giving users what they ask for versus introducing them to new music they might love? This project showed me that recommendation systems aren't neutral—they actively shape what we discover (or don't discover).

Finally, building the "Because" explanations made me realize how valuable **transparency** is. When my system says "Genre match: lofi (+2.0); Mood match: chill (+1.0)," users can understand and trust the recommendation. Most real-world systems hide this logic, but this project convinced me that users deserve to see how decisions are made, especially when those decisions influence what culture and art they consume.


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

