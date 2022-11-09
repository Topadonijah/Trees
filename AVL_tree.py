# 삽입: 성공
# 삭제: 성공

f = open("AVL-input.txt", 'r')# 읽어올 텍스트 파일의 경로

import queue

class Tree:
    def __init__(self, root = None):
        self.root = root

class Node:
    def __init__(self, key = None, right = None, left = None, height = None, bf = None): #키값, 오른쪽 자식 노드, 왼쪽 자식 노드, 높이, 균형인수
        self.key = key
        self.right = right
        self.left = left
        self.height = height
        self.bf = bf


def inorder(T): #중위 순회 탐색
    if T.root.right == None and T.root.left == None: # 루트노드 하나뿐이라면 바로 출력
        print("({}, {})".format(T.root.key, T.root.bf))
        return

    buffer = queue.LifoQueue()
    buffer.put(T.root)
    visit = 0
    values = []
    node = T.root

    while not buffer.empty():
        node = buffer.get()
        buffer.put(node)

        if node.left != None and visit == 0: #노드의 왼쪽에 자식이 있고 아직 방문하지 않았다면
            buffer.put(node.left)
        elif node.left == None and node.right == None: #노드에게 자식이 없다면
            value = buffer.get()
            values.append((value.key, value.bf))
            visit = 1 #방문완료 표시
        else: # 오른쪽 노드로 방문해야 하는 상황이라면
            value = buffer.get()
            values.append((value.key, value.bf))
            if value.right != None:
                buffer.put(value.right)
                visit = 0 # 방문 초기화

    for i in values:
        print(i, "", end = '')
    print()


def searchBST(T, searchKey): #입력받은 키값을 검색
    node = T.root

    while node != None:
        if node.key > searchKey:
            node = node.left
        elif node.key < searchKey:
            node = node.right
        elif node.key == searchKey:
            return node

    return None 

def height(Node): # 해당노드의 서브트리의 높이를 구하는 함수
    if Node == None:
        return 0

    list = []
    Nodes = Node
    stack = queue.LifoQueue()
    stack.put((Nodes,1))

    while not stack.empty():
        node_info = stack.get()
        node, height = node_info[0], node_info[1]

        if node.right != None: # 오른쪽에 자식노드가 있다면
            stack.put((node.right, height + 1))

        if node.left != None: # 왼쪽에 자식노드가 있다면
            stack.put((node.left, height + 1))

        if node.left == None and node.right == None: # 자식이 없는 노드라면
            list.append(height) # 높이 정보를 입력

    maxHeight = 0

    for i in list:
        if i > maxHeight:
            maxHeight = i

    return maxHeight # 서브트리의 높이를 리턴
        
def maxNode(Node): # 최대 키값을 탐색
    node = Node
    
    while True: #오른쪽으로 계속 진행
        if node.right != None:
            node = node.right
        else:
            break
    
    return node

def minNode(Node): #최소 키값을 탐색
    node = Node
    
    while True: #왼쪽으로 계속 진행
        if node.left != None:
            node = node.left
        else:
            break
    
    return node

def noNode(Node): #해당 노드의 서브트리안 노드의 총 갯수를 세어주는 함수
    count = 0
    Nodes = Node
    stack = queue.LifoQueue()
    stack.put(Nodes)

    while not stack.empty():
        node = stack.get()
        count += 1

        if node.right != None: #오른쪽에 자식이 있다면
            stack.put(node.right)

        if node.left != None: #왼쪽에 자식이 있다면
            stack.put(node.left)

    return count

def parentBST(T, findKey): #입력받은 노드의 부모노드를 찾아주는 함수
    node = T.root
    dir = 0

    if node.key == findKey: #노드가 루트노드라면
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

#avl 균형체크 
def checkBalance(T, newKey):
    stack = queue.LifoQueue()#키가 담긴 노드까지의 경로를 담을 스택
    p = T.root
    q = None
    balance = True #균형 여부
    parent = None

    while True:
        if newKey < p.key: #현재 노드보다 찾는 값이 작다면 왼쪽으로 이동
            stack.put(p)
            p = p.left
        elif newKey > p.key: #현재 노드보다 찾는 값이 크다면 오른쪽으로 이동
            stack.put(p)
            p = p.right
        else: #값이 같다면 종료
            stack.put(p)
            break

    bf_stack = stack #스택에 담긴 노드정보를 기억

    while not stack.empty():
        q  = stack.get()
        q.height = height(q)
        q.bf = min(height(q.left), q.height) - min(height(q.right), q.height) # 양쪽 자식노드의 높이 비교
        if abs(q.bf) > 1: # 균형인수가 -2 혹은 2라면
            if balance:
                balance = False # 균형깨짐
                p = q
                parent = parentBST(T, p.key)
        
    if parent == None:
        parent = [None]

    if balance:
        return "NO", p, parent[0]
        
    if p.bf > 1: # 불균형이 왼쪽으로 시작된다면
        if p.left.bf > 0: # 불균형이 왼쪽으로 계속된다면
            return "LL", p, parent[0]
        else: #불균형이 오른쪽으로 바뀐다면
            return "LR", p, parent[0]
    elif p.bf < -1: #불균형이 오른쪽으로 시작된다면
        if p.right.bf > 0: #불균형이 왼쪽으로 바뀐다면
            return "RL", p, parent[0]
        else:
            return "RR", p, parent[0]

def rotationTree(T, rotationType, p, q): #불균형 노드에 대하여 회전을 실행
    if rotationType == "LL": #LL회전 
        p_child = p.left #불균형 노드의 자식
        p_child2 = p_child.left # 불균형 노드 자식의 자식
        temp = p_child.right #불균형 노드 자식의 오른쪽 자식을 임시 보관

        if q != None: #부모가 존재한다면
            if(p.key < q.key): #부모와 불균형 노드가 왼쪽으로 이어져 있다면
                q.left = p_child
            else: # 부모와 불균형 노드가 오른쪽으로 이어져 있다면
                q.right = p_child
        else: #루트노드라면
            T.root = p_child

        p_child.right = p #LL회전을 통해 루트 노드를 변경
        p.left = temp #자녀노드의 자녀들을 루트노드에게 인계
    elif rotationType == "LR":
        p_child = p.left #불균형 노드의 자식
        p_child2 = p_child.right # 자식노드의 자식노드
        temp1, temp2 = p_child2.left, p_child2.right  #루트로 올릴 노드의 자식노드들을 임시 보관

        if q != None: #부모가 존재한다면
            if(p.key < q.key): #부모와 불균형 노드가 왼쪽으로 이어져 있다면
                q.left = p_child2
            else: # 부모와 불균형 노드가 오른쪽으로 이어져 있다면
                q.right = p_child2
        else:
            T.root = p_child2
        p_child2.left = p_child # LR회전을 통해 루트노드로 올린 노드의 자식노드를 변경
        p_child2.right = p
        p_child.right = temp1 # 루트노드로 올라간 노드가 가지고 있던 자식노드를 각각의 노드들에게 인계
        p.left = temp2

    elif rotationType == "RR":
        p_child = p.right #불균형 노드의 자식
        p_child2 = p_child.right # 불균형 노드 자식의 자식
        temp = p_child.left #불균형 노드 자식의 오른쪽 자식을 임시 보관

        if q != None: #부모가 존재한다면
            if(p.key < q.key): #부모와 불균형 노드가 왼쪽으로 이어져 있다면
                q.left = p_child
            else: # 부모와 불균형 노드가 오른쪽으로 이어져 있다면
                q.right = p_child
        else:
            T.root = p_child

        p_child.left = p #LL회전을 통해 루트 노드를 변경
        p.right = temp #자녀노드의 자녀들을 루트노드에게 인계
    else: #RL 회전
        p_child = p.right #불균형 노드의 자식
        p_child2 = p_child.left # 자식노드의 자식노드
        temp1, temp2 = p_child2.left, p_child2.right  #루트로 올릴 노드의 자식노드들을 임시 보관

        if q != None: #부모가 존재한다면
            
            if(p.key < q.key): #부모와 불균형 노드가 왼쪽으로 이어져 있다면
                q.left = p_child2
            else: # 부모와 불균형 노드가 오른쪽으로 이어져 있다면
                q.right = p_child2
        else:
            T.root = p_child2

        p_child2.left = p # RL회전을 통해 루트노드로 올린 노드의 자식노드를 변경
        p_child2.right = p_child
        p_child.left = temp2 # 루트노드로 올라간 노드가 가지고 있던 자식노드를 각각의 노드들에게 인계
        p.right = temp1
    
    if q != None:
        checkBalance(T, q.key) # 회전이 일어난 노드의 부모노드들의 균형인수 최신화
    
    # 회전된 세 노드에 대하여 균형인수 최신화 
    p.bf = max(height(p.left), p.height) - max(height(p.right), p.height)
    p_child.bf = max(height(p_child.left), p_child.height) - max(height(p_child.right), p_child.height)
    p_child2.bf = max(height(p_child2.left), p_child2.height) - max(height(p_child2.right), p_child2.height)
    


