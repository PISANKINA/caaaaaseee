import random


def feedback(petrol, queue):
    [print('Автомат №{} максимальная очередь {} Марки бензина: {} -> {}'.format(station, petrol[station][0],petrol[station][1],'*' * len(queue[station]))) for station in petrol]
    print('\n')


def order(petrol, queue, time, data):
    var = []
    volume, fuel = int(data[time][0]), data[time][1]
    for station in petrol:
        if fuel in petrol[station][1]:
            var.append(station)
    for i in var:
        if len(queue[i]) == int(petrol[i][0]):
            var.remove(i)
    vol = volume
    if volume % 10:
        volume = int((volume // 10) * 10 + 10)
    volume += random.randrange(-10, 11, 10)
    time_to = int(volume / 10)
    if volume == 0:
        volume = 10
    if var == []:
        return 'В {} новый клиент: {} {} {} {} не смог заправить свой автомобиль и покинул АЗС'.format(time, time, fuel,
                                                                                                       vol, time_to)
    lst = [[i, len(queue[i])] for i in var]
    sorted(lst, key=lambda x: x[1])
    station = lst[0][0]
    queue[station].append([time, volume, fuel, time_to])
    return 'В {} новый клиент: {} {} {} {} встал в очередь к автомату {}'.format(time, time, fuel, vol, time_to,
                                                                                 station)


def timing(time, queue, data, petrol):
    time[1] += 1
    if time[1] == 60:
        time[1] = 0
        time[0] += 1
    if time[0] == 24:
        time[0] = -1
    time_out = '{:0>2}:{:0>2}'.format(time[0], time[1])
    for station in queue:
        if queue[station] != []:
            time_in, vol, fuel, time_to = queue[station][0]
            queue[station][0][1] -= 10
            if queue[station][0][1] == 0:
                queue[station] = []
                print('В {} клиент: {} {} {} {} заправил свой автомобиль и покинул АЗС'.format(time_out, time_in, fuel,
                                                                                               vol, time_to))
                feedback(petrol, queue)
    return time, queue, data


def stream(petrol, queue, data):
    time = [0, 0]
    while True:
        for item in data:
            if item == '{:0>2}:{:0>2}'.format(time[0], time[1]):
                print(order(petrol, queue, item, data))
                feedback(petrol, queue)
        timing(time, queue, data, petrol)
        if time[0] == -1:
            break


def main():
    with open('azs.txt', 'r') as azs:
        azs = azs.readlines()
    petrol = dict()
    queue = dict()
    for string in azs:
        number, max_queue, *fuel = string.split()
        queue.update({number: []})
        petrol.update({number: [max_queue, fuel]})
    with open('input.txt', 'r') as clients:
        clients = clients.readlines()
    data = dict()
    for client in clients:
        time, *item = client.split()
        data.update({time: item})
    stream(petrol, queue, data)


if __name__ == "__main__":
    main()
