__author__ = 'luoming'
import Queue
from math import fabs

T = [(2,3), (5,4), (9,6), (4,7), (8,1), (7,2)]

class TreeNode:
    def __init__(self, p, d):
        self.data = p
        self.dimension = d
        self.left = None
        self.right = None

def sift_down(A, i, n):
    s = i * 2 + 1
    t = A[i]
    while s < n:
        if s + 1 < n and A[s] < A[s+1]:
            s += 1
        if t < A[s]:
            A[i] = A[s]
            i = s
            s = i * 2 + 1
        else:
            break
    A[i] = t

def build_heap(A, n):
    for i in range(0, n/2)[::-1]:
        sift_down(A, i, n)

def heap_sort(A, n):
    for i in range(0, n/2)[::-1]:
        sift_down(A, i, n)
    for j in range(1, n)[::-1]:
        A[0], A[j] = A[j], A[0]
        sift_down(A, 0, j)

def k_min(A, k):
    n = len(A)
    build_heap(A, k)
    for i in range(k, n):
        if A[i] < A[0]:
            A[0] = A[i]
            sift_down(A, 0, k)
    return A[0]

def split_data(data, i):
    lefttree = []
    righttree = []
    t = [example[i] for example in data]
    median = k_min(t, len(t)/2+1)
    for point in data:
        if point[i] < median:
            lefttree.append(point)
        elif point[i] > median:
            righttree.append(point)
        else:
            midpoint = point
    return midpoint, lefttree, righttree

def create_kd_tree(dataSet, i, k):
    if 1 == len(dataSet):
        return TreeNode(dataSet[0], i)
    rootdata, left, right = split_data(dataSet, i)
    root = TreeNode(rootdata, i)
    if len(left) > 0:
        root.left = create_kd_tree(left, (i+1)%k, k)
    if len(right) > 0:
        root.right = create_kd_tree(right, (i+1)%k, k)
    return root

def level_traverse(T):
    if T == None:
        return
    queue = Queue.Queue()
    queue.put(T)
    while not queue.empty():
        node = queue.get()
        print node.data, node.dimension
        if node.left != None:
            queue.put(node.left)
        if node.right != None:
            queue.put(node.right)

def next_node_search(tree, nearest, nearestNode, target):
    if tree == None:
        return nearest
    optimal = nearest
    optimalNode = nearestNode
    queue = Queue.Queue()
    queue.put(tree)
    while not queue.empty():
        node = queue.get()
        dist = 0
        for i in range(len(node.data)):
            dist += (node.data[i] - target[i]) * (node.data[i] - target[i])
        if dist < optimal:
            optimal = dist
            optimalNode = node.data
        if node.left != None:
            queue.put(node.left)
        if node.right != None:
            queue.put(node.right)
    return optimal, optimalNode


def kd_tree_search(kd_tree, target):
    if kd_tree == None:
        return 0, None
    dimension = kd_tree.dimension
    if target[dimension] <= kd_tree.data:
        kNN, kNNPoint= kd_tree_search(kd_tree.left, target)
        if kNNPoint == None:
            kNNPoint = kd_tree.data
            for i in range(len(kNNPoint)):
                kNN += (kNNPoint[i] - target[i]) * (kNNPoint[i] - target[i])
        if kd_tree.right != None:
            if fabs(kd_tree.data[dimension] - kNNPoint[dimension]) < kNN:
                kNN, kNNPoint = next_node_search(kd_tree.right, kNN, kNNPoint, target)
    elif target[dimension] > kd_tree.data:
        kNN, kNNPoint = kd_tree_search(kd_tree.right, target)
        if kNNPoint == None:
            kNNPoint = kd_tree.data
            for i in range(len(kNNPoint)):
                kNN += (kNNPoint[i] - target[i]) * (kNNPoint[i] - target[i])
        if kd_tree.left != None:
            if fabs(kd_tree.data[dimension] - kNNPoint[dimension]) < kNN:
                kNN, kNNPoint = next_node_search(kd_tree.left, kNN, kNNPoint, target)
    return kNN, kNNPoint


if __name__ == '__main__':
    kdtree = create_kd_tree(T, 0, 2)

    kNN, kNNPoint = kd_tree_search(kdtree, (9, 7))
    print kNNPoint
#    level_traverse(kdtree)



