for key, values in dict.items():

main(jimmi='boy', amy='girl', john='trans'):

class Person:
    def __init__(self, **properties):
        for key, value in properties.items():
            setattr(self, key, value)

x = Person('Jhonny')
x.age = 20
{
    'jimmy':'boy',
    'amy':'girl'
}

packet = {
    'type': 'game_state_header',
    'positon': [430, 320],
    
}

def create_packet(self, type, player_data):
    packet = {'type':' '}
    for player, data in player_data:
        packet[player] = data