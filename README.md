# py-artemis-monitor-agent
Python monitoring agent for Artemis

Case: when an artemis cluster is setted up with jdbc persistance and the database goes down the broker shutsdown with exit code 0 and remains down.
When server restarts, artemis broker gets down but the server stays up.

Consideration:
log messages are one way to identify the issue, but i think that an actual call to the broker would be better.
