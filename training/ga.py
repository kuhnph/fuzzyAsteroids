import array
import random
import numpy as np
from deap import algorithms, base, creator, tools


def build_toolbox(agent, chromosome_length, int_min=0, int_max=4):
    """
    Create and return a DEAP toolbox configured for this project.
    """
    if not hasattr(creator, "FitnessMin"):
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

    if not hasattr(creator, "Individual"):
        creator.create(
            "Individual",
            array.array,
            typecode="i",
            fitness=creator.FitnessMin,
        )

    toolbox = base.Toolbox()

    toolbox.register("attr_int", random.randint, int_min, int_max)

    toolbox.register(
        "individual",
        tools.initRepeat,
        creator.Individual,
        toolbox.attr_int,
        n=chromosome_length,
    )

    toolbox.register(
        "population",
        tools.initRepeat,
        list,
        toolbox.individual,
    )

    # Better for repeated integer chromosomes
    toolbox.register("mate", tools.cxTwoPoint)

    toolbox.register(
        "mutate",
        tools.mutUniformInt,
        low=int_min,
        up=int_max,
        indpb=0.1,
    )

    # Better selection pressure than selBest inside eaSimple
    toolbox.register("select", tools.selTournament, tournsize=3)

    toolbox.register("evaluate", agent.evaluate_chromosome)

    return toolbox


def build_stats():
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    return stats


def initialize_ga(agent):
    '''
    First step in the genetic process. Agent gets his own toolbox
    '''
    agent.toolbox = build_toolbox(
        agent=agent,
        chromosome_length=agent.N,
        int_min=agent.INT_MIN,
        int_max=agent.INT_MAX,
    )
    agent.stats = build_stats()
    agent.population = agent.toolbox.population(agent.POPULATION_SIZE)
    agent.hall_of_fame = tools.HallOfFame(1)
    agent.ga_initialized = True


def step_generation(agent):
    """
    Advance the GA by one generation.
    """
    algorithms.eaSimple(
        agent.population,
        agent.toolbox,
        agent.CXPB,
        agent.MUTPB,
        1,
        halloffame=agent.hall_of_fame,
        verbose=False,
        stats=agent.stats,
    )
    costs = [ind.fitness.values[0] for ind in agent.population]

    print("generation min cost:", min(costs))
    print("generation max cost:", max(costs))
    print("hall of fame cost:", agent.hall_of_fame[0].fitness.values[0])

    best_individual = agent.hall_of_fame[0]
    best_cost = agent.hall_of_fame[0].fitness.values[0]

    print("Best Individual:", list(best_individual))
    print("Best stored cost:", best_cost)

    return best_individual, best_cost