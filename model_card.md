# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**MoodMatch Recommender v1.0**

---

## 2. Intended Use

This recommender system is designed for **classroom exploration and learning purposes only**—not for real users or production deployment.

**What it does:**
- Generates personalized song recommendations from a small catalog based on user taste preferences
- Ranks songs by calculating similarity scores across multiple musical attributes
- Provides transparent explanations for why each song was recommended

**Assumptions:**
- Users can describe their preferences using simple categories (genre, mood, energy level)
- Musical taste can be represented numerically using features like energy, acousticness, and valence
- Users want recommendations that closely match their stated preferences (not necessarily diverse suggestions)

**Use case:** Educational tool to understand how content-based filtering works in real music platforms like Spotify or TikTok.

---

## 3. How the Model Works

The recommender uses a **weighted scoring system** to match songs to user preferences:

1. **Genre Matching** (highest weight): If the song's genre exactly matches what the user prefers (e.g., "pop"), it earns 2.0 bonus points. This ensures the system respects broad categorical preferences.

2. **Mood Matching** (medium weight): If the song's emotional vibe (e.g., "happy," "chill," "intense") matches the user's desired mood, it earns 1.0 bonus point.

3. **Energy Similarity** (continuous scoring): The system measures how close the song's energy level (0.0 = calm, 1.0 = intense) is to the user's target. Songs with nearly identical energy levels earn up to 1.5 points, with the score decreasing as the difference grows.

4. **Acousticness Preference** (optional): If the user prefers acoustic sounds, songs with high acousticness (guitars, pianos, natural instruments) get a 0.5 point bonus. If they prefer electronic sounds, low-acousticness tracks get the bonus instead.

5. **Valence Similarity** (happiness bonus): Songs with valence (musical positivity/happiness) similar to the user's preference can earn up to 0.5 additional points.

After scoring every song in the catalog, the system sorts them from highest to lowest score and returns the top 5 recommendations with explanations showing which features contributed to the score.

**Key design choice:** Genre has the strongest influence to prevent the system from recommending wildly different categories, but energy and mood still allow cross-genre discovery when they align well.

---

## 4. Data

**Catalog size:** 25 songs (expanded from the original 10 starter songs)

**Genre distribution:**
- Well-represented: pop (2 songs), lofi (4 songs), ambient (2 songs)
- Moderately represented: rock, jazz, EDM, synthwave
- Underrepresented: metal, reggae, blues, classical, dubstep, country, R&B, punk, latin, gothic, tropical house, jazz fusion (1 song each)

**Mood coverage:** The dataset includes happy, chill, intense, relaxed, focused, energetic, sad, moody, peaceful, romantic, rebellious, dark, nostalgic, and experimental moods.

**Changes made:** Added 15 diverse songs spanning metal to classical to ensure broader genre representation and enable more varied testing scenarios.

**What's missing:**
- No hip-hop, K-pop, or world music genres
- Limited representation of cultural diversity
- No lyrics or language-based features
- Artist popularity and social signals are absent
- Only one song per artist for most artists

---

## 5. Strengths

**Works well for:**
1. **Users with clear, specific preferences**: When someone wants "energetic pop music," the system confidently surfaces "Sunrise City" and "Gym Hero" with high scores.

2. **Energy-based differentiation**: The system successfully distinguishes between high-energy users (rock/EDM fans scoring 0.9) and low-energy users (lofi/jazz fans scoring 0.3-0.4), even across different genres.

3. **Transparent explanations**: Every recommendation shows exactly why it scored well (e.g., "Genre match: lofi (+2.0); Mood match: chill (+1.0)"), making the system's logic understandable and trustworthy.

4. **Cross-genre discovery**: Even without a perfect genre match, songs can rank highly if they nail the mood and energy. For example, a jazz lover might discover reggae tracks with similar relaxed vibes.

5. **Handling edge cases**: When testing a "melancholic blues" profile with only one blues song in the catalog, the system gracefully fell back to other low-energy, emotionally introspective tracks (ambient, classical) rather than breaking or giving nonsensical results.

---

## 6. Limitations and Bias

**Feature blindness:**
- Ignores tempo entirely (a 60 BPM song and 180 BPM song could score identically)
- Doesn't consider danceability explicitly in scoring
- No understanding of lyrics, artist style, or cultural context

