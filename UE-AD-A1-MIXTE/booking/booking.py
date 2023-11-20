import json
from concurrent import futures

import grpc

import booking_pb2
import booking_pb2_grpc
import showtime_pb2
import showtime_pb2_grpc


def get_movies(stub, date):
    """
    Client calling the server to get the movies on a specific date
    :param stub: client stub
    :param date: string
    :return:
    """
    movie = stub.GetMovies(date)
    print(movie)


def get_times(stub):
    """
    Client calling servicer to get the schedule
    :param stub: client stub
    :return:
    """
    schedule = stub.GetTimes(showtime_pb2.Empty())
    for time in schedule:
        print("Date: %s  " % time.date)
        print("Movie: %s " % time.movies)


class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    def GetBookingByUserID(self, request, context):
        """
        Distant method that gets a user's bookings by passing his id as a parameter

        :param request: string
        :param context:
        :return: BookingData
        """
        print()
        print("---GetBookingByUserId---")
        for booking in self.db:
            if booking["userid"] == request.id:
                print("User Found")
                return booking_pb2.BookingData(userid=booking['userid'], dates=booking['dates'])
        return booking_pb2.BookingData(userid="!not found!", dates="!not found!")

    def GetBookings(self, request, context):
        """
        Distant procedure to get all the bookings in the DataBase
        :param request:
        :param context:
        :return: BookingData
        """
        for booking in self.db:
            yield booking_pb2.BookingData(userid=booking['userid'], dates=booking['dates'])

    with grpc.insecure_channel('localhost:3002') as channel:
        stub = showtime_pb2_grpc.ShowtimeStub(channel)

        print("-------------- GetMovies --------------")
        date = showtime_pb2.Date(date="20151202")
        get_movies(stub, date)

        print("-------------- GetTimes --------------")
        get_times(stub)

    channel.close()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3003')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
    # run()
