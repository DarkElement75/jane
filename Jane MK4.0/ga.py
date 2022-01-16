"""
Genetic Algo testing on stock environment sims.

Modified from https://github.com/cai91/openAI-classic-control/blob/master/cartPole_openAI.py

to work on our StockEnvironment
"""
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from sim import StockEnvironment


# General libraries
import random
import numpy as np
import matplotlib.pyplot as plt

# Importing gym
import gym

# Neural network libraries
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Genetic algorithms libraries
from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import deap


week_data_dir = "jan_12_2022/week.npy"
data = np.load(week_data_dir)

# if __name__ == "__main__":
#     stock_n = data.shape[0]
#     market = []
#     for stock_i in tqdm(range(stock_n)):

# Function to roll parameters
def rollParams(uWs, top):
    '''This function takes in a list of unrolled weights (uWs) and a list with the number of neurons per layer in the following format:
    [input,first_hidden,second_hidden,output] and returns another list with the weights rolled ready to be input into a Keras model
    describing a two hidden layer neural network'''

    rWs = []
    s = 0

    for i in range(len(top) - 1):
        tWs = []
        for j in range(top[i]):
            tWs.append(uWs[s:s + top[i + 1]])
            s = s + top[i + 1]

        rWs.append(np.array(tWs))
        rWs.append(np.array(uWs[s:s + top[i + 1]]))
        s = s + top[i + 1]

    return rWs


# Fitness function
def cartPole(agent):
    R = 0
    env = gym.make('CartPole-v0')
    obs = env.reset()
    model.set_weights(rollParams(agent, [4, 10, 5, 1]))

    for t in range(200):

        action = model.predict_classes(np.array([obs]))[0][0]
        obs, reward, done, info = env.step(action)
        R += reward

        if done:
            return (R),
            break


env = StockEnvironment(data[0])
def cartStockPole(agent):
    obs, reward = env.start()
    model.set_weights(rollParams(agent, [5, 10, 5, 1]))

    while not env.done:

        #action = model.predict_classes(np.array([obs]))[0][0]
        action = model.predict_on_batch(np.array([obs]))[0][0]
        obs, reward = env.act(action)

    return reward

# Create neural network model
model = Sequential()
model.add(Dense(10, input_dim=5, activation='relu'))
model.add(Dense(5, activation='relu'))
#model.add(Dense(1, activation='sigmoid'))
model.add(Dense(units=1))

# Evolution settings

# Creator
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# Toolbox
toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, -1, 1)
# 111 = # of fully connected params = (n*m + m) for any src layer n nodes to dst layer m nodes
# because each node has bias
# 4*10 + 10, 10*5 + 5, 5*1 + 1 = 50 + 55 + 6 = 111

# So for cartStockPole it's 5*10 + 10, 10*5 + 5, 5*1 + 1 = 121
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, 121)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", cartStockPole)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0.0, sigma=0.2, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


def main():
    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)

    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    # Launch evolutionary algorithm
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.8, mutpb=0.2, ngen=10,
                                   stats=stats, halloffame=hof, verbose=True)
    print('\nBest: ')
    print(hof)
    return hof


for i in range(2,data.shape[0]):
    print(i)
    env = StockEnvironment(data[i])
    best = main()[0]
    env.env = env.validation
    print(f"Validation: {cartStockPole(best)}")
    env.env = env.test
    print(f"Test: {cartStockPole(best)}")

