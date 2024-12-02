import matplotlib.pyplot as plt
import numpy as np
import os

# Generate a random star chart
def generate_star_chart():
    stars = np.random.rand(50, 2)
    plt.figure(figsize=(5, 5))
    plt.scatter(stars[:, 0], stars[:, 1], c="white", edgecolor="blue")
    plt.gca().set_facecolor("black")
    plt.title("Today's Random Star Chart")
    output_path = "results/star_chart.png"
    plt.savefig(output_path)
    plt.close()
    print(f"Star chart saved to {output_path}")

if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)
    generate_star_chart()