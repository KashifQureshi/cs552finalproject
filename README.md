This code uses port 6000 by default.  That port must be able to accept traffic in order for this program to work.
To test for link capacity, aServer.py must be started on one machine.  It will prompt you to ask if you are using a 
high bandwidth connection. All this does is increase the size of packets that are sent.  The reason for this is from 
testing, using packets that are too small results in flawed results on a link with high capacity.  Saying Yes when 
the link is expected to be low capacity seems to be fine but it takes a long time.  In the future, sending some 
initial probing packets to determine the throughput of the connection before testing for link capacity would be the 
ideal approach but for now it asks.

There are two client modules.  aClient.py runs from the command line.  It asks for an IP to connect to and if you
expect this to be a high bandwidth connection.  speedtestClient requires the use of the kivy API.  Installation 
instructions for various operating systems are available here: https://kivy.org/doc/stable/guide/basic.html#installation-of-the-kivy-environment
speedtestClient does not accept any user input so in order to use it you need to have the server running on a 
machine hosted on ilab1-4.  It also sets the smaller packet size so it is not suitable for testing the link capacity
when the result is expected to be high.

When testing with competing traffic, use iperf3 in UDP mode.  On the client side run iperf3 -s and on the server run
iperf3 -c [IP address of client] -u -b [bandwidth amount followed by m for megabits] -t [time duration].  Normal 
iperf seems to misbehave once you exceed ~20% of the link capacity in the bandwidth you set.  To ensure you are using
the correct IP on Cloudlab: https://gitlab.flux.utah.edu/emulab/emulab-devel/-/wikis/faq/Using%20the%20Testbed/Control%20Network
