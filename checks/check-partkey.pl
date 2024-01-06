#!/usr/bin/perl
use Term::ANSIColor qw(:constants);
local $/;

$warningblocks = 5000;
$testwarning = 0;
$testerror = 0;

print "Checking participation key... ";

open (PART, "goal account partkeyinfo | grep 'Effective last round'|");
$part = <PART>;
$part =~ /Effective last round:\s+(\d+)/;
$part = $1;

open (STATUS, "goal node status | grep 'Last committed block'|");
$status = <STATUS>;
$status =~ /Last committed block:\s+(\d+)/;
$status = $1;

if ($testwarning)
{
  $part = $status + $warningblocks - 1;
}
if ($testerror)
{
  $part = $status - 10;
}

$diff = $part - $status;
#print "status = $status, part = $part, diff = $diff, warningblocks = $warningblocks\n";

if ($diff > $warningblocks)
{ 
  print GREEN "OK - $diff blocks until your key stops working\n" . RESET;
} 
elsif ($diff > 0)
{
  print YELLOW "WARNING - $diff blocks until your key stops working\n" . RESET;
}
else
{
  print RED "ERROR - Your key expired $diff blocks ago\n" . RESET;
}
