#!/usr/local/bin/perl

while(<>) {
    chomp;
    s/\<[^<>]*\>//g;           # eliminate markup
    tr/[A-Z]/[a-z]/;           # downcase

    s/([a-z]+|[^a-z]+)/\1 /g;  # separate letter strings from other types of sequences

    s/[^a-z0-9\$\% ]//g;       # delete anything not a letter, digit, $, or %

    s/[0-9]+/\#/g;             # map numerical strings to #

    s/\s+/ /g;                 # these three lines clean up white space (so it's always exactly one space between words, no newlines
    s/^\s+//;
    s/\s+$/ /;


    print if(m/\S/);           # print what's left
}
print "\n"; # final newline, so whole doc is on one line that ends in newline
