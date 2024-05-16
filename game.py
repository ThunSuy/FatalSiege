class Game:
    def __init__(self, id):
        self.ready = False
        self.id = id
        self.health = [15, 15]

    def get_health(self):
        return self.health

    def check_health(self):
        return any(health == 0 for health in self.health)

    def reset_health(self):
        self.health = [15, 15]

    def current_health(self, player, current_health):
        self.health[player] = current_health

    def connected(self):
        """
        Kiểm tra trạng thái kết nối của trận đấu

        :return: Trạng thái kết nối (True hoặc False)
        """
        return self.ready

    def winner(self):
        if self.health[0] == 0:
            return 1
        elif self.health[1] == 0:
            return 0
