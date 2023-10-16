from mlp_sdk.abstract import Task
from mlp_sdk.types import TextsCollection
from mlp_sdk.hosting.host import host_mlp_cloud
from mlp_sdk.transport.MlpServiceSDK import MlpServiceSDK
from mlp_sdk.transport.MlpClientSDK import MlpClientSDK
from pydantic import BaseModel
from typing import List, Any
from deap import base, creator, tools, algorithms
import numpy as np
import random
import re
import io


def mainContainer():
    ACCOUNT = "1234909"
    MODEL = "platform-vectorizer-ru-test"

    sdk = MlpClientSDK()
    sdk.init()
    req = TextsCollection(texts=["Hello"])
    res = sdk.predict(account=ACCOUNT, model=MODEL, data=req.json())
    print(res)
    sdk.shutdown()
    return res

    # def generate_random_coefficients(coefficients, variation_percentage=50):
    #     """
    #     Варьирует существующие коэффициенты случайным образом в пределах заданного процента.
    #
    #     Args:
    #         coefficients (list): Список существующих коэффициентов.
    #         variation_percentage (int): Процент вариации (максимальная амплитуда изменений).
    #
    #     Returns:
    #         list: Список новых коэффициентов с учетом вариации.
    #     """
    #     new_coefficients = [
    #         random.uniform(coeff - (coeff * variation_percentage / 100), coeff + (coeff * variation_percentage / 100))
    #         for coeff in coefficients
    #     ]
    #
    #     return new_coefficients
    #
    # def generate_random_system():
    #     """1) реализовать определение границ внутри этой системы
    #     2) добавить аргумент,который определяет что линза последняя, для нее не будет
    #     генирироваться толщина эта функция будет вызываться внутри фунции создающую  модель"""
    #     system = []
    #     t_1 = random.uniform(0.6, 1.8)
    #     k_1 = random.uniform(0.001, 1.0)
    #
    #     air_t_1 = random.uniform(0.7, 1.3)
    #
    #     t_2 = random.uniform(1, 0.5)
    #     k_2 = random.uniform(0.001, 1.0)
    #
    #     air_t_3 = random.uniform(0.7, 1.3)
    #
    #     t_3 = random.uniform(0.35, 1.2)
    #     k_3 = random.uniform(0.001, 1.0)
    #
    #     air_t_2 = random.uniform(0.35, 1)
    #
    #     system.extend([t_1, k_1, air_t_1, t_2, k_2, air_t_2])
    #     system.extend(generate_random_coefficients(
    #         [0., 0., -1.895e-2, 2.426e-2, -5.123e-2, 8.371e-4, 7.850e-3, 4.091e-3, -7.732e-3, -4.265e-3]))
    #     system.extend(generate_random_coefficients(
    #         [0., 0., -4.966e-3, -1.434e-2, -6.139e-3, -9.284e-5, 6.438e-3, -5.72e-3, -2.385e-2, 1.108e-2]))
    #     system.extend(generate_random_coefficients(
    #         [0., 0., -4.388e-2, -2.555e-2, 5.16e-2, -4.307e-2, -2.831e-2, 3.162e-2, 4.630e-2, -4.877e-2]))
    #     system.extend(generate_random_coefficients(
    #         [0., 0., -1.131e-1, -7.863e-2, 1.094e-1, 6.228e-3, -2.216e-2, -5.89e-3, 4.123e-3, 1.041e-3]))
    #     system.extend(generate_random_coefficients(
    #         [0., 0., -7.876e-2, 7.02e-2, 1.575e-3, -9.958e-3, -7.322e-3, 6.914e-4, 2.54e-3, -7.65e-4]))
    #     system.extend([air_t_3, t_3, k_3])
    #     return system
    #
    # def custom_mutate(individual, mu, sigma, indpb):
    #     for i in range(len(individual)):
    #         # Первый и третий параметры оставляем без мутации
    #         if i not in [0, 1, 2, 3, 4, 5, 6, 36, 37, 38]:
    #             individual[i] += random.gauss(mu, sigma) if random.random() < indpb else 0.0
    #     return individual,
    #
    # # Creating obgects
    # creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    # creator.create("Individual", list, fitness=creator.FitnessMin)
    #
    # toolbox = base.Toolbox()
    # toolbox.register("attribute", generate_random_system)
    # toolbox.register("individual", tools.initIterate, creator.Individual,
    #                  toolbox.attribute)
    # toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    #
    # # Operators
    # toolbox.register("mate", tools.cxOnePoint)
    # toolbox.register("mutate", custom_mutate, mu=0, sigma=1, indpb=0.1)
    # toolbox.register("select", tools.selTournament, tournsize=3)
    # toolbox.register("evaluate", evaluate_system)
    #
    # def main():
    #     CXPB, MUTPB, NGEN = 0.5, 0.2, 40
    #     population = toolbox.population(n=32)
    #     population, logbook = algorithms.eaSimple(population, toolbox,
    #                                               cxpb=CXPB,
    #                                               mutpb=MUTPB,
    #                                               ngen=NGEN,
    #                                               verbose=True)
    #     stats = tools.Statistics(lambda ind: ind.fitness.values)
    #     return population, logbook
    #
    # population, logbook = main()
    # res = list(map(evaluate_system, population))
    # res_1 = [i[0] for i in res]


class PredictRequest(BaseModel):
    point:float

    def __int__(self, points):
        self.points = points


class PredictResponse(BaseModel):
    system: Any
    def __int__(self, system):
        self.system = system


class SimpleActionExample(Task):

    def __init__(self, config: BaseModel, service_sdk: MlpServiceSDK = None) -> None:
        super().__init__(config, service_sdk)

    def predict(self, data: PredictRequest, config: BaseModel) -> PredictResponse:
        system = mainContainer()
        return PredictResponse(system=system)


if __name__ == "__main__":
    host_mlp_cloud(SimpleActionExample, BaseModel())
