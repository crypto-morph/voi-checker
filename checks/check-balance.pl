#!/usr/bin/perl
use Term::ANSIColor qw(:constants);

print "Checking balance... ";

open (ACCOUNT, "goal account dump -a $ENV{addr}|");
local $/;
$account = <ACCOUNT>;
$account =~ /"algo": (\d+)/;
$balance = $1;
if ($balance >= 550000000)
{ 
  print GREEN "OK - " . $balance / 1000000 .  " voi is enough\n" . RESET;
} 
else 
{
  print RED $balance / 1000000 . " is NOT enough\n" . RESET;
}
