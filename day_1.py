import networkx as nx
import random
import pandas as pd
import matplotlib.pyplot as plt

plt.ion()

def schedule_events(events, conflicts):
    """
    Assigns rooms to events to minimize the number of rooms used while avoiding conflicts.

    :param events: List of events (vertices in the graph).
    :param conflicts: List of pairs of conflicting events (edges in the graph).
    :return: A dictionary with event-room assignments and the total number of rooms.
    """
    # Step 1: Create a graph
    G = nx.Graph()
    G.add_nodes_from(events)
    G.add_edges_from(conflicts)

    # Step 2: Perform greedy coloring
    room_assignment = nx.coloring.greedy_color(G, strategy="largest_first")
    
    # Step 3: Count the total rooms used
    total_rooms = max(room_assignment.values()) + 1 if room_assignment else 0

    return total_rooms


def generate_random_data(num_events, conflict_probability):
    """
    Generate random events and conflicts.

    :param num_events: Number of events.
    :param conflict_probability: Probability of a conflict between any two events (0 to 1).
    :return: List of events and their conflicts.
    """
    events = [f"E{i}" for i in range(1, num_events + 1)]
    conflicts = [
        (e1, e2)
        for i, e1 in enumerate(events)
        for e2 in events[i + 1 :]
        if random.random() < conflict_probability
    ]
    return events, conflicts


def run_parametrized_tests(event_sizes, conflict_probs, repetitions):
    """
    Run tests for different configurations of event sizes and conflict probabilities.

    :param event_sizes: List of event sizes to test.
    :param conflict_probs: List of conflict probabilities to test.
    :param repetitions: Number of times to repeat each configuration for averaging.
    :return: DataFrame summarizing results.
    """
    results = []

    for num_events in event_sizes:
        for conflict_prob in conflict_probs:
            for _ in range(repetitions):
                # Generate data
                events, conflicts = generate_random_data(num_events, conflict_prob)
                # Compute number of rooms
                total_rooms = schedule_events(events, conflicts)
                # Record results
                results.append({
                    "num_events": num_events,
                    "conflict_probability": conflict_prob,
                    "total_rooms": total_rooms
                })

    # Convert results to DataFrame
    df = pd.DataFrame(results)
    return df


# Parameters for testing
event_sizes = [10, 20, 50, 100, 200]  # Number of events to test
conflict_probs = [0.1, 0.3, 0.5, 0.7, 0.9]  # Conflict probabilities to test
repetitions = 5  # Repeat each configuration 5 times

# Run the tests
results_df = run_parametrized_tests(event_sizes, conflict_probs, repetitions)

# Display results
print(results_df)

# Analyze results
# Plot the average number of rooms needed as a function of event size and conflict probability
avg_results = results_df.groupby(["num_events", "conflict_probability"]).mean().reset_index()

for conflict_prob in conflict_probs:
    subset = avg_results[avg_results["conflict_probability"] == conflict_prob]
    plt.plot(subset["num_events"], subset["total_rooms"], label=f"p={conflict_prob}")

plt.xlabel("Number of Events")
plt.ylabel("Average Number of Rooms Needed")
plt.title("Greedy Algorithm Performance")
plt.legend()
plt.grid()
plt.show(block=True)
plt.savefig("greedy_algorithm_performance.png")