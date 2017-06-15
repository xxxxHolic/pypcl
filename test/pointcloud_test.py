'''
Tests of pcl.pointcloud
'''

import os
import sys
import pytest
sys.path.append(os.path.dirname(__file__) + '/' + os.path.pardir)
import pcl

def test_build_cloud():
    '''
    Test Generating point cloud from arrays
    '''
    cloud = pcl.PointCloud()
    cloud = pcl.PointCloud(width=2, height=2)
    with pytest.raises(TypeError):
        cloud = pcl.PointCloud(fields=('x', 'y', 'z'))
        cloud = pcl.PointCloud(width=2, height=2, fields=('x', 'y', 'z'))
    assert cloud.fields == []

    data = [[1, 2., 3.], [4, 5., 6.]]
    cloud = pcl.PointCloud(data, ('x', 'y', 'z'))
    cloud = pcl.PointCloud(data, [('x', 'i1'), ('y', 'f2'), ('z', 'f2')])
    cloud = pcl.PointCloud(data, [('x', 1, 'I'), ('y', 'f', 2), ('z', 2, 'F')])
    cloud = pcl.PointCloud(data, cloud.data.dtype)
    assert cloud.fields == [('x', 'i1'), ('y', 'f2'), ('z', 'f2')]

    data = [[1, (2., 3.)], [4, (5., 6.)]]
    # pity that numpy do not support inferring tuple types
    # cloud = pcl.PointCloud(data, ('x', 'yz'))
    cloud = pcl.PointCloud(data, [('x', 'i1'), ('yz', '2f2')])
    cloud = pcl.PointCloud(data, [('x', 1, 'I'), ('yz', 'f', 2, 2)])
    cloud = pcl.PointCloud(data, cloud.data.dtype)
    assert cloud.fields == [('x', 'i1'), ('yz', '2f2')]

    data = [[1, 2., 3.], [4, 5., 6.], [7, 8., 9.], [10, 11., 12.]]
    cloud = pcl.PointCloud(width=2, height=2, fields=[('x', 'i1'), ('y', 'f2'), ('z', 'f2')])
    cloud = pcl.PointCloud(data, width=2, height=2, fields=('x', 'y', 'z'))
    cloud = pcl.PointCloud(data, width=2, height=2, fields=[('x', 'i1'), ('y', 'f2'), ('z', 'f2')])
    cloud = pcl.PointCloud(data, width=2, height=2,
                           fields=[('x', 1, 'I'), ('y', 'f', 2), ('z', 2, 'F')])
    cloud = pcl.PointCloud(cloud, cloud.data.dtype)
    assert cloud.fields == [('x', 'i1'), ('y', 'f2'), ('z', 'f2')]

    return cloud

def test_cloud_operations():
    '''
    Test operations on the point cloud
    '''
    cloud = test_build_cloud()
    # for point in cloud:
    #     print(point)

    assert cloud.names == ['x', 'y', 'z']
    assert cloud.width == 2 and cloud.height == 2
    assert cloud.data.tolist() == [(1, 2., 3.), (4, 5., 6.), (7, 8., 9.), (10, 11., 12.)]
    assert cloud[2].tolist() == (7, 8., 9.)
    assert cloud[:2].tolist() == [(1, 2., 3.), (4, 5., 6.)]
    assert cloud['x'].tolist() == [1, 4, 7, 10]
    assert cloud[['x', 'y']].tolist() == [(1, 2.), (4, 5.), (7, 8.), (10, 11.)]
    assert cloud['x', 'y'].tolist() == [(1, 2.), (4, 5.), (7, 8.), (10, 11.)]
    assert cloud[1, 0] == cloud[2] and cloud[0, 1] == cloud[1]
    assert cloud[:2, :2].tolist() == [[(1, 2., 3.), (4, 5., 6.)], [(7, 8., 9.), (10, 11., 12.)]]
    del cloud[[1, 3]]
    cloud.insert([1, 2], [(2, 3., 3.), (4, 6, 6)])
    cloud.append([(0, 0, 0)])
    assert cloud.pop().tolist() == (0, 0., 0.)
    cloud += [(10, 9., 8.), (8, 9., 10.)]
    assert len(cloud) == 6

def test_cloud_field_operations():
    '''
    Test operations on the fields of point cloud
    '''
    cloud = test_build_cloud()

    with pytest.raises(TypeError):
        cloud.append_fields([('x', 'i2')], 4)
        cloud.insert_fields([('x', 'i1')], [3])
    assert cloud.to_ndarray(['y', 'z']).tolist() == [[2, 3], [5, 6], [8, 9], [11, 12]]
    cloud.append_fields([('w', 'i2')], 4)
    assert cloud.names == ['x', 'y', 'z', 'w']
    assert cloud['w'].tolist() == [4, 4, 4, 4]
    cloud.append_fields([('a', 'f2'), ('b', 'f2')], {'a':[1, 2, 3, 4], 'b':[5, 6, 7, 8]})
    assert cloud.names == ['x', 'y', 'z', 'w', 'a', 'b']
    cloud.insert_fields([('t', 'i1')], [3])
    assert cloud.names == ['x', 'y', 'z', 't', 'w', 'a', 'b']
    del cloud['w']
    del cloud['a', 'b']
    assert cloud.names == ['x', 'y', 'z', 't']
    cloud.insert_fields([('r', 'i1'), ('s', 'i2'), ('u', 'f8')], (3, 3, 4), \
                        {'r':[0, 0, 0, 0], 's':[1, 1, 1, 1]})
    assert cloud.names == ['x', 'y', 'z', 'r', 's', 't', 'u']
    del cloud['x', 'y', 'z', 'u']
    cloud.insert_fields([('k', 'f8')], [3], 6)
    cloud.insert_fields([('a', 'i2'), ('b', 'i4')], [4, 4], \
                        [[1, 2, 3, 4], [5, 6, 7, 8]])
    del cloud['a', 'b']
    cloud.insert_fields([('a', 'i2'), ('b', 'i4')], [4, 4], \
                        pcl.np.array([(1, 5), (2, 6), (3, 7), (4, 8)], \
                                     dtype=[('a', 'i2'), ('b', 'i4')]))
    assert cloud.names == ['r', 's', 't', 'k', 'a', 'b']


if __name__ == '__main__':
    pytest.main([__file__, '-s'])
# test_cloud_field_operations()
