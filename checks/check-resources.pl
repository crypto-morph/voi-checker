#!/usr/bin/perl
use Term::ANSIColor qw(:constants);

$highcpu = 80.0;
$highmem = 80.0;
$highhd = 95.0;

print "Checking machine resources... \n";
print "  CPU... ";
$cpu = `checks/check-cpu.sh`;
chomp($cpu);
if ($cpu < $highcpu)
{
  print GREEN "OK ($cpu\%)\n" . RESET;
}
else
{
  print RED "CPU is high ($cpu\%)\n" . RESET;
}	

print "  RAM... ";
$mem = `checks/check-mem.sh`;
chomp($mem);
if ($mem < $highcpu)
{
  print GREEN "OK ($mem\%)\n" . RESET;
}
else
{
  print RED "RAM usage is high ($mem\%)\n" . RESET;
}	

print "  HDD... ";
$hd = `checks/check-hdd.sh`;
chomp($hd);
chop($hd); # remove %
if ($hd < $highhd)
{
  print GREEN "OK ($hd\%)\n" . RESET;
}
else
{
  print RED "HD usage is high ($hd\%)\n" . RESET;
}	
