# Hight Availability Project

This project intents to implement a HA custom solution, and test its fiseability.

The idea is to deploy several workers into different threads. The dispatcher should then activate them following the criteria explained later on.

## Workers

When a worker is instanced should register with the dispatcher. For this it should use a broadcast message "is someone there", together with its ip address. The dispatcher will receive it, and he will answer with the id assigned to the worker and the ip address of the dispatcher. The Id will be used for its communications with the dispatcher. It should regiter with the dispatcher, communicating the weight it assigns itself. The weight will be used as a priority for activation.

All the communication with the dispatcher, will contain its id and the information to be exchanged.

The worker should expect to receive a "status check", that will answer with "activated" or "not activated".

The worker will get activated by a message of the dispatcher containing its id (that will have to compare against its own) and the order "activate". It will answer informing it has been "activated".

Once a worker has been activated, it should send back responses at random intervals (less than 5 seconds) for 5 times, until it deactivates itself. This message will contain whether it will continue active or not, "activated" or "not activated".

A worker can terminate its own thread with a likelihood of 0.8.

## The Dispatcher

In order to instanciate a worker, the dispatcher should assign an id, and receive the weight the worker took on.

The dispatcher should keep a list with all the workers, their weight, the number of times they has been activated until that momment, when the last communication happened the number of answers received from last activation and whether they are available.

The activation of workers should be decided on the basis of their weights, selecting the one that makes the distribution of activations closer to that of the weights. When the dispatcher activates a worker, it should mark it as not available until it deactivates.

All communication with the worker should contain the "id" of the target worker.

The dispatcher will activate a worker every 2 seconds if less than 5 of them are active.

In order to activate a worker, the dispatcher should first check the status by sending a "status check" instruction. If the actual status is "not activated", it will send an activation message instruction "activate". The worker should answer informing that it has been activated, "worker activated". Then the dispatcher should mark the worker as activated. If the received status is "activated" it will move onto the next best candidate.

When the dispatcher receives a response, it should print it received a response citing the id of the worker, the number of answers received from that worker from its last activation, and update the time of the last communication and the number of communications from the last activation.

Once the dispatcher receives a notice that a worker has deactivated, it will update the list of workers, making it available. It should also zero the number of communications from the last activation, and make -1 the time from the last communication.

If 5 seconds pass without any communication, the dispatcher should consider that the worker was terminated and remove it from the list. The dispatcher should inform when it considers that a worker has terminated.

## Implementation

In order to implement the requirements for the serve, I will use a `ThreadingUDPServer` for the worker registration, for the discovery and update of the list of registered workers. The use of threads allow me to interact with the list in the main thread.

I will also use a `ForkingTCPServer`to manage the remaining of the communication, as it will deal with issues only related to each worker (i.e. the alive ping or its responses).

The workers will implement two sockets, one for UDP and another for TCP. Through broadcast/UDP, they will find out the address of the server,and receive the address of the socket assigned to them. Through TCP, they will carry the rest of the communication.