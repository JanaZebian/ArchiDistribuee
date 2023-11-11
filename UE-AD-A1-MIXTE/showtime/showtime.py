import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
import json

class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):

    def __init__(self):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]

    def GetMovies(self, request, context):
        for movie in self.db:
            if movie['date'] == request.date:
                print("Movie Found!")
                return showtime_pb2.ShowtimeData(date=movie['date'], movies=movie['movies'])
        return showtime_pb2.ShowtimeData(date="!not found!", movies="!not found!")
    def GetTimes(self, request, context):
        for time in self.db:
            yield showtime_pb2.ShowtimeData(date=time['date'], movies=time['movies'])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
