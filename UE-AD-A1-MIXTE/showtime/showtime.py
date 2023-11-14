import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
import json


class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):
    """
    class that inherits from the generated showtime_pb2_grpc.ShowtimeServicer object. In this class we overload the
    constructor where we read the json file which will serve as our database.
    """
    def __init__(self):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]

    def GetMovies(self, request, context):
        """
        Distant method that gets the movies at a certain date that is indicated in the request body

        :param request:
        :param context:
        :return: ShowtimeData
        """
        for movie in self.db:
            if movie['date'] == request.date:
                print("Movie Found!")
                return showtime_pb2.ShowtimeData(date=movie['date'], movies=movie['movies'])
        return showtime_pb2.ShowtimeData(date="!not found!", movies="!not found!")

    def GetTimes(self, request, context):
        """
        Distant method that returns a list of strings that represents the movies in the database

        :param request:
        :param context:
        :return: String list
        """
        for time in self.db:
            yield showtime_pb2.ShowtimeData(date=time['date'], movies=time['movies'])


def serve():
    """
    main function that is in charge of creating the gRPC server and saving the ShowtimeServicer to this server
    Port: 3002
    :return:
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
