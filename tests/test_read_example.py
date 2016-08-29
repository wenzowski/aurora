import pytest
import numpy


@pytest.fixture
def mnt():
    import h5pyd as h5py
    # there is one public/ folder at the root path
    return h5py.File('/', 'r', endpoint='http://localhost:5000')


@pytest.fixture
def tall_file(mnt):
    # there is one file in the public/ folder named tall.h5
    return mnt['/public/tall']


# WARN mnt.id.id is volatile: changes with every h5serv index operation
def test_mountpoint(mnt):
    assert mnt.filename == '/'
    assert mnt.name == '/'
    assert mnt.id.id == 'ba88a35e-6e23-11e6-a230-04016789eb01'
    assert len(mnt) == 1
    assert [key for key in mnt] == ['public']


def test_folders_can_be_opened_by_relative_path(mnt):
    public_folder = mnt['public']
    assert public_folder.id.id == 'ba88a35f-6e23-11e6-a230-04016789eb01'


def test_folders_can_be_opened_by_absolute_path(mnt):
    public_folder = mnt['/public']
    assert public_folder.id.id == 'ba88a35f-6e23-11e6-a230-04016789eb01'


def test_files_can_be_opened_by_relative_path(mnt):
    tall_file = mnt['public/tall']
    assert tall_file.id.id == 'ca73fe34-6e1f-11e6-a230-04016789eb01'


def test_files_can_be_opened_by_absolute_path(mnt):
    tall_file = mnt['/public/tall']
    assert tall_file.id.id == 'ca73fe34-6e1f-11e6-a230-04016789eb01'


def test_folders_have_no_root_scope(mnt):
    tall_file = mnt['/public/tall']
    with pytest.raises(KeyError):
        tall_file['/public']


def test_list_folders(mnt):
    assert len(mnt) == 1
    assert [key for key in mnt] == ['public']


def test_list_files(mnt):
    public_folder = mnt['/public']
    assert len(public_folder) == 1
    assert [key for key in public_folder] == ['tall']


def test_top_level_group_in_file_has_no_filename_attribute(tall_file):
    with pytest.raises(AttributeError):
        tall_file.filename


def test_top_level_group_in_file_has_subgroups(tall_file):
    assert tall_file.name == '/'
    assert len(tall_file) == 2
    assert [key for key in tall_file] == ['g1', 'g2']


def test_file_paths_cannot_be_combined_with_dataset_paths(mnt):
    with pytest.raises(KeyError):
        mnt['/public/tall/g1']


def test_file_indicies_can_be_opened_by_relative_path(tall_file):
    g1_1 = tall_file['g1/g1.1']
    assert g1_1.id.id == 'ca73fe36-6e1f-11e6-a230-04016789eb01'


def test_file_indicies_can_be_opened_by_absolute_path(tall_file):
    g1_1 = tall_file['/g1/g1.1']
    assert g1_1.id.id == 'ca73fe36-6e1f-11e6-a230-04016789eb01'


def test_root_scope_of_file_index_is_not_contextual(tall_file):
    g1_1 = tall_file['/g1/g1.1']
    g1 = g1_1['/g1']
    assert g1.id.id == tall_file['/g1'].id.id


def test_true_when_subscope_exists(tall_file):
    assert ('g1' in tall_file) is True


def test_subscope_exists(tall_file):
    assert ('nobody.can.find.me' in tall_file) is False


def test_folder_type(mnt):
    from h5pyd._hl.files import File
    assert isinstance(mnt, File)


def test_file_type(mnt):
    from h5pyd._hl.group import Group
    public_folder = mnt['/public']
    assert isinstance(public_folder, Group)


def test_group_type(tall_file):
    from h5pyd._hl.group import Group
    assert isinstance(tall_file, Group)


def test_1d_data_type(tall_file):
    from h5pyd._hl.dataset import Dataset
    dset1_1_2 = tall_file['/g1/g1.1/dset1.1.2']
    assert isinstance(dset1_1_2, Dataset)