"""
# Comment out main(), add env.render() inside the loop of the fitness function and uncomment following code to see best agent in action.

# Best agent
ind=[0.8786142609531805, -0.24499985914455918, 0.19830243346525878, 3.6135458449894977, -0.8756389008884015, -0.17625509764705652, 0.8238902515818699, -3.719170121907547, 0.9533418343262616, 1.3606989742046416, -0.10552819110606862, 0.07883893044152994, -0.13225081006020262, -0.8220883053882172, -1.1935508495598426, 0.1470175841665257, -0.11277111439210363, 1.1600658200085057, -0.8290904449138293, 0.37794766375458866, -0.9547008797729267, 1.0371657486039811, -2.17475178534988, 0.16401709691765404, -1.7635558440239587, -0.6324829440715244, -0.15417730908589997, -0.043030426038392036, -0.32573478851676185, 0.7038825332136986, -1.5318441728003125, -0.41884866442994606, -1.3524357666645215, 0.603326845672879, -0.03779834162305759, 0.7432539768279451, 1.1397187839825786, 1.327158088904039, 0.4998306704987332, -0.9104966036409607, 0.3307351133959217, 1.1052651459158027, 0.13110896569556038, 0.4091353922638391, -0.29229473505337566, -0.44761791653031524, 0.9206234610641171, 0.15283487657256578, 1.1768812206242758, -0.2117086642917545, -0.16998368121715757, 0.10990165849772918, -0.9162034681979427, -0.3578489891800434, 0.014799919774310579, -1.6628373102560525, -0.5916954478186089, -1.4734229345643473, -0.9762941207234848, -0.5268528685429597, 1.9362480535809967, -0.059642452067269466, 2.14489198215534, -0.901627145725414, -1.5442330143128042, 0.23779181664595178, 0.6088838140794923, -0.281336966549756, -0.11419085183349717, -0.37614406673447387, -0.21241909745889445, 0.3181345462145525, 0.46829460835323367, -0.3985292689276118, -0.758736232983492, -0.4003734659314951, -0.14871248132826265, 0.032694482647512374, -0.37913765462036075, 0.2671840830695918, -0.3752513355088073, -1.0889279936348917, -0.5800897618280139, 1.1201400900508431, -0.8216854784938163, -0.25736069605183853, 0.3704669268086817, 0.42367422374548486, 0.5448200834780769, -0.13254027403837923, 0.414567344742819, 0.15529735087176094, 0.5460743730241069, -0.7959490785624537, -1.1729591807542195, 0.9924160371034438, -2.4801505279912885, -0.08216604767737523, 1.2036801936608237, -0.04953529297306664, -0.1576094365745388, 0.8559486824645739, -0.834284341650256, 1.707193321358777, 0.5392708474345845, -0.7808348619320679, -0.026440866545192947, 0.043084343629598065, 1.2209150563395077, 0.46783104436520323, -0.8629512011905451]

for i in range(10):
    cartPole(ind)
"""
#best = [0.2612465769176178, 0.5777424593068096, -0.3040976030486658, 0.09376253109737145, 0.971100400831485, 0.995809768995738, 1.8168211962914507, -0.008919377712811666, -0.19050476387365403, 1.174665272175784, -0.3537049937443939, 0.4063498755505669, 0.6460162587932037, 0.3314202307161558, 0.6719688736250289, 0.41212488981325823, -0.29552577975911803, 0.8618103075529756, -0.2206796477172795, -0.7023230104991396, -0.13600185053404296, -0.3183303295356867, -0.8469934492146363, 0.1296724545960288, -0.061948055636465604, -0.35646057914950124, 0.5462005089871373, 0.9113673858898484, 0.48401993740824567, -0.13133183725023398, 2.906553678320006, -1.7021392372900954, 0.10760956598925883, -0.6188963132759132, -0.137083884891179, -0.834303128534155, 0.016896698494281798, -0.02523688609518572, 0.0949772151912775, 1.1009756677536795, -0.6566223958640262, 0.10643615749818125, -0.7813595579385932, 0.025770706602743648, -0.33066445914740816, -0.01828625855744216, 0.008816300441571168, -0.5797680734155382, -0.09692589982098467, -0.7369443067737285, 0.34126700130798265, 0.1773840142931584, 1.0233896363586843, -0.2712720565456592, -0.6269604493361085, 0.031068158397318475, 0.004847469062880125, 0.06679724709433514, -0.0249674977424153, -0.4722206373012834, -0.40126001999287414, -0.31178898195029414, 0.7410690255924574, -0.3122487277145314, -0.6342449787203863, -0.2955157057423619, 0.28538343335805416, 0.7336955188443798, -0.23964206732402912, -0.6485422370444105, 0.17245221890769336, -0.213476032956643, -1.2822024076825662, 0.38626100829355764, -1.1541673049227137, 1.0335571199467029, 0.16313017287259735, 0.4948857949169862, 1.3149456759248184, -0.2298265472262951, 1.2424404412880325, -0.8259932074522238, -0.07800414021844829, 2.131948819704336, -0.16853072033210492, 0.09812398533279618, -0.2548756024110733, -1.0243037746618178, 0.7672756536861162, 1.167438421600317, -0.43312822932451855, 1.762114673966505, -1.5225305426494529, 0.0680017366762783, 0.9699618239955263, 1.2652077508388306, -0.4328916956078177, 0.4503375762101509, -0.480918253702298, 0.15296134712862014, 0.2401563057278116, 0.6441720937373154, -0.2982693656005607, -0.41250934130270733, -1.0198836410616208, -0.33966602460266465, -0.03616423813646753, -0.2124879271875061, -0.994601951699943, 0.02786332297997124, 0.055798617696758146, -0.35815401686704174, 1.506722799301874, 1.543376009236205, -0.5832413286970719, 0.37251272036881994, -0.9408255582286296, 0.7340818772083179, 0.7826173170268067, 1.1536675657014626, 0.4970262429353345]
#best2 = [-0.5786745403471651, 1.8513025910727008, -0.29173215955277587, -1.1021591838600873, -0.21256645661512508, -1.8437698386422632, -0.2051122349647139, -0.36459161565289633, -1.5715907454411153, 1.9233776539601142, -0.9743700409061389, 0.3043257643691919, -0.17656881275643066, -0.6459226015429841, 1.5198438706007935, -0.905606339712152, 0.16930101667005376, -1.5275254530048579, -0.15481469106861467, -0.572911863403367, -0.521584996364037, -0.8168527401909267, 0.1036611418219528, 0.06971404933289663, -0.5168398290475793, 0.4017455190860057, -1.3311734764352214, 0.23708441915583028, 2.1331257410400837, 0.18702393830232963, 0.2945913438826133, 0.5245526939341967, 0.4569696387228173, 0.21747040347580124, 0.5762246151546095, -0.37810182884670784, -1.016903938704264, 0.09720462338746357, 0.9497919041659455, 0.0775422767815227, 0.3945712565326957, -0.3637009858886058, -0.5965755590936817, 0.21838848408676198, 0.043084003926784346, -0.6041831389341771, 0.0791406444296491, -0.7099108865812429, -0.27934956850102644, 1.3084736566503896, -0.6837574217165767, 1.0634294732733502, -0.7049526856213852, -1.0004189173717786, 1.0822611292152198, 0.9210679561538135, -1.2192847059258984, -0.7638209872573163, -0.050497769628908354, -1.206933574060695, 0.6361470920152468, -0.21662412967708547, 0.45113785122491484, -0.7067949069603471, -0.6430490712402364, -1.0585673061875818, 0.9867513860256764, -1.264776905950285, 0.17467145158126438, 0.8384265560310911, -0.9428189967357996, 0.5880536286062402, -0.13338190059544325, -1.2019414938116446, 0.8055855227163998, 0.18579680375840218, 0.31824759897193866, -0.9269920662117186, -1.2253127286862104, -0.11433871157197506, 0.04965806747485724, 0.501711058217891, 0.4829291257173254, 0.10830928074206946, 0.9194293081096788, 0.4819789750139086, -0.3426825391353143, 1.081291809913528, -0.28279152949218445, 1.7419663459564168, -0.05589045379028093, -0.2342397599456375, -0.5092163061229604, -0.7035558760267313, -2.8134383138685797, 0.2833834653692791, -0.5846367164636745, 0.3671099133929923, 0.47807647119375496, 0.6210049084720398, 0.773797181863435, -0.4377231533469488, -0.16880537964730835, 0.547470747968259, -0.2579099509007201, -0.35889938720874714, -0.5743817637153678, -0.20252684119879746, -0.007396500916398566, 0.2929690153773551, -0.0677628770203429, 0.7377916492770806, 0.7681555156178801, -0.28744381039343675, 0.6753251530923217, 0.03898531323341023, -0.0831134881564885, 0.1991828004898985, 0.3458286308003544, 0.7586712387773867, -1.6353755820625877]
print(cartStockPole(best2))