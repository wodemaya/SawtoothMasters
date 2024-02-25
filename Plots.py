from matplotlib import pyplot as plt



plt.figure(figsize=(10, 8))

plt.rc('axes', labelsize=20)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=15)    # fontsize of the tick labels
plt.rc('ytick', labelsize=15)    # fontsize of the tick labels
plt.rc('font', size=15)          # controls default text sizes

plt.xlabel("Number of blocks mined")
plt.ylabel("Total computational time(ms)")
plt.title("Number of P2P CS nodes: 5, Number of transactions in each block: 60")

times = [7.478, 14.705, 21.269, 31.472, 42.731]
blks = [10, 20, 30, 40, 50]
wid = 5
for index, _ in enumerate(blks):
    plt.text(blks[index] - wid/3, times[index] + 0.5,
             times[index])


plt.bar(blks, times, width=wid, color='#91ACE0')
plt.show()

##########



plt.figure(figsize=(10, 8))

plt.rc('axes', labelsize=20)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=15)    # fontsize of the tick labels
plt.rc('ytick', labelsize=15)    # fontsize of the tick labels
plt.rc('font', size=15)          # controls default text sizes

plt.xlabel("Number of transactions per block")
plt.ylabel("Total computational time(ms)")
plt.title("Number of P2P CS nodes: 5, Number of blocks mined: 30")

times = [9.608, 13.475, 19.177, 23.634, 28.849]
txs = [20, 40, 60, 80, 100]
wid = 10
for index, _ in enumerate(txs):
    plt.text(txs[index] - wid/3, times[index] + 0.5,
             times[index])


plt.bar(txs, times, width=wid, color='#A9E9E4')
plt.show()