def test_2d_data_type(tall_file):
    from h5pyd._hl.dataset import Dataset
    dset1_1_1 = tall_file['/g1/g1.1/dset1.1.1']
    assert isinstance(dset1_1_1, Dataset)


def test_1d_dataset_has_keys(tall_file):
    dset1_1_2 = tall_file['/g1/g1.1/dset1.1.2']
    assert dset1_1_2.name == '/g1/g1.1/dset1.1.2'
    assert dset1_1_2.dims is None
    assert dset1_1_2.dtype == numpy.dtype('>i4')
    assert dset1_1_2.shape == (20, )
    assert len(dset1_1_2) == 20
    assert numpy.array_equal(
        [key for key in dset1_1_2],
        numpy.arange(20)
    )


def test_1d_dataset_has_attributes(tall_file):
    from h5pyd._hl.attrs import AttributeManager
    from collections import KeysView
    dset1_1_2 = tall_file['/g1/g1.1/dset1.1.2']
    parent = tall_file['/g1/g1.1']
    #  assert len(dset1_1_2.attrs) == 0
    #  assert [key for key in dset1_1_2.attrs] == []
    attrs = AttributeManager(parent)
    assert isinstance(dset1_1_2.attrs, AttributeManager)
    assert dset1_1_2.attrs == attrs
    assert type(dset1_1_2.attrs.keys()) == KeysView


def test_2d_dataset_has_keys(tall_file):
    dset1_1_1 = tall_file['/g1/g1.1/dset1.1.1']
    assert dset1_1_1.name == '/g1/g1.1/dset1.1.1'
    assert dset1_1_1.dims is None
    assert dset1_1_1.dtype == numpy.dtype('>i4')
    assert dset1_1_1.shape == (10, 10)
    assert len(dset1_1_1) == 10
    assert numpy.array_equal(
        [key for key in dset1_1_1][0][0],
        numpy.zeros((10), dtype=numpy.int32)
    )
    assert numpy.array_equal(
        [key for key in dset1_1_1][0],
        numpy.zeros((1, 10), dtype=numpy.int32)
    )
    # assert numpy.array_equal(
    #     dset1_1_1,
    #     numpy.zeros((1, 10), dtype=numpy.int32)
    # )


def test_walk_h5_file_index_tree(tall_file):
    def visit_item(name):
        visitedItems.append(name)
        return None
    visitedItems = []
    tall_file.visit(visit_item)
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


def test_partially_walk_h5_file_index_tree(tall_file):
    def find_dset2_1(name):
        foundItems.append(name)
        if name == '/g2/dset2.1':
            return True
        return None
    foundItems = []
    tall_file.visit(find_dset2_1)
    assert foundItems == [
       '/g2',
       '/g2/dset2.2',
       '/g2/dset2.1'
    ]


def test_walk_and_read_h5_file_index_tree(tall_file):
    def visit_item_obj(name, obj):
        visitedItemsDict[name] = obj.id.id
        return None
    visitedItemsDict = {}
    tall_file.visititems(visit_item_obj)
    assert visitedItemsDict == {
        '/g1': 'ca73fe35-6e1f-11e6-a230-04016789eb01',
        '/g1/g1.1': 'ca73fe36-6e1f-11e6-a230-04016789eb01',
        '/g1/g1.1/dset1.1.1': 'ca73fe37-6e1f-11e6-a230-04016789eb01',
        '/g1/g1.1/dset1.1.2': 'ca73fe38-6e1f-11e6-a230-04016789eb01',
        '/g1/g1.2': 'ca73fe39-6e1f-11e6-a230-04016789eb01',
        '/g1/g1.2/g1.2.1': 'ca73fe3a-6e1f-11e6-a230-04016789eb01',
        '/g2': 'ca73fe3b-6e1f-11e6-a230-04016789eb01',
        '/g2/dset2.1': 'ca73fe3c-6e1f-11e6-a230-04016789eb01',
        '/g2/dset2.2': 'ca73fe3d-6e1f-11e6-a230-04016789eb01'
    }
