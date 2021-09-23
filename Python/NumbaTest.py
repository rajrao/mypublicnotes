from numba import jit #pip3 install numba
from statistics import mean
import random
import timeit

def monte_carlo_pi_noOptimizations(nsamples):
    acc = 0
    for i in range(nsamples):
        x = random.random()
        y = random.random()
        if (x ** 2 + y ** 2) < 1.0:
            acc += 1
    return 4.0 * acc / nsamples

@jit(nopython=True) #use only @jit, if you dont want to be warned about nopython not being applied
def monte_carlo_pi(nsamples):
    acc = 0
    for i in range(nsamples):
        x = random.random()
        y = random.random()
        if (x ** 2 + y ** 2) < 1.0:
            acc += 1
    return 4.0 * acc / nsamples

#Warmup functions
monte_carlo_pi_noOptimizations(1)
monte_carlo_pi(1)

print ('Warmup completed, running tests...!')
iterations = [100,1000,10000,100000]
nonOptimizedRunTimes = [];
optimizedRunTimes = [];
for runCount in iterations:
  print (f'Num Iterations: {runCount}')
  cpu_time = timeit.timeit('monte_carlo_pi_noOptimizations(100)', number=runCount, setup="from __main__ import monte_carlo_pi_noOptimizations")
  print(f'\tUnOptimized Run Time: {cpu_time}')
  nonOptimizedRunTimes.append(cpu_time/runCount)

  cpu_time = timeit.timeit('monte_carlo_pi(100)', number=runCount, setup="from __main__ import monte_carlo_pi")
  print(f'\tOptimized Run Time: {cpu_time}')
  optimizedRunTimes.append(cpu_time/runCount)

print ('Tests complete!')

print(f'UnOptimized Run Time: {mean(nonOptimizedRunTimes):.10f}')
print(f'Optimized Run Time: {mean(optimizedRunTimes):.10f}')

print(f'Optimized is faster by a factor of: {round(mean(nonOptimizedRunTimes)/mean(optimizedRunTimes),1)}')
