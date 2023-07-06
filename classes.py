from threading import Timer

class Distance:
    node = None 
    distance = -1

    # estamos definindo a classe Distance com duas variáveis de instância: node e distance
    # O método __init__ é o construtor da classe Distance. Ele é chamado quando um objeto Distance é criado. 
    # Esse método recebe dois argumentos: node (representando o nó de destino) e distance (representando a distância até o nó de destino). 
    # Dentro do construtor, os valores recebidos são atribuídos às variáveis de instância self.node e self.distance
    def __init__(self, node, distance):
        """
        Classe que representa uma distância até um nó específico.

        Args:
            node (Node): O nó de destino.
            distance (int): A distância até o nó de destino.
        """
        self.node = node
        self.distance = distance

    # O método get_node é um método de acesso que retorna o nó de destino da distância. 
    # Ele não recebe nenhum argumento e retorna o valor da variável de instância self.node
    def get_node(self):
        """
        Obtém o nó de destino.

        Returns:
            Node: O nó de destino.
        """
        return self.node

    # O método get_distance é outro método de acesso que retorna a distância até o nó de destino. 
    # Ele não recebe nenhum argumento e retorna o valor da variável de instância self.distance.
    def get_distance(self):
        """
        Obtém a distância até o nó de destino.

        Returns:
            int: A distância até o nó de destino.
        """
        return self.distance

# Aqui, estamos definindo a classe Neighbor com duas variáveis de instância: node e pointed. 
# Ambas são inicializadas com valores padrão (None e False, respectivamente).
class Neighbor:
    node = None 
    pointed = False

# O método __init__ é o construtor da classe Neighbor. 
# Ele é chamado quando um objeto Neighbor é criado. 
# Esse método recebe dois argumentos: node (representando o nó vizinho) e pointed (um argumento opcional que indica se o vizinho está sendo apontado). 
# Por padrão, o valor de pointed é False. Dentro do construtor, os valores recebidos são atribuídos às variáveis de instância self.node e self.pointed
    def __init__(self, node, pointed=False):
        """
        Classe que representa um vizinho de um nó.

        Args:
            node (Node): O nó vizinho.
            pointed (bool, optional): Indica se o vizinho está sendo apontado. Default é False.
        """
        self.node = node
        self.pointed = pointed

    def get_id(self):
        """
        Obtém o ID do vizinho.

        Returns:
            int: O ID do vizinho.
        """
        return self.id

    def get_pointed(self):
        """
        Verifica se o vizinho está sendo apontado.

        Returns:
            bool: True se o vizinho está sendo apontado, False caso contrário.
        """
        return self.pointed

class Node:
    id = None 
    name = None 
    distances = [] 
    neighbors = [] 

    def __init__(self, id, name):
        """
        Classe que representa um nó.

        Args:
            id (int): O ID do nó.
            name (str): O nome do nó.
        """
        self.id = id
        self.name = name

    def get_id(self):
        """
        Obtém o ID do nó.

        Returns:
            int: O ID do nó.
        """
        return self.id

    def get_distances(self):
        """
        Obtém as distâncias do nó.

        Returns:
            list[Distance]: As distâncias do nó.
        """
        return self.distances

    def get_neighbors(self):
        """
        Obtém os vizinhos do nó.

        Returns:
            list[Neighbor]: Os vizinhos do nó.
        """
        return self.neighbors

    def set_distances(self, distances):
        """
        Define as distâncias do nó.

        Args:
            distances (list[Distance]): As distâncias do nó.
        """
        self.distances = distances

    def set_neighbors(self, neighbors):
        """
        Define os vizinhos do nó.

        Args:
            neighbors (list[Neighbor]): Os vizinhos do nó.
        """
        self.neighbors = neighbors

class MyTimer:
    timer = None
    duration = None 
    function = None 

    def __init__(self, duration, function):
        """
        Classe que representa um timer.

        Args:
            duration (float): A duração do timer.
            function (function): A função a ser executada quando o timer expirar.
        """
        self.timer = Timer(2.0, function)
        self.duration = duration
        self.function = function

    def resetTimer(self):

        """
        Reseta o timer, cancelando a contagem anterior e iniciando um novo timer.
        """
        self.timer.cancel()
        self.timer = Timer(self.duration, self.function)
        self.timer.start()
