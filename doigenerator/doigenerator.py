# _*_ coding: utf-8 _*_
"""doigenerator

Generates a DOI based on Crockford's base32
(http://www.crockford.com/wrmg/base32.html).

Usage:
  doigenerator [-u] <prefix> <id> <offset>
  doigenerator -r <doi>
  doigenerator -h


Arguments:
  <prefix>    The DOI prefix assigned to your datacenter.
  <id>        An internal ID <2e6 (integer), usually a counter of minted DOIs.
  <offset>    Is added to the internal ID. Assign offsets 0, 2e6, 4e6, ... 26e6 to different data centers.
  <doi>       A DOI that was generated with doigenerator (not the URL - form).


Options:
  -u, --url       Return the DOI in URL-form, e.g. "https://doi.org/10.123/123456".
  -r, --reverse   Returns offset and internal ID belonging to <doi>.

"""
import base32_crockford as b32
import sys
from docopt import docopt

def generate_doi(prefix, intid, offset, url=False):
    """ Generates a DOI based on Crockford's base32
    http://www.crockford.com/wrmg/base32.html
    
    Args:
        prefix (str): DOI prefix
        intid (int): Internal ID, usually consecutive numbering.
                     Must be < 2e6.
        offset (int): Is added to the internal ID. Assign offsets
                      0, 2e6, 4e6, ... 26e6 to different data centers.
    Returns:
        A 6 character string suited as DOI (without prefix)

    We want a checksum symbol and the resulting suffix
    should have 6 characters (including checksum character).
    If the suffix has a shorter length, it is padded with zeros.
 
    We want to avoid checksums 32 to 36, so that only
    alphanumerical characters are used.

    Since 32**5 - 1 =  906876 * 37 + 19, this leaves us with
    #([0, 906875] X [0, 31] + [0, 19])
    = 906876 * 32 + 20 = 29020052 different DOIs.

    We suggest to split this DOI-suffix-space into 13 ranges, each of them
    with room for 2e6 suffixes. OK, we waste 1.020052 mio suffixes here.

    """
    MAXI = 29020051
    RANGESIZE = int(2e6)
    OFFSETS = range(0, MAXI - RANGESIZE + 2, RANGESIZE)

    intid = int(intid)
    offset = int(offset)
    ## Avoid overlapping ranges for different datacenters
    assert(0 <= intid and intid < RANGESIZE)
    ## Valid offsets to serve max. 13 offset-defined ranges (datacenters)
    ## with 2 mio DOIs each. If each datacenter has its own prefix,
    ## this is mostly aesthetics.
    assert(offset in OFFSETS)

    def intid2i(intid, offset):
        '''
        Calculates the integer which is suited to be converted to base32,
        so that the checksum chracter is alphanumeric.
        
        Args:
            intid (int): internal ID
            offset (int): Offset for data center
        Returns:
            An integer that can be converted to base32 (Crockford)

        '''
        intid += offset
        n = int(intid / 32.)
        c = intid - n * 32
        return 37 * n + c
    
    suffix = b32.encode(intid2i(intid, offset), checksum=True)
    padding = 6 - len(suffix)
    suffix = padding * '0' + suffix
    proxy = 'https://doi.org/' if url else ''
    return '{}{}/{}'.format(proxy, prefix, suffix)

def revert_doi(doi):
    '''
    Returns offset and internal ID belonging to a DOI that was generated
    with generate_doi().

    Args:
        doi (str): The DOI
    Returns:
        {"prefix" (str): the prefix, "offset" (int): the offset,
         "intid" (int): internal ID}

    '''
    prefix, encoded = doi.split('/')
    i = b32.decode(encoded, checksum=True)
    n = int(i / 37)
    c = i % 37
    intid = int(c + n * 32)
    batch = int(intid / 2e6)
    offset = int(batch * 2e6)
    intid = intid - offset
    return {'prefix': prefix, 'offset': offset, 'intid': intid}

def main():
    args = docopt(__doc__, argv=sys.argv[1:], help=True)
    if args['--reverse']:
        res = revert_doi(args['<doi>'])
        print('\nDOI: {}\nPrefix: {}\nOffset: {}\nIntID: {}\n'
              .format(args['<doi>'], res['prefix'],
                      res['offset'], res['intid']))
    else:
        doi = generate_doi(args['<prefix>'], args['<id>'],
                           int(float(args['<offset>'])),
                           url=args['--url'])
        print('\nPrefix: {}\nOffset: {}\nIntID: {}\nDOI: {}'
              .format(args['<prefix>'], args['<offset>'], args['<id>'], doi))

                      
                                              
        


                   
            

