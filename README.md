# pybus

Simple implementation of message multicasting using Service Bus subscriptions and topics

![logo](https://github.com/giventocode/pybus/raw/master/multicast.png)

This sample has two components: the sender (sender.py) and the receiver (receiver.py).

The sender is a simple web app that expects a POST request that includes the topic and the message to be delivered to the bus. The thought behind this approach is having the sender app live side by side (e.g., in a container) with the process requiring message multicasting, and thus decoupling the Service Bus semantics from the caller.

The receiver is a sample implementation of a subscription to a specific topic. Each instance represents a client receiving messages from a specific topic.


## Prerequisites

Install flask

```python

    pip install Flask

```

Azure Service Bus SDK

```python

    pip install azure-servicebus

```

## Getting Started

First you must create a namespace and obtain the credentials. Intructions here:

[Create a namespace and obtain credentials](https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-python-how-to-use-topics-subscriptions#create-a-namespace)


Then enter the information in the configuration file config.conf

```python

namespace = "<YOUR NAMESPACE>"
acc_name = "<YOUR ACCOUNT NAME>"
acc_key = "<YOUR ACCOUNT KEY>"


```

>Note: Both sender and receiver use this configuration file.

Via the portal you can create a subscription, by going to your namespace and select *Topics* under the *Entities* on the left navigation pane.

Once the subscription is created you can navigate to it and create one or more *Subscriptions*.

## Running the sample

Running the sender:

```python

python sender.py

``` 

>Note: The sender will be listening on the following URL: http://localhost:5000

For the sender you need to pass the topic and the subscription as parameters

```python

python receiver.py topic1 subscription1

``` 

Issue a multi-form POST request using curl:

```bash

curl -X POST -F X POST -F 'topic=topic1'  -F 'msg={"id":1,"name":"my message"}' http://localhost:5000

```