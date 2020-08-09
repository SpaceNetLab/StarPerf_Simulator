# -*- coding: UTF-8 -*-

#ground station location
class ground_segment_location:
    def __init__(self):
        self.id = 0;
        self.latitude = 0;
        self.longitude = 0;
        self.attitude = 0;


ground_station_points = [];

#(0)Phoenix, AZ
op_Phoenix = ground_segment_location();
op_Phoenix.id = "Phoenix-AZ-USA";
op_Phoenix.latitude = 33.41613888888889;
op_Phoenix.longitude = -112.00916666666667;
op_Phoenix.attitude = 0;
ground_station_points.append(op_Phoenix)

#(1)Fremont, CA
op_Fremont = ground_segment_location();
op_Fremont.id = "Fremont-CA-USA";
op_Fremont.latitude = 37.47247222222222;
op_Fremont.longitude = -121.92141666666667;
op_Fremont.attitude = 0;
ground_station_points.append(op_Fremont)

#(2)Roubaix, France
op_Roubaix = ground_segment_location();
op_Roubaix.id = "Roubaix-France";
op_Roubaix.latitude = 50.69277777777778;
op_Roubaix.longitude = 3.178111111111111;
op_Roubaix.attitude = 0;
ground_station_points.append(op_Roubaix)

#(3)Chizhevskogo, Kazakhstan
op_Chizhevskogo = ground_segment_location();
op_Chizhevskogo.id = "Chizhevskogo-Kazakhstan";
op_Chizhevskogo.latitude = 49.81733333333334;
op_Chizhevskogo.longitude = 73.09452777777777;
op_Chizhevskogo.attitude = 0;
ground_station_points.append(op_Chizhevskogo)

#(4)Chelyabinskaya-Russia
op_Chelyabinskaya = ground_segment_location();
op_Chelyabinskaya.id = "Chelyabinskaya-Russia";
op_Chelyabinskaya.latitude = 55.16558333333333;
op_Chelyabinskaya.longitude = 61.433499999999995;
op_Chelyabinskaya.attitude = 0;
ground_station_points.append(op_Chelyabinskaya)

#(5)Johannesburg-South-Africa
op_Johannesburg = ground_segment_location();
op_Johannesburg.id = "Johannesburg-South-Africa";
op_Johannesburg.latitude = -26.18691666666667;
op_Johannesburg.longitude = 28.04363888888889;
op_Johannesburg.attitude = 0;
ground_station_points.append(op_Johannesburg)

#(6)Athanasios-Cyprus
op_Athanasios = ground_segment_location();
op_Athanasios.id = "Athanasios-Cyprus";
op_Athanasios.latitude = 34.70727777777778;
op_Athanasios.longitude = 33.06386111111111;
op_Athanasios.attitude = 0;
ground_station_points.append(op_Athanasios)
