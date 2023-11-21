import json
from concurrent import futures

import grpc
import requests

import booking_pb2
import booking_pb2_grpc
import showtime_pb2
import showtime_pb2_grpc


# Client


def get_movies(stub, date):
    """
    Client calling the server to get the movies on a specific date
    :param stub: client stub
    :param date: string
    :return: void
    """
    movie = stub.GetMovies(date)
    print(movie)


def get_times(stub):
    """
    Client calling servicer to get the schedule
    :param stub: client stub
    :return: void
    """
    schedule = stub.GetTimes(showtime_pb2.Empty())
    for time in schedule:
        print("Date: %s  " % time.date)
        print("Movie: %s " % time.movies)


# Server


class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    def GetBookingByUserID(self, request, context):
        """
        Distant method that gets a user's bookings by passing his id as a parameter

        :param request:
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
        :return: stream BookingData
        """
        for booking in self.db:
            yield booking_pb2.BookingData(userid=booking['userid'], dates=booking['dates'])


    def AddBookingByUser(self, request, context):
        # Checking the validity of the booking (checking if
        # the movie is available at the requested date).
        time_req = requests.get("http://localhost:3202/showmovies/" + request.date)
        if not time_req.ok:
            return booking_pb2.Id(id="error : the booking's movie is not available at the requested date")
        else:
            user_found = False
            date_found = False
            movie_found = False

            # Checking if the user exists.
            for booking in self.db:
                if str(booking["userid"]) == str(request.userid):
                    user_found = True
                    # Checking if the booking's date exists.
                    for bk_date in booking["dates"]:
                        if str(bk_date["date"]) == str(request.date):
                            date_found = True
                            # Checking if the booking's movie exists.
                            for available_movie_id in bk_date["movies"]:
                                if str(available_movie_id) == str(request.movieid):
                                    movie_found = True
                                    return booking_pb2.Id(id="error : the requested movie is already booked by that user")

                            if not movie_found:
                                bk_date["movies"].append(request["movieid"])
                                return booking_pb2.Id(id="booking successfully added")

                    if not date_found:
                        # Adding new element to the "dates" list.
                        new_dict = {
                            'date': request.date,
                            'movies': [request.movieid]
                        }
                        booking["dates"].append(new_dict)
                        return booking_pb2.Id(id="booking successfully added")
            if not user_found:
                # Adding the user to the list of users that ordered, and
                # adding the booking to the user's list of bookings.
                new_dict = {
                    'date': request.date,
                    'movies': [request.movieid]
                }
                new_booking = {
                    'userid': request.userid,
                    'dates': [new_dict]
                }
                self.db.append(new_booking)
                return booking_pb2.Id(id="booking successfully added")

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
