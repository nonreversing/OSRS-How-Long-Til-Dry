import matplotlib.pyplot as plt
from scipy.stats import binom
import numpy as np
import tkinter as tk
from tkinter import simpledialog, messagebox
from fractions import Fraction

# Function to calculate cumulative probability of getting at least k successes
def cumulative_at_least_k(n, k, p):
    return 1 - binom.cdf(k-1, n, p)

# Function to find the minimum number of trials
def find_min_trials(p, k, target_probability):
    n = 2
    while cumulative_at_least_k(n, k, p) < target_probability:
        n += 1
    return n

# Function to plot the results
def plot_results(n, k, p, target_probability):
    n_values = np.arange(2, n+1)
    probabilities = [cumulative_at_least_k(n, k, p) for n in n_values]

    fraction_p = Fraction(p).limit_denominator()

    plt.figure(figsize=(10, 6))
    plt.plot(n_values, probabilities, label='Cumulative Probability of At Least {} Successes'.format(k))
    plt.axhline(y=target_probability, color='r', linestyle='--', label='{:.0%} Probability'.format(target_probability))
    plt.axvline(x=n, color='g', linestyle='--', label=f'Minimum n = {n}')
    plt.xlabel('Number of Trials (n)')
    plt.ylabel('Cumulative Probability')
    plt.title('Cumulative Probability of Getting At Least {} Successes'.format(k))
    plt.legend(title=f'Success Rate: $\mathbf{{{fraction_p}}}$')
    plt.grid(True)
    plt.show()

# Function to convert probability input
def parse_probability(prob_input):
    if '/' in prob_input:
        numerator, denominator = map(float, prob_input.split('/'))
        return numerator / denominator
    else:
        return float(prob_input)

# Function to convert target probability input
def parse_target_probability(target_input):
    if '%' in target_input:
        return float(target_input.strip('%')) / 100
    else:
        return float(target_input)

# Function to prompt user for input and calculate results
def get_user_input():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Prompt user for inputs
    prob_input = simpledialog.askstring("Input", "Enter the probability of success (e.g., 0.0002 or 1/5000):")
    p = parse_probability(prob_input)
    k = int(simpledialog.askstring("Input", "Enter the number of successes (e.g., 2):"))
    target_input = simpledialog.askstring("Input", "Enter the target probability (e.g., 0.5 or 50%):")
    target_probability = parse_target_probability(target_input)

    # Calculate the minimum number of trials
    n = find_min_trials(p, k, target_probability)
    prob = cumulative_at_least_k(n, k, p)

    # Show result in a message box
    # messagebox.showinfo("Result", f"The minimum number of trials needed is {n}, with a cumulative probability of {prob:.4f}")

    # Plot the results
    plot_results(n, k, p, target_probability)

# Run the function to get user input
get_user_input()
