import honors
import matplotlib.pyplot as plt

mode = "Scatter"
mode2 = "Save"
if mode == "Scatter":
    n = 25
if mode == "Bar":
    n = 1000

if mode:
    avg1, results1 = honors.run_avg1(n)
    avg2, results2 = honors.run_avg2(n)
    avg3, results3 = honors.run_avg3(n)
    avg4, results4 = honors.run_avg4(n)
    x = [(i+1) for i in range(n)]
    
if mode == "Scatter":
    plt.plot(x, results1, 'ro', label = 'Algorithm 1')
    plt.plot(x, results2, 'bo', label = 'Algorithm 2')
    plt.plot(x, results3, 'go', label = 'Algorithm 3')
    plt.title("After {} Rounds of Are You the One?...".format(n))
    plt.plot(x, results4, 'yo')
    plt.plot(x, [avg1 for i in range(n)], 'r')
    plt.plot(x, [avg2 for i in range(n)], 'b')
    plt.plot(x, [avg3 for i in range(n)], 'g')
    plt.plot(x, [avg4 for i in range(n)], 'y')
    plt.ylabel("Number of Weeks")
    plt.xlabel("Trial #")
    plt.axis([0, n+(n//10), 0, max(results1)+10])
    plt.legend()
    if mode2 == "Save":
        plt.savefig("Scatter")
    elif mode2 == "Show":
        plt.show()
    
if mode == "Bar":
    plt.bar(1, avg1, label = 'Algorithm 1')
    plt.bar(2, avg2, label = 'Algorithm 2')
    plt.bar(3, avg3, label = 'Algorithm 3')
    plt.bar(4, avg4, label = 'Algorithm 4')
    plt.title("After {} Rounds of Are You the One?....".format(n))
    plt.ylabel("Average Number of Weeks")
    plt.legend()
    if mode2 == "Show":
        plt.show()
    if mode2 == "Save":
        plt.savefig("Bar")