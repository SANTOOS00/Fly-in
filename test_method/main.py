import heapq
import copy

def dijkstra(graph, source, sink):
    """
    حساب أقصر مسار باستخدام Dijkstra.
    ترجع قائمة العقد (Path) والتكلفة الإجمالية (Cost).
    """
    # priority queue: (cost, current_node, path)
    pq = [(0, source, [source])]
    visited = set()

    while pq:
        (cost, current, path) = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)

        if current == sink:
            return path, cost

        for neighbor, weight in graph.get(current, {}).items():
            if neighbor not in visited:
                heapq.heappush(pq, (cost + weight, neighbor, path + [neighbor]))

    return None, float('inf')


def get_path_cost(graph, path):
    """حساب التكلفة الإجمالية لمسار معين."""
    cost = 0
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        if u in graph and v in graph[u]:
            cost += graph[u][v]
        else:
            return float('inf')
    return cost


def yen_ksp(graph, source, sink, K):
    """
    تطبيق خوارزمية Yen's K-Shortest Paths.
    """
    # A كتحتفظ بالمسارات المقبولة الرسمية (A[0], A[1], ..., A[K-1])
    A = []
    
    # 1. إيجاد أقصر مسار أول (A[0])
    first_path, first_cost = dijkstra(graph, source, sink)
    if not first_path:
        return A  # لا يوجد أي مسار من source إلى sink
    
    A.append((first_path, first_cost))
    
    # B كتحتفظ بالمسارات المرشحة (Potential Paths)
    # كنخزنو فيها: (cost, path)
    B = []

    for k in range(1, K):
        # المسار المقبول السابق
        prev_path = A[k - 1][0]

        # كنمشيو على العقد من 0 حتى لقبل الأخيرة
        for i in range(len(prev_path) - 1):
            spur_node = prev_path[i]
            root_path = prev_path[:i + 1]

            # نديرو نسخة موقتة من الـ Graph باش نعدلو عليها
            working_graph = copy.deepcopy(graph)

            # 3. مسح الأضلاع الخارجه من spur_node اللي كيتشاركو فـ نفس root_path
            for path_data in A:
                p_path = path_data[0]
                if len(p_path) > i and root_path == p_path[:i + 1]:
                    u = p_path[i]
                    v = p_path[i + 1]
                    if u in working_graph and v in working_graph[u]:
                        del working_graph[u][v]

            # 4. مسح العقد اللي فـ root_path (من غير spur_node) باش نمنعو الـ Loops
            for node in root_path[:-1]:
                if node in working_graph:
                    del working_graph[node]
                    # مسح جميع الأضلاع اللي كتدخل لهاد العقدة من بقية العقد
                    for u in working_graph:
                        if node in working_graph[u]:
                            del working_graph[u][node]

            # حساب الـ Spur Path من spur_node لـ sink فالـ Graph المقتطع
            spur_path, _ = dijkstra(working_graph, spur_node, sink)

            # إذا لقينا spur_path نجمعوه مع root_path
            if spur_path:
                # root_path[:-1] + spur_path تجنب تكرار spur_node
                total_path = root_path[:-1] + spur_path
                total_cost = get_path_cost(graph, total_path)

                # التأكد أن المسار غير موجود فـ B ولا فـ A
                candidate = (total_cost, total_path)
                if candidate not in B and candidate not in A:
                    B.append(candidate)

        # إذا كانت B خاوية، يعني تسلاو المسارات الممكينة
        if not B:
            break

        # ترتيب B حسب الـ Cost واختيار الأقصر
        B.sort(key=lambda x: x[0])
        
        # إضافة أقصر مسار لـ A وحذفه من B
        shortest_candidate = B.pop(0)
        A.append(shortest_candidate)

    return A


graph = {
    'S': {'A': 2, 'B': 1, 'C': 3},
    'A': {'T': 3},
    'B': {'T': 4},
    'C': {'T': 1},
    'T': {}
}

paths = yen_ksp(graph, source='S', sink='T', K=3)

# طباعة النتائج:
for idx, (path, cost) in enumerate(paths):
    print(f"k = {idx + 1}: Path = {path}, Cost = {cost}")