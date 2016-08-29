import h5pyd as h5py
from numpy import dtype


visitedItems = []
foundItems = []
visitedItemsDict = {}


def visit_item(name):
    visitedItems.append(name)
    return None


def find_g1_2(name):
    print('visit:', name)
    foundItems.append(name)
    if name == '/g2/dset2.1':
        return True  # any defined return value stops iteration
    return None


def visit_item_obj(name, obj):
    visitedItemsDict[name] = obj.id.id
    return None


def test_version():
    assert h5py.version.version == '0.0.1'


def keys(g2):
    return [key for key in g2]


def test_network():
    f = h5py.File(
        'tall.data.hdfgroup.org',
        'r',
        endpoint='https://data.hdfgroup.org:7258'
    )
    assert f.filename == 'tall.data.hdfgroup.org'
    assert f.name == '/'
    assert f.id.id == '4af80138-3e8a-11e6-a48f-0242ac110003'

    g2 = f['g2']

    assert g2.id.id != f.id.id
    assert g2.id.id == '4af955c4-3e8a-11e6-a48f-0242ac110003'
    assert g2.name == '/g2'
    assert len(g2) == 2

    assert keys(g2) == ['dset2.1', 'dset2.2']

    assert ('xyz' in g2) is False
    assert ('dset2.1' in g2) is True

    dset21 = g2['dset2.1']
    assert dset21.id.id == '4af97dd8-3e8a-11e6-a48f-0242ac110003'
    assert dset21.name == '/g2/dset2.1'
    assert dset21.shape == (10,)
    assert dset21.dtype == dtype('>f4')  # four numpy fields?

    dset111 = f['/g1/g1.1/dset1.1.1']
    assert dset111.id.id == '4af8bc72-3e8a-11e6-a48f-0242ac110003'
    assert dset111.name == '/g1/g1.1/dset1.1.1'
    assert dset111.shape == (10, 10)
    assert dset111.dtype == dtype('>i4')
    assert len(dset111) == 10

    assert len(dset111.attrs) == 2
    #    assert type(dset111.attrs.keys()) is KeysView
    assert keys(dset111.attrs) == ['attr1', 'attr2']

    f.visit(visit_item)
    assert visitedItems == [
        '/g2',
        '/g2/dset2.2',
        '/g2/dset2.1',
        '/g1',
        '/g1/g1.2',
        '/g1/g1.2/g1.2.1',
        '/g1/g1.1',
        '/g1/g1.1/dset1.1.2',
        '/g1/g1.1/dset1.1.1'
    ]

    status = f.visit(find_g1_2)
    # visit aborts iteration
    assert foundItems == ['/g2', '/g2/dset2.2', '/g2/dset2.1']
    assert status is None  # visit does not return search status

    # print('visititems...')
    # visit_item_obj()
    f.visititems(visit_item_obj)
    assert visitedItemsDict == {
        '/g1': '4af86b14-3e8a-11e6-a48f-0242ac110003',
        '/g1/g1.1': '4af88f0e-3e8a-11e6-a48f-0242ac110003',
        '/g1/g1.1/dset1.1.1': '4af8bc72-3e8a-11e6-a48f-0242ac110003',
        '/g1/g1.1/dset1.1.2': '4af8e602-3e8a-11e6-a48f-0242ac110003',
        '/g1/g1.2': '4af90b64-3e8a-11e6-a48f-0242ac110003',
        '/g1/g1.2/g1.2.1': '4af930ee-3e8a-11e6-a48f-0242ac110003',
        '/g2': '4af955c4-3e8a-11e6-a48f-0242ac110003',
        '/g2/dset2.1': '4af97dd8-3e8a-11e6-a48f-0242ac110003',
        '/g2/dset2.2': '4af9a7c2-3e8a-11e6-a48f-0242ac110003'
    }
