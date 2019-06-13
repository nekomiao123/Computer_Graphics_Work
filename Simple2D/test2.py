import queue


if __name__ == "__main__":
    q = queue.Queue()
    #put是入队，get是出队
    for i in range(6):
        q.put(i)

    for i in range(5):
        print(q.get())

    #print(q.get())
    #print(q.empty())


