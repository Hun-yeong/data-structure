# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 13:05:42 2016
Written in python 3.1
@author: Hun-yeong
"""

WHITE = 0
GRAY = 1
BLACK = 2


class Adj:
    def __init__(self): 
        self.n = 0
        self.next = None



class DFSVertex(Vertex):
    def __init__(self, name):
        super().__init__(name)
        self.d = 0
        self.f = 0
    def copy(self, other):
        super().copy(other)
        self.d = other.d
        self.f = other.f

class Queue:
    def __init__(self):
        self.front = 0
        self.rear = 0
        self.sz = 0
        self.buf = []
    def create_queue(self,sz):
        self.sz = sz
        self.buf = list(range(sz)) 
    def enqueue(self,val):
        self.buf[self.rear] = val
        self.rear = (self.rear + 1) % self.sz
    def dequeue(self):
        res = self.buf[self.front]
        self.front = (self.front + 1) % self.sz
        return res
    def is_empty(self):
        return self.front == self.rear

def print_vertex(vertices,n):
    print (vertices[n].name, end=' ')
    print (vertices[n].color, end=' ')
    print (vertices[n].parent, end=' ')
    print (vertices[n].d, end=':')
    p = vertices[n].first
    while p:
        print (vertices[p.n].name, end = ' ')
        p = p.next
    print('')

def g_trans(vertices, vertices1):
    for i in range(len(vertices1)):
        vertices1[i].first = None
    for v in vertices:
        p = v.first
        while p:
            vertices1[p.n].add(v)
            p = p.next

class DFS:
    def __init__(self):
        self.time = 0;
        self.vertices = None
        
        
    def set_vertices(self,vertices):
        self.vertices = vertices
        for i in range(len(self.vertices)):
            self.vertices[i].n = i
            
            
    def dfs(self):
        for u in self.vertices:
            u.color = WHITE
            u.parent = -1
        self.time = 0
        for u in self.vertices:
            if u.color == WHITE:
                self.dfs_visit(u)
                
                
    def dfs_visit(self, u):
        self.time = self.time + 1
        u.d = self.time
        u.color = GRAY
        v = u.first
        while v:
            if self.vertices[v.n].color == WHITE:
                self.vertices[v.n].parent = u.n
                self.dfs_visit(self.vertices[v.n])
            v = v.next;
        u.color = BLACK
        self.time = self.time + 1
        u.f = self.time

    def print_scc(self, u):
        print(u.name, end=" ")
        vset = self.vertices
        if u.parent >= 0:
            self.print_scc(vset[u.parent])
        
    def scc_find(self, u):
        u.color = GRAY
        v = u.first
        found = False
        while v:
            if self.vertices[v.n].color == WHITE:
                found = True
                self.vertices[v.n].parent = u.n
                self.scc_find(self.vertices[v.n])
            v = v.next;
        if not found:
            print("SCC:", end=" ")
            self.print_scc(u)
            print ("")
        u.color = BLACK
        
    def print_vertex(self,n):
        print (self.vertices[n].name, end=' ')
        print (self.vertices[n].color, end=' ')
        print (self.vertices[n].parent, end=' ')
        print (self.vertices[n].d, end=' ')
        print (self.vertices[n].f, end=':')
        p = self.vertices[n].first
        while p:
            print (self.vertices[p.n].name, end = ' ')
            p = p.next
        print('')
    def print_vertices(self):
        for i in range(len(self.vertices)):
            self.print_vertex(i)
    def trans(self):
        vertices1 = []
        for v in self.vertices:
            v1 = DFSVertex(v.name)
            v1.copy(v)
            vertices1.append(v1)
        g_trans(self.vertices,vertices1)
        self.set_vertices(vertices1)

    def left(self,n):
        return 2*n+1

    def right(self,n):
        return 2*n+2

    def heapify(self,A,i,heapsize):
        vset = self.vertices
        l = self.left(i)
        r = self.right(i)
        if l < heapsize and vset[A[l]].f < vset[A[i]].f:
            largest = l
        else:
            largest = i
        if r < heapsize and vset[A[r]].f < vset[A[largest]].f:
            largest = r
        if largest != i:
            A[i],A[largest] = A[largest],A[i]
            self.heapify(A,largest,heapsize)

    def buildheap(self,A):
        for i in range(len(A)//2 + 1,0,-1):
            self.heapify(A,i-1,len(A))

    def heapsort(self,A):
        self.buildheap(A)
        for i in range(len(A),1,-1):
            A[i-1],A[0] = A[0],A[i-1]
            self.heapify(A,0,i - 1)
        
    def sort_by_f(self):
        vset = self.vertices
        sorted_indices = list(range(len(vset)))
        self.heapsort(sorted_indices)
        return sorted_indices
    
    def scc(self):
        self.dfs()
        self.print_vertices()
        self.trans()
        sorted = self.sort_by_f()
        vset = self.vertices
        for v in vset:
            v.color = WHITE
            v.parent = -1
        for n in sorted:
            if self.vertices[n].color == WHITE:
                self.scc_find(vset[n])

import sys

INFTY = 1E10

class Heap:
    def __init__(self):
        self.nelem = 0
        self.A = []
    def parent(self,n):
        return (n-1)//2
    def left(self,n):
        return 2*n+1
    def right(self,n):
        return 2*n+2
    def compare(self,a,b):
        return a - b > 0
    def exchange(self,i,j):
        A = self.A
        A[i],A[j] = A[j],A[i]
    def heapify(self,i):
        A = self.A
        l = self.left(i)
        r = self.right(i)
        if l < self.nelem and self.compare(A[l], A[i]):
            largest = l
        else:
            largest = i
        if r < self.nelem and self.compare(A[r], A[largest]):
            largest = r
        if largest != i:
            self.exchange(i,largest)
            self.heapify(largest)
            
class PrioNode:
    def __init__(self, key, n):
        self.ndx = 0
        self.n = n
        self.key = key
    def __repr__(self):
        return "(%d:%d,%d)" % (self.ndx,self.n, self.key)

class MaxQueue(Heap):
    def __init__(self):
        super().__init__()
    def compare(self,a,b):
        return a.key > b.key
    def exchange(self,i,j):
        A = self.A
        A[i].ndx = j
        A[j].ndx = i
        super().exchange(i,j)
    def update_key(self,i):
        parent = lambda x: self.parent(i)
        compare = lambda a,b: self.compare(a,b)
        A = self.A
        while i > 0 and not compare(A[parent(i)], A[i]):
            self.exchange(i,parent(i))
            i = parent(i)
    def increase_key(self,i,key):
        A = self.A
        if key < A[i].key:
            print ("Error")
            sys.exit(-1)
        A[i].key = key
        self.update_key(i)
    def insert(self,n):
        A = self.A
        while (len(A) < self.nelem):
            A.append(None)
        i = self.nelem
        A.append(None)
        self.nelem = self.nelem + 1
        A[i] = n
        A[i].ndx = i
        self.update_key(i)
    def extract(self):
        elem = self.A[0]
        self.exchange(0,self.nelem-1)
        self.nelem = self.nelem - 1
        self.heapify(0)
        return elem
    def is_empty(self):
        return self.nelem == 0

class MinQueue(MaxQueue):
    def __init__(self):
        super().__init__()
    def compare(self,a,b):
        return a.key < b.key
    def update_key(self,i):
        parent = lambda x: self.parent(i)
        A = self.A
        while i > 0 and not self.compare(A[parent(i)], A[i]):
            self.exchange(i,parent(i))
            i = parent(i)
    def decrease_key(self,i,key):
        A = self.A
        if key > A[i].key:
            print ("Error")
            sys.exit(-1)
        A[i].key = key
        self.update_key(i)
    def __repr__(self):
        return "%a %a" % (self.nelem,self.A)

class Adj:
    def __init__(self, n):
        self.n = n
        self.next = None

class Weight(Adj):
    def __init__(self, n, w):
        super().__init__(n)
        self.w = w

class Vertex:
    def __init__(self, name):
        self.parent = -1
        self.name = name
        self.n = 0
        self.first = None
    def add(self, v):
        a = Adj()
        a.n = v.n
        a.next = self.first
        self.first = a
    def copy(self, other):
        self.parent = other.parent
        self.name = other.name
        self.n = other.n
        self.first = other.first

class DijkVertex(Vertex):
    def __init__(self, name):
        super().__init__(name)
        self.d = INFTY
        self.priority = None
    def __repr__(self):
        return "(%a %a %a)" % (self.name,self.n,self.d)
    def add(self, v, w):
        a = Weight(v, w) 
        a.next = self.first
        self.first = a
    def set_priority(self,n):
        self.priority = n
    def decrease_key(self, q):
        prio = self.priority
        ndx = prio.ndx
        q.decrease_key(ndx, self.d)
        

class Dijkstra:
    def __init__(self):
        self.vertices = []
        self.q = MinQueue()
    def add_vertex(self,name):
        n = len(self.vertices)
        v = DijkVertex(name)
        v.n = n
        self.vertices.append(v)
        return v
    def get_vertex(self,name):
        for v in self.vertices:
            if v.name == name:
                return v
        return None        
    def print_vertex(self,n):
        print (self.vertices[n].name, end=' ')
        print (self.vertices[n].parent, end=' ')
        print (self.vertices[n].d, end=' ')
        p = self.vertices[n].first
        while p:
            print (p.n.name, end = ' ')
            print (p.w, end = ' ')
            p = p.next
        print('')
    def print_vertices(self):
        for i in range(len(self.vertices)):
            self.print_vertex(i)
    def relax(self, u):
        vset = self.vertices
        q = self.q
        p = u.first
        while p:
            v = p.n;
            d = u.d + p.w
            if d < v.d:
                v.d = d
                v.parent = u.n
                print(v)
                v.decrease_key(q)
            p = p.next
    def shortest_path(self):
        q = self.q
        vset = self.vertices
        for v in vset:
            n = PrioNode(v.d, v.n) 
            v.set_priority(n)
            q.insert(n)
        while not q.is_empty():
            u = q.extract()
            self.relax(vset[u.n])




import os
instruction = int(input(
"""0. Read data files
1. display statistics
2. Top 5 most tweeted words
3. Top 5 most tweeted users
4. Find users who tweeted a word (e.g., ’연세대’)
5. Find all people who are friends of the above users 
6. Delete users who mentioned a word
7. Delete all users who mentioned a word
8. Find strongly connected components 
9. Find shortest path from a given user (weight = number of friends)
99. Quit
Select Menu:
""").strip())



if instruction == 0:
    chdir = input("set current directory(Full path):")
    os.chdir(chdir)
    a = open("user.txt", encoding = 'UTF-8')
    b = open("friend.txt", encoding = 'UTF-8')
    c = open("word.txt", encoding = 'UTF-8')

    user_str = a.read()
    a.close()
    user_list = user_str.split("\n\n")

    user_numID = []
    for i in user_list:
        i_split = i.split('\n')
        user_numID.append((i_split[0],i_split[-1])) 


    con_str = b.read()
    b.close()
    con_list = con_str.split("\n\n")
    
    con_numID = []
    for i in con_list:
        i_split = i.split('\n')
        con_numID.append((i_split[0],i_split[-1])) 
        
    twt_str = c.read()
    c.close()
    twt_list = twt_str.split("\n\n")
    
    twt_numID = []
    for i in twt_list:
        i_split = i.split('\n')
        twt_numID.append((i_split[0],i_split[-1]))

    total_users = len(user_numID)
    total_frd = len(con_numID)
    total_twt = len(twt_numID)
    data_files = 'Total users: %s \nTotal friendship records: %s \nTotal tweets: %s' %(total_users, total_frd, total_twt)
    print(data_files)

    
elif instruction == 1: 
    
elif instruction == 2: 
    words = []
    for x,y in twt_numID:
        words.append(y)
    word_freq = {}
    for i in words:
        if i not in word_freq.keys():
            word_freq[i] = 1
        else:
            word_freq[i] += 1
    topUsers = sorted(word_freq, key=word_freq.get, reverse=True)
    twt_top5 = topUsers[0:5]
    print(twt_top5)
    
elif instruction == 3:
    users = []
    for x,y in twt_numID:
        users.append(x)
    user_freq = {}
    for i in users:
        if i not in user_freq.keys():
            user_freq[i] = 1
        else:
            user_freq[i] += 1
    topUsers = sorted(user_freq, key=user_freq.get, reverse=True)
    user_top5 = topUsers[0:5]
    print(user_top5)    

elif instruction == 4: 
    
elif instruction == 5:  

elif instruction == 6: 

elif instruction == 7: 

elif instruction == 8: 
    frd_vertices = []
    for i in con_numID:
        frd_DFS = DFS()
        a = DFSVertex(i[0])
        b = DFSVertex(i[-1])
        a.add(b)
        b.add(a)
        frd_vertices.append(a,b)
        frd_DFS.set_vertices(vertices)
elif instruction == 9: 
    given_user = input("given user:")
    for x,y in con_numID:
        g = Dijkstra()
        a = g.add_vertex(x)
        b = g.add_vertex(y)
        a.add(b,1)
        b.add(a,1)
    for i in g.vertices:
        if i == given_user:
            g.shortest_path()
            
elif instruction == 99:
