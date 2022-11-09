import queue

class Tree:
    def __init__(self, root = None):
        self.root = root

class Node:
    def __init__(self, key = None, right = None, left = None, height = None): #키값, 오른쪽 자식 노드, 왼쪽 자식 노드, 높이
        self.key = key
        self.right = right
        self.left = left
        self.height = height



def inorder(T):
    if T.root.right == None and T.root.left == None:
        print(T.root.key)
        return

    buffer = queue.LifoQueue()
    buffer.put(T.root)
    visit = 0
    values = []
    node = T.root

    while not buffer.empty():
        node = buffer.get()
        buffer.put(node)
        if node.left != None and visit == 0:
            buffer.put(node.left)
        elif node.left == None and node.right == None:
            value = buffer.get()
            values.append(value.key)
            visit = 1
        else:
            value = buffer.get()
            values.append(value.key)
            if value.right != None:
                buffer.put(value.right)
                visit = 0
    for i in values:
        print(i, "", end = '')
    print()


def searchBST(T, searchKey):
    node = T.root

    while node != None:
        if node.key > searchKey:
            node = node.left
        elif node.key < searchKey:
            node = node.right
        elif node.key == searchKey:
            return node

    return None 

def height(Node):
    if Node == None:
        return 0

    maxHeight = 0
    Nodes = Node
    stack = queue.LifoQueue()
    stack.put(Nodes)

    while not stack.empty():
        node = stack.get()
        
        if node.height > maxHeight:
            maxHeight = node.height #노드가 이전 최대 높이보다 높다면

        if node.right != None:
            stack.put(node.right)

        if node.left != None:
            stack.put(node.left)

    return maxHeight
        
def maxNode(Node):
    node = Node
    
    while True:
        if node.right != None:
            node = node.right
        else:
            break
    
    return node

def minNode(Node):
    node = Node
    
    while True:
        if node.left != None:
            node = node.left
        else:
            break
    
    return node

def noNode(Node):
    count = 0
    Nodes = Node
    stack = queue.LifoQueue()
    stack.put(Nodes)

    while not stack.empty():
        node = stack.get()
        count += 1

        if node.right != None:
            stack.put(node.right)

        if node.left != None:
            stack.put(node.left)

    return count

def parentBST(T, findKey):
    node = T.root
    dir = 0

    if node.key == findKey:
        return None

    while node != None:
        parent = node

        if node.key > findKey:
            node = node.left
            dir = 1 #부모노드가 왼쪽으로 이어져 있다면
        elif node.key < findKey:
            node = node.right
            dir = -1 #부모노드가 오른쪽으로 이어져 있다면

        if node.key == findKey:
            return [parent, dir]


def insertBST(T, newKey):
    node = Node(newKey, None, None, None)
    root = T.root

    if searchBST(T, newKey) != None:
        return print("i {} : The key already exist".format(newKey))

    if root == None:
        node.height = 1
        T.root = node
    else:
        next_node = T.root
        while next_node != None:
            temp = next_node
            if next_node.key > newKey:
                next_node = next_node.left
            else:
                next_node = next_node.right
        
        if temp.key > newKey:
            node.height = temp.height + 1
            temp.left = node
        elif temp.key < newKey:
            node.height = temp.height + 1
            temp.right = node
        
            
def deleteBST(T, deleteKey):
    delNode = searchBST(T, deleteKey)
    if delNode == None:
        return print("d {} : The key does not exist".format(deleteKey))

    #삭제 할 노드의 부모찾기
    temp = parentBST(T, deleteKey)
    if temp != None:
        parentNode, dir = temp[0], temp[1]
    else:
        parentNode, dir = None, 0
    
    #삭제 할 노드가 1개 남았다면(루트 노드)
    if T.root.right == None and T.root.left == None:
        T.root = None
        return

    #자식 노드가 없다면 -> 바로 삭제
    if delNode.right == None and delNode.left == None:
        if dir == -1:
            parentNode.right = None
        else:
            parentNode.left = None
        return    

    #자식 노드가 있다면 -> 교체할 노드를 선정, 교체할 노드의 부모 노드 할당, 교체할 노드의 부모와 연결 끊기
    if height(delNode.left) < height(delNode.right):
        Cnode = minNode(delNode.right)
        temp = parentBST(T, Cnode.key)
        Cparent, Cdir = temp[0], temp[1]
    elif height(delNode.left) == height(delNode.right) and noNode(delNode.left) < noNode(delNode.right):
        Cnode = minNode(delNode.right)
        temp = parentBST(T, Cnode.key)
        Cparent, Cdir = temp[0], temp[1]
    else:
        Cnode = maxNode(delNode.left)
        temp = parentBST(T, Cnode.key)
        Cparent, Cdir = temp[0], temp[1]

    if Cdir == 1:
        Cparent.left = None
    else:
        Cparent.right = None

    #교체할 노드와 삭제할 노드가 부모 자식 관계라면
    #부모노드를 삭제한 후  교체할 노드의 그대로 교체
    if Cparent.key == deleteKey:
        if dir == 1 or dir == 0: #삭제한 노드의 부모가 왼쪽으로 이어져 있다면
            #삭제할 노드가 루트노드인지 구분
            if parentNode != None:
                parentNode.left = Cnode
            else:
                T.root = Cnode
            
            if Cparent.left != None:
                Cnode.left = Cparent.left
            elif Cparent.right != None:
                Cnode.right = Cparent.right

        elif dir == -1: #삭제한 노드의 부모가 오른쪽으로 이어져 있다면
            parentNode.right = Cnode
            if Cparent.left != None:
                Cnode.left = Cparent.left
            elif Cparent.right != None:
                Cnode.right = Cparent.right
        return

    #삭제할 노드와 교체할 노드가 거리가 있다면
    #교체할 노드의 자식들을 부모노드에게 인계 또한 삭제할 노드의 부모와 교체할 노드를 연결
    if dir == 1 or dir == 0: #삭제할 노드가 부모노드와 왼쪽으로 연결 혹은 루트 노드라면
        if parentNode != None:
            parentNode.left = Cnode
        else:
            T.root = Cnode

        if Cdir == -1:
            Cparent.right = Cnode.left if Cnode.left != None else Cnode.right
        else:
            Cparent.left = Cnode.left if Cnode.left != None else Cnode.right
    else:
        parentNode.right = Cnode

        if Cdir == 1:
            Cparent.left = Cnode.left if Cnode.left != None else Cnode.right
        else:
            Cparent.right = Cnode.left if Cnode.left != None else Cnode.right

    #삭제한 노드의 자식노드들을 교체한 노드에게 인계
    Cnode.right = delNode.right
    Cnode.left = delNode.left
        

T = Tree()

cmd, key = input().split()
insertBST(T, int(key))
inorder(T)

while T.root != None:
    cmd, key = input().split()
    if cmd == 'd':
        deleteBST(T, int(key))
    elif cmd == 'i':
        insertBST(T, int(key))

    if T.root != None:
        inorder(T)