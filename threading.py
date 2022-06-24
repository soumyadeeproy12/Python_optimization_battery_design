import threaded
import time 

##Here to add to the main function 

## Import two functions here 


## Import all the libraries 

def thread():
    thread1 = threaded.Thread(
    target=simulation_module, args=("thread1", '_INPUT_YOUR_VARIABLES'))
    time.wait(4)
    thread2 = threaded.Thread(
        target=optimization_module, args=("thread2", '_INPUT_YOUR_VARIABLES'))

    thread1.start()
    time.wait(4)
    thread2.start()

    thread1.join()
    thread2.join()



    