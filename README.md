


# 📚 Fuzzy Book Recommender

This repository contains a fuzzy logic-based book recommendation system built with Python. It leverages user interest in certain genres and the average rating of books to generate personalized recommendations.

## ✨ Features

- Utilizes fuzzy logic (via `scikit-fuzzy`) to handle uncertainty in user preferences.
- Filters books based on genre interest and rating.
- Combines fuzzy output with genre match scoring for better results.
- Simple command-line interface for input and display.

## 📂 Dataset

The book dataset is sourced from [Kaggle](https://www.kaggle.com/). Only a subset of books is used in this project for demonstration purposes.

Each book entry contains:
- Title
- Authors
- Categories (genres)
- Published year
- Average rating

## ⚙️ Fuzzy Logic Design

The fuzzy system uses the following inputs and outputs:

**Input Variables:**
- `Rating`: Range 0–5, categorized into Low, Medium, High
- `Interest (Minat)`: Range 0–10, based on user preference level

**Output Variable:**
- `Recommendation`: Range 0–10, categorized into Low, Medium, High

### 🧠 Fuzzy Rules

```text
IF Rating is High AND Interest is High THEN Recommendation is High  
IF Rating is High AND Interest is Medium THEN Recommendation is Medium  
IF Rating is Medium AND Interest is High THEN Recommendation is Medium  
IF Rating is Low OR Interest is Low THEN Recommendation is Low
````

## 🛠 How It Works

1. The user inputs their name and selects preferred genres.

2. The system asks how much they like those genres (on a scale of 1–5).

3. Books are filtered based on genre and rated using fuzzy logic.

4. A final recommendation score is calculated:

   ```
   Final Score = Fuzzy Recommendation Score + Genre Match Score
   ```

5. The top 20 book recommendations are displayed.

## 💻 Installation & Usage

```bash
# Install required libraries
pip install numpy pandas scikit-fuzzy

# Run the recommender
python main.py
```

> ⚠ Ensure you have the `filtered_data.csv` file (downloaded from Kaggle) in the same directory or update the path in the code accordingly.

## 🧾 Example Input

```bash
Nama: Sarah
Masukkan genre favorit: fantasy, mystery
Seberapa kamu suka genre-genre tersebut?
1 = Sangat suka
Pilihan (1-5): 1
```

## 📊 Sample Output

```
📚 Rekomendasi Buku untuk Sarah (fantasy, mystery):
------------------------------------------------------------------------------------------
Title              | Authors           | Categories       | Year | Rating | Final Score
Harry Potter 1     | J.K. Rowling      | Fantasy, Magic   | 1997 | 4.5    | 13.0
...
```

## 📎 File Structure

```
├── Filtering_data.py                # Main script
├── data.csv      # Dataset (from Kaggle)
└── README.md              # Project documentation
```


## 🙋‍♂️ Author

Created by Dos Hansel Sihombing – feel free to reach out with suggestions or contributions.

```