def insertBST(T, newKey): #bst삽입
    node = Node(newKey, None, None, None, 0)
    root = T.root
    buffer = queue.LifoQueue()

    if searchBST(T, newKey) != None:
        print("i {} : The key already exist".format(newKey))
        return True # 값이 겹침

    if root == None: #삽입될 위치가 루트라면
        node.height = 1
        T.root = node
    else:
        next_node = T.root

        while next_node != None: #삽입할 위치까지의 경로를 저장하며 삽입할 위치까지 탐색
            buffer.put(next_node)
            temp = next_node
            if next_node.key > newKey:
                next_node = next_node.left
            else:
                next_node = next_node.right
        
        if temp.key > newKey:
            node.height = 1
            temp.left = node
        elif temp.key < newKey:
            node.height = 1
            temp.right = node

    while not buffer.empty():
        node = buffer.get()
        node.height = height(node) #삽입된 부모노드부터 루트까지의 높이값을 최신화함

    return False # 값이 겹치지 않고 삽입됌
        
            
def deleteBST(T, deleteKey):

    delNode = searchBST(T, deleteKey)

    if delNode == None: # 삭제할 노드가 존재하지 않는다면
        print("d {} : The key does not exist".format(deleteKey))
        inorder(T)
        return None 

    #삭제 할 노드의 부모찾기
    temp = parentBST(T, deleteKey)
    if temp != None:
        parentNode, dir = temp[0], temp[1]
    else:
        parentNode, dir = None, 0

    #삭제 할 노드가 1개 남았다면(루트 노드)
    if T.root.right == None and T.root.left == None:
        T.root = None
        return None

    #자식 노드가 없다면 -> 바로 삭제
    if delNode.right == None and delNode.left == None:
        if dir == -1:
            parentNode.right = None
        else:
            parentNode.left = None
        return parentNode #삭제할 노드의 부모를 리턴하여 균형계산

    #자식 노드가 있다면 -> 교체할 노드를 선정, 교체할 노드의 부모 노드 할당, 교체할 노드의 부모와 연결 끊기
    if height(delNode.left) < height(delNode.right):
        Cnode = minNode(delNode.right) # 교체할 노드
        temp = parentBST(T, Cnode.key) # 교체할 노드의 부모정보
        Cparent, Cdir = temp[0], temp[1] #교체할 노드의 부모노드, 부모노드와 이어진 방향
    elif height(delNode.left) == height(delNode.right) and noNode(delNode.left) < noNode(delNode.right):
        Cnode = minNode(delNode.right)
        temp = parentBST(T, Cnode.key)
        Cparent, Cdir = temp[0], temp[1]
    else:
        Cnode = maxNode(delNode.left)
        temp = parentBST(T, Cnode.key)
        Cparent, Cdir = temp[0], temp[1]

    if Cdir == 1: #교체할 노드가 부모노드와 왼쪽으로 이어져 있다면
        Cparent.left = None #부모노드의 왼쪽을 공백으로
    else:
        Cparent.right = None



    #교체할 노드와 삭제할 노드가 부모 자식 관계라면
    #부모노드를 삭제한 후  교체할 노드의 그대로 교체
    if Cparent.key == deleteKey:
        if dir == 1 or dir == 0: #삭제한 노드의 부모가 왼쪽으로 이어져 있다면 혹은 루트 노드라면
            #삭제할 노드가 루트노드인지 구분
            if parentNode != None: 
                parentNode.left = Cnode
            else: #삭제할 노드가 루트노드라면
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
        return Cnode


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
    return Cparent # 교체할 노드의 부모를 리턴하여 해당 노드부터 균형 검사

def insertAVL(T, newKey):
    over = False

    over = insertBST(T, newKey) #BST삽입 실행 #삽입값이 중복인지 출력
    
    rotationType, p, q = checkBalance(T,newKey) #균형검사 회전유형, 불균형 노드, 불균형 노드의 부모값 리턴

    if not over:
        if rotationType != "NO":
            rotationTree(T, rotationType, p, q) # 트리에 문제가 있다면 해당 노드에 대하여 회전 실시
            print(rotationType, "", end = ' ')
            inorder(T)
        else:
            print(rotationType, "", end = ' ')
            inorder(T)
    else:
        inorder(T)

def deleteAVL(T, newKey):

    p = deleteBST(T, newKey) #BST삭제를 실행, 삭제가 진행되었다면 교체된 노드의 부모노드가 리턴

    if p != None: # 값이 리턴되었다면 
        rotationType, p, q = checkBalance(T, p.key) #변화한 트리에 대하여 균형검사
        if rotationType != "NO": # 균형이 꺠져있다면 
            rotationTree(T, rotationType, p, q)
            print(rotationType, "", end = ' ')
            inorder(T)
        else: #트리의 균형이 알맞다면
            print(rotationType, "", end = ' ')
            inorder(T)

T = Tree()

while True:
    line = f.readline()
    if not line: break
    cmd, key = line.split()
    
    if cmd == 'i':
        insertAVL(T, int(key))
    else:
        deleteAVL(T, int(key))

f.close()