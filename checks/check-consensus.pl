#!/usr/bin/perl
use Term::ANSIColor qw(:constants);

print "Checking consensus... \n";
$addr = $ENV{addr};

open (CONSENSUS, "curl -s https://analytics.testnet.voi.nodly.io/v0/consensus/accounts/all|");
while ($consensus = <CONSENSUS>)
{
  
  #if ($consensus =~ /\s+\[\"(\S+)\"\,\s+\"(\d+)\"\,\s+\"(\d+)\"\,\s+\"(\d+)\"\,\s+\"(\d+)\"\,\s+(\d+)\,\s+\"(\d+)\"\,\s+\"([^,]+)\"\,\s+([^,]+),\s+([^,]+),\s+(.+)\]\,/)
  if ($consensus =~ /\s+\[\"$addr\"\,\s+\"(\d+)\"\,\s+\"(\d+)\"\,\s+\"(\d+)\"\,\s+\"(\d+)\"\,\s+(\d+)\,\s+\"(\d+)\"\,\s+\"([^,]+)\"\,\s+([^,]+),\s+([^,]+),\s+(.+)\]\,/)
  {

    $softVotes = $addr;
    $softTokens = $2;
    $certVotes = $3;
    $certTokens = $4;
    $q05Latency = $5;
    $proposals = $6;
    $lastSoftVote = $7;
    $lastCertVote = $8;
    $lastProposal = $9;
    $avgPctOnTime = $10;

    #print "    softVotes: $softVotes\n";
    #print "    softTokens: $softTokens\n";
    #print "    certVotes:  $certVotes\n";
    #print "    certTokens: $certTokens\n";
    #print "    q05Latency: $q05Latency\n";
    #print "    proposals: $proposals\n";
    #print "    lastSoftVote: $lastSoftVote\n";
    #print "    lastCertVote: $lastCertVote\n";
    #print "    lastProposal: $lastProposal\n";
    #print "    avgPctOnTime: $avgPctOnTime\n";
  }
}

if ($avgPctOnTime > 80)
{ 
  print GREEN "    OK - good average percentage on time - $avgPctOnTime\%\n" . RESET;
} 
else 
{
  print RED "    low average percentage on time - $avgPctOnTime\%\n"  . RESET;
}
