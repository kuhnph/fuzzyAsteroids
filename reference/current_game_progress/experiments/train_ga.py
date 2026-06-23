from training import TrainingAgent


def main():
    agent = TrainingAgent()

    # First call initializes the GA
    agent.train_step()

    while True:
        agent.train_step()


if __name__ == "__main__":
    main()