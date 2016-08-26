import h5pyd as h5py
from numpy import dtype, all

def visit_item(name):
    print('visit:', name)
    return None

def find_g1_2(name):
    print('visit:', name)
    if name.endswith('g1.2'):
        return True  # stop iteration


def visit_item_obj(name, obj):
    print('visit:', name, obj.id.id)
    return None

def test_version():
    assert h5py.version.version == '0.0.1'

def keys(g2):
    return [key for key in g2]

def test_network():
    f = h5py.File('tall.data.hdfgroup.org', 'r', endpoint='https://data.hdfgroup.org:7258')
    assert f.filename == 'tall.data.hdfgroup.org'
    assert f.name == '/'
    assert f.id.id == '4af80138-3e8a-11e6-a48f-0242ac110003'

    g2 = f['g2']

    assert g2.id.id != f.id.id
    assert g2.id.id == '4af955c4-3e8a-11e6-a48f-0242ac110003'
    assert g2.name == '/g2'
    assert len(g2) == 2

    assert keys(g2) == ['dset2.1', 'dset2.2']

    assert ('xyz' in g2) == False
    assert ('dset2.1' in g2) == True

    dset21 = g2['dset2.1']
    assert dset21.id.id == '4af97dd8-3e8a-11e6-a48f-0242ac110003'
    assert dset21.name == '/g2/dset2.1'
    assert dset21.shape == (10,)
    assert dset21.dtype == dtype('>f4') # four numpy fields?

    dset111 = f['/g1/g1.1/dset1.1.1']
    assert dset111.id.id == '4af8bc72-3e8a-11e6-a48f-0242ac110003'
    assert dset111.name == '/g1/g1.1/dset1.1.1'
    assert dset111.shape == (10, 10)
    assert dset111.dtype == dtype('>i4')
    assert len(dset111) == 10


    attr1 = dset111.attrs['attr1']
    mockattr1 = [ 49, 115, 116,  32,  97, 116, 116, 114, 105,  98, 117, 116, 101, 32, 111, 102,  32, 100, 115, 101, 116,  49,  46,  49,  46,  49,   0 ]
    assert (attr1 == mockattr1).all()
    assert len(dset111.attrs) == 2
    #  assert type(dset111.attrs.keys()) is KeysView
    assert keys(dset111.attrs) == ['attr1', 'attr2']

    for attr in dset111.attrs:
        assert attr == None

    #  print('visit...')
    #  f.visit(visit_item)

    #  print('visititems...')
    #  f.visititems(visit_item_obj)

    #  print('search g1.2:')
    #  f.visit(find_g1_2)
