
Azure Service Bus - Portal based behavior of Topic and Subscription statuses.
1. When topic is enabled and subscription is enabled (normal behavior), messages sent to the topic will be delivered to the consumer and any subscription clients will be able to pick up the message.

2. Topic is disabled (not very useful).
	Disabling of the topic auto disables the subscriptions.
	Messages cant be sent to the topic.
	Messages cant be picked up clients of subscriptions.
	
	Code behavior:
	1. publishers will throw an exception that messaging entity is disabled on attempting to send a message. In effect, this topic is shut down.
	2. subscription clients will be able to connect to their topic without a catastrophic failure.
		consumers will continue running if the disabling of the topic happens during run-time (but internally, if you wanted, you can detect that the topic is disabled and perform specialized processing).

		
3. Active Topic, disabled subscription (very useful):
	Messages can be published to the topic.
	Messages will be delivered to all subscriptions (regardless of the subscription state being active or disabled).
	Subscription clients will be able to pick up the messages as soon as the subscription is made active again.
	
	Code behavior:
	1. Messages sent to the topic will continue to be delivered to the subscription.
	2. When the disabled subscription is made active, it will automatically begin delivering messages to any connected consumers.
	3. Subscription clients on disabled subscriptions will continue running. Again, the code will let you detect this and handle it appropriately if you wanted.
	This I consider useful, as you can turn off the consumer of a system that might be down, being overwhelmed by messages or being updated or you just dont want messages to be processed to protect the state of a system (eg: bug investigation). After the issue is cleared, you can re-enable the subscription and clients will begin processing messages.
	
Azure Service Bus - Portal based behavior Queue status:
	Supports only 2 states in the portal: active and disabled.
	Active state: sends are successful and message is delivered to the queue and subsequently to clients.
	Disable state: sends are unsuccessful. clients can connect but will not receive messages until queue is made active.

Note: 
	The client behavior is based on Microsoft.Azure.ServiceBus, .net standard library. If you use a different library or change the default options, the client behavior may in-fact cause it to fail catastrophically.
