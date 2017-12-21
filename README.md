# DOI-generator

Generates a DOI based on Crockford's base32
http://www.crockford.com/wrmg/base32.html as suggested by M. Fenner's ["Cool DOIs" blog post](https://doi.org/10.5438/55e5-t5c0).

A typical DOI generated with this tool looks like so:


**10.24386/YK4G6A**

We have changed some details, however:

* Instead of basing the suffix on a randomly generated number, we base
  it on an internal ID. That results in a more effective generation of
  suffixes once the allocated range fills up and random generation
  would increasingly produce duplicates.

* It is possible to reverse the suffix to the internal ID to help with
  debugging if the need arises.

* The suffix has only 6 characters, including the check-character. If
  the calculated suffix has a shorter length, it is padded with zeros.

* The set of numbers from which the suffix is created is restricted in
  a way that will result in only alphanumeric check-characters.

* We enable splitting the total number of possible suffixes into
  several ranges which are identified by an offset to the internal
  ID. A possible application is to assign different suffix-ranges to
  different clients of an allocator, even though that seems a bit
  redundant, as different clients should have different prefixes.

----

## Details

We want a checksum symbol and the resulting suffix should have 6
characters (including checksum character).

We want to avoid checksums 32 to 36, so that only alphanumerical
characters are used.

Since 32^5 - 1 =  906876 * 37 + 19, this leaves us with

\#([0, 906875] X [0, 31] + [0, 19])
= 906876 * 32 + 20 = 29020052 different DOI-suffixes.

We suggest to split this DOI-suffix-space into 13 ranges, each of them
with room for 2e6 suffixes. OK, we waste 1.020052 mio suffixes that way.

Possible offsets are then 0, 2e6, 4e6, ... 26e6. The size of a range and
correspondingly the offsets can be changed by modifying the constant `RANGESIZE`.



