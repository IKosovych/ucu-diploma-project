import json
import matplotlib.pyplot as plt

with open('evaluation_results/topic_comparison_results.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

scores = [entry['score'] for entry in data]

plt.figure(figsize=(10, 6))
plt.hist(scores, bins=20, edgecolor='black', alpha=0.7)
plt.xlabel('Scores')
plt.ylabel('Frequency')
plt.title('Distribution of Topic Comparison Scores')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()