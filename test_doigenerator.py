from doigenerator import generate_doi, revert_doi
import random
import pytest

def test_generate_doi():
    
    prefix = "10.24386"
    intids = ([random.randint(0, 2e6-1) for x in range(0, 101)]
              + [0, 65.0, 2e6-1])
    offsets = [0, 18e6, 26e6]
    for intid in intids:
        for offset in offsets:
            doi = generate_doi(prefix, intid, offset, url=False)
            reverse = revert_doi(doi)
            assert(reverse['prefix'] == prefix)
            assert(reverse['offset'] == offset)
            assert(reverse['intid'] == intid)
    
    with pytest.raises(AssertionError):
        generate_doi(prefix, 2e6, 20e6)
    with pytest.raises(AssertionError):
        generate_doi(prefix, 30, 21e6)
        
    print(generate_doi(prefix, 33, 0))

    assert(generate_doi(prefix, 0, 0) == 'https://doi.org/{}/000000'
           .format(prefix))
        