**Genre bias and filter bubbles:**
- The +2.0 genre weight creates strong preference for exact matches, potentially trapping users in a narrow category
- Users who like niche genres (country, gothic, classical) get very limited options—just 1 song each
- Pop and lofi fans enjoy 3-4 songs each, creating an unfair advantage

**Mood imbalance:**
- "Happy" and "chill" moods dominate the dataset, while "sad" has minimal representation
- Users seeking emotional depth or melancholic music have fewer quality recommendations

**Arbitrary thresholds:**
- The 0.6 cutoff for "high acousticness" is hardcoded and may misclassify borderline songs
- Energy similarity uses a linear penalty, but musical perception isn't always linear

**Cold start problem:**
- New users with no history get the same generic results
- System doesn't adapt or learn from user feedback

**Artist over-representation:**
- Some artists (LoRoom, Neon Echo) appear multiple times, risking over-exposure

---

## 7. Evaluation

**Tested profiles:**
1. High-Energy Pop Fan (genre: pop, mood: happy, energy: 0.8)
2. Chill Lofi Study Session (genre: lofi, mood: chill, energy: 0.4, acoustic)
3. Intense Rock Enthusiast (genre: rock, mood: intense, energy: 0.9, electronic)
4. Relaxed Acoustic Vibes (genre: jazz, mood: relaxed, energy: 0.35, acoustic)
5. Energetic EDM Party Mode (genre: edm, mood: energetic, energy: 0.95, valence: 0.75)
6. Melancholic Blues Edge Case (genre: blues, mood: sad, energy: 0.3)

**What I looked for:**
- Do top results match the stated preferences?
- Does the system differentiate between similar but distinct profiles (e.g., rock vs. EDM)?
- How does it handle underrepresented genres?

**Surprising findings:**
- The EDM profile achieved the highest score ever (5.40) because all factors aligned, showing the system rewards comprehensive matches
- The melancholic blues profile worked despite having only 1 matching song, proving the energy fallback mechanism is effective
- Acousticness preference made a noticeable difference in separating electronic (EDM, rock) from organic (lofi, jazz) recommendations

**Manual verification:** Each profile's top recommendation made intuitive sense based on the stated preferences. No obviously "wrong" suggestions appeared in the top 5 for any profile.

---

## 8. Future Work

**Improvements to explore:**

1. **Tempo-based scoring**: Add tempo ranges (slow: <80 BPM, medium: 80-120, fast: >120) to better capture rhythm preferences

2. **Diversity injection**: Implement a "diminishing returns" penalty so the top 5 aren't all from the same artist or sub-genre

3. **Collaborative filtering**: Learn from what similar users liked to recommend songs outside the user's stated preferences

4. **Dynamic weight tuning**: Let users adjust how much they care about genre vs. mood vs. energy through sliders

5. **Context-aware recommendations**: Different suggestions for "morning commute" vs. "late-night study" vs. "Friday party"

6. **Expand dataset**: Add 100+ songs with balanced genre distribution and cultural diversity

7. **Hybrid scoring**: Combine content-based features with popularity metrics and recency to avoid recommending obscure or outdated tracks exclusively

8. **User feedback loop**: Allow thumbs up/down to refine future recommendations

---

## 9. Personal Reflection

Building this recommender taught me that **simple math can create surprisingly "smart" behavior**. Before this project, I thought Spotify's algorithms must be incredibly complex, but I now understand that even basic weighted scoring can produce relevant, personalized results when the features are well-chosen.

The most unexpected discovery was how **bias creeps in through data imbalance**, not just algorithm design. Even though my scoring logic treats all genres equally (each genre match gets +2.0 points), users who like pop or lofi effectively have a better experience because there are more options to choose from. This made me realize that fairness in AI isn't just about equal treatment in code—it's about equal representation in data.

I was also surprised by the **"filter bubble" effect** created by the genre weight. While testing, I noticed that pop fans almost never saw jazz recommendations, even when the energy and mood matched perfectly. Real-world platforms like TikTok and Spotify must face this challenge too: how do you balance giving users what they asked for vs. introducing them to new sounds they might love?

Finally, this project changed how I think about the **"Because"** explanations. When Spotify says "Recommended because you listened to similar songs," I used to assume it was vague marketing speak. Now I appreciate that behind every recommendation is a scoring function making specific decisions—and users deserve to see that logic, just like my system shows "Genre match: lofi (+2.0)."

This simulation is just the beginning, but it's given me a clearer mental model of how data becomes predictions, and where human judgment still matters in deciding what "good music" means for each listener.
