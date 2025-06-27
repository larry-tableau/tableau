import multiprocessing
import sys
import os

# Set multiprocessing start method before any other imports
if __name__ == '__main__':
    multiprocessing.set_start_method('spawn', force=True)
    
    # Set environment variables
    os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
    os.environ['MULTIPROCESSING_START_METHOD'] = 'spawn'
    
    # Now import and run TabPy
    from tabpy.tabpy import main
    main()
