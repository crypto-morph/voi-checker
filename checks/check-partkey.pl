#!/usr/bin/perl
use Term::ANSIColor qw(:constants);
local $/;

print "Checking participation key... ";

open (PART, "goal account partkeyinfo | grep 'Effective last round'|");
$part = <PART>;
$part =~ /Effective last round:\s+(\d+)/;
$part = $1;

open (STATUS, "goal node status | grep 'Last committed block'|");
$status = <STATUS>;
$status =~ /Last committed block:\s+(\d+)/;
$status = $1;

$diff = $part - $status;

if ($diff > 0)
{ 
  print GREEN "OK - $diff blocks until your key stops working\n" . RESET;
} 
else 
{
  print RED "ERROR - Your key expired $diff blocks ago" . RESET;
}
