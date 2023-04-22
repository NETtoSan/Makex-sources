
scores = 3
subjects = ["math", "physics", "programming"]
score = []

for i in range(scores): 
    a = int(input(f"Score for {subjects[i]} (100): "))
    score.append(a)
avg_score = sum(score) / len(score)

print(f"Average score: {avg_score}")
print("Your grade is A") if avg_score > 80 else print("Your grade is B") if avg_score > 60 else print("Your grade is C") if avg_score > 50 else print("Your gradfe is F")
