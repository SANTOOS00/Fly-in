from edge import Edge
from hube import Hub




if __name__ == "__main__":

    edges =[]

    edg1 = Edge(Hub(name='santoos1',x=2,y=2), Hub(name='santoos11',x=2,y=2))
    edg2 = Edge(Hub(name='santoos2',x=2,y=2), Hub(name='santoos21',x=2,y=2))
    edg3 = Edge(Hub(name='santoos3',x=2,y=2), Hub(name='santoos31',x=2,y=2))
    edg4 = Edge(Hub(name='santoos4',x=2,y=2), Hub(name='santoos41',x=2,y=2))
    edg5 = Edge(Hub(name='santoos5',x=2,y=2), Hub(name='santoos51',x=2,y=2))
    edg6 = Edge(Hub(name='santoos6',x=2,y=2), Hub(name='santoos61',x=2,y=2))
    edg7 = Edge(Hub(name='santoos7',x=2,y=2), Hub(name='santoos71',x=2,y=2))
    edg8 = Edge(Hub(name='santoos8',x=2,y=2), Hub(name='santoos81',x=2,y=2))
    edg9 = Edge(Hub(name='santoos31',x=2,y=2), Hub(name='santoos23',x=2,y=2))


    edges.append(edg1)
    edges.append(edg2)
    edges.append(edg3)
    edges.append(edg4)
    edges.append(edg5)
    edges.append(edg6)
    edges.append(edg7)
    edges.append(edg8)
    # edges.append(edg9)
    print([len({eg.source, eg.destintion}) for eg in edges])
    if {edg9.source, edg9.destintion} in [{eg.source, eg.destintion} for eg in edges]:
        print("is ok")