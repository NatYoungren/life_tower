# Nat Youngren
# June 9, 2023

import time
import numpy as np

class DebugTimer:
    def __init__(self, printall=False):
        self.printall = printall # If true, print every lap.
        
        self.time_dict = {} # Stores the last time for each name.
        self.lap_times = {} # Stores the lap times for each name.
        
        self.set_time('init')


    def get_time(self, name, tare=True, reset=False):
        """Return stored time for a given name, optionally taring and/or resetting the timer.

        Args:
            name (str): Dict key of the time to return.
            tare (bool, optional): If True, return time since last stored time. Defaults to True.
            reset (bool, optional): If True, reset stored time to the current time. Defaults to False.

        Returns:
            float: Either the stored time, or the time since the stored time (if tare=True).
        """
        old_time = self.time_dict[name]
        current_time = time.time()
        
        if reset:
            self.time_dict[name] = current_time
            
        if tare:
            old_time = current_time - old_time
            
        return old_time


    def set_time(self, name, set_last=True):
        """Set the stored time for a given name.

        Args:
            name (str): Dict key of the time to set.
            set_last (bool, optional): If True, reset the value of 'last' in the dict, used for lapping. Defaults to True.
        """
        t = time.time()
        self.time_dict[name] = t
        if set_last:
            self.time_dict['last'] = t
    
        
    def lap(self, name, since='last', reset=True, printout=False):
        """Record a lap time for a given name.

        Args:
            name (str): Dict key of the lap to record.
            since (str, optional): Dict key referencing the 'start' of the lap. Defaults to 'last'.
            reset (bool, optional): If True, reset since to current time. Defaults to True.
            printout (bool, optional): If True, provide a printout (can be overriden to True by self.printall at init). Defaults to False.
        """
        if since is None:
            since = name
        
        new_time = self.get_time(since, reset=True)
        
        if printout or self.printall:
            print(f'{name}: {new_time}')
        
        self.lap_times[name] = self.lap_times.get(name, []) + [new_time]
        
        if reset:
            self.set_time(since)
    
    
    def print_laps(self):
        """Print lap times/stats for each stored lap name.
        """
        init_time = self.get_time('init', tare=False)
        last_time = self.get_time('last', tare=False)
        total_time = last_time - init_time
        
        print('\n ## ## LAP TIMES ## ## ')
        print(f'Total time: {total_time:.6f} sec.')
        for name in self.lap_times:
            laptimes = self.lap_times[name]
            lapcount = len(laptimes)
            lapsum = sum(laptimes)
            print(f'\n{name}: {lapcount} laps, {lapsum:.6f} total time')
            print(f'> Percent of total time: {(lapsum/total_time)*100:.2f}%')
            print(f' > Average time per lap: {lapsum/lapcount:.6f}')
            print(f'  > Highest lap time: {max(laptimes):.6f}, lowest lap time: {min(laptimes):.6f}, median lap time: {np.median(laptimes):.6f}')
