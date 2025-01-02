# Hight Availability Project

This project intents to implement a HA custom solution, and test its fiseability.

The idea is to deploy several workers into different processes. The dispatcher should then activate them following the criteria explained later on.

## Workers

When a worker is instanced should register with the dispatcher. For this it should use a message "is someone there", that will also include the assigned weight. The dispatcher will answer with the id assigned to the worker. The weight will be used as priority for activation.

The worker will get activated by a message of the dispatcher containing its id (that will have to compare against its own) and the order "activate". It will answer informing it has been "activated".

Once a worker has been activated, it should send back responses at random intervals (less than 5 seconds) for 5 times, until it deactivates itself. This message will contain whether it will continue active or not, "active" or "non-active".

## The Dispatcher

In order to instanciate a worker, the dispatcher should receive the weight the worker took on and assign it an id. This id will be a hash with the time.

The dispatcher should keep a list with all the workers, their weight, the number of times they have been activated, when the last communication happened, and whether they are currently active.

The activation of workers should be decided on the basis of their weights, selecting the one that makes the distribution of activations closer to that of the weights. The dispatcher should only consider those workers that are not currently active.

The dispatcher will activate a worker every 2 seconds, if there are any non-active woker available.

In order to activate a worker, the dispatcher will send an activation message instruction "activate". The worker should answer informing that it has been activated, "worker activated".

When the dispatcher receives a response, it should print it citing the id of the worker, the time of the communication and the worker status (active/non-active).

## Implementation

In order to implement the requirements for the server, I will use a `ThreadingUDPServer` for the the discovery of the address of the server.

I will also use a second `ThreadingTCPServer`to handle the remaining of the communication.

The workers will implement two sockets, one for UDP and another for TCP. Through broadcast/UDP, they will find out the address of the server. Through TCP, they will carry the rest of the communication.
