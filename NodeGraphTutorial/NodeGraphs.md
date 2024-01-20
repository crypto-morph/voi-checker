
# Node Graph Examples
or "Why is my Voi Participation Node acting funny?"

## How to look for patterns

The amazing site https://voi-node-info.boeieruurd.com/ shows node history over the last 7 days.

If you node is not working correctly - it's worth checking this site to see why.

Before we start - things to note:

* A new node can take upto 24 hours to turn up on the list
* If your node isn't on this list:
  - If it's Ubuntu based (ideally using https://d13.co/posts/set-up-voi-participation-node) then use the voi-checker https://github.com/crypto-morph/voi-checker to work out why. 
  - If the node is build via another method - or if the checker isn't helping - raise a request on #node-help in Discord. 

The Graphs:

## My node is working fine

![Node Spec Too Low](/NodeGraphTutorial/goodnode.png)
If you have a graph like this - don't worry - everything is fine.

We're looking at:

* Total score is near 10 - that's exceptional - anything above 5 gets rewards
* Voting score is 1 (that's the maximum)
* Network score is 0.944 (also close to maximum of 1)
* "Min" score is good too - the worst this node operated was better than the reward level

## Something's wrong 1) - My node is not keeping up

![Node Spec Too Low](/NodeGraphTutorial/nodespectoolow.png)

This graph shows a node that is not keeping up:

* Network score is okay - but Voting score is 0
* The machine is only connecting to the relays occasionally
* Likely the machine is not keeping up with blockchain
* Check node is at least the minimum spec?

## Something's wrong 2) - Network contention

![Network Contention?](/NodeGraphTutorial/networkcontention.png)

* Voting score is good, Network score isn't
* Looking at the graph - it looks like traffic is being shaped
* Check with your connection provider - are they throttling traffic?

## Something's wrong 3) - Machine rebooting?

![Machine Rebooting?](/NodeGraphTutorial/goodsetup-machinerebootsoccasionally.png)

* Stats look good - but there are 'zero events' in the graph
* In this case - the machine was running Windows and Windows Update was rebooting it over the week. 
* It can also be caused by a machine overheating

## Something's wrong 4) - Voting Issues

![Voting Issues?](/NodeGraphTutorial/goodnetwork-badvote.png)

* This machine has 'fallen off a cliff' voting-wise in the last few days
* Look for changes to the server - has something been installed? updated?