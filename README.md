# Hight Availability Project

This project intents to implement a HA custom solution, and test its fiseability.

The idea is to deploy several workers into different processes. The dispatcher should then activate them following the criteria explained later on.

## Workers

When a worker is instanced should register with the dispatcher. For this it should use a message "is someone there", that will also include the assigned weight. The dispatcher will answer with the id assigned to the worker. The weight will be used as priority for activation.

The worker will get activated by a message of the dispatcher containing its id (that will have to compare against its own) and the order "activate".

Once a worker has been activated, it should go to sleep for a random period of time between 1 and 5 seconds. Once the worker is free again, it should communicate the dispatcher with a message i_am_available.

The worker will use heartbeats to check the communication with the dispatcher. If the worker doesn't obtain an answer from the dispatcher five times in a row, it will shut down itself.

## The Dispatcher

In order to instanciate a worker, the dispatcher should receive the weight the worker took on and assign it an id. This id will be a hash generated from the time.

The dispatcher should keep a list with all the workers, their weight, the number of times they have been activated, when the last communication happened, and whether they are currently busy.

The activation of workers should be decided on the basis of their weights, selecting the one that makes the distribution of activations closer to that of the weights. The dispatcher should only consider those workers that are not currently busy.

The dispatcher will activate a new worker every 2 seconds, if there are any worker available.

In order to activate a worker, the dispatcher will send an activation message instruction "activate".

The dispatcher will remove the worker for whom it hasn't received a heartbeat for 45 seconds strait.
