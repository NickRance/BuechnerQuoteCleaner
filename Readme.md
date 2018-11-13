# Controversy Flagger

## Problem
Given a dataset of quotes from a person create software that identifies quotes that may be controversial

## Solution
Use a "Blacklist" to filter out quotes from the quote dataset that are likely to contain controversial words.
The quotes that could be controversial are placed in a (flagged file)[./flagged.csv]
The quotes that don't contain any blacklisted words are placed in a (clean file)[./clean.csv]