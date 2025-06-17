import os
import json

class HighScore:
    def __init__(self, filename='highscores.json'):
        self.filename = filename
        self.scores = self.load_scores()

    def load_scores(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return []

    def save_scores(self):
        with open(self.filename, 'w') as f:
            json.dump(self.scores, f)

    def add_score(self, name, score):
        self.scores.append({'name': name, 'score': score})
        self.scores = sorted(self.scores, key=lambda x: x['score'], reverse=True)[:5]  # Nur die besten 5
        self.save_scores()

    def get_scores(self):
        return self.scores