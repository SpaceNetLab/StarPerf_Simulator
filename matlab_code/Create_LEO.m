function Create_LEO(conid,path)
    global No_leo cycle No_snap tStop constellation dT;
    parameter = readtable(path);
    parameter = parameter.Value;
    constellation = parameter{1,1};
    Altitude = str2num(parameter{2,1});
    cycle = str2num(parameter{3,1});
    No_snap = floor(cycle/dT)+1;
    tStop = cycle;
    dtr = pi/180;
    inc = str2num(parameter{4,1})*dtr;
    F = str2num(parameter{5,1});
    leo_plane = str2num(parameter{6,1});
    no = str2num(parameter{7,1});
    if (str2num(parameter{4,1}) > 80) && (str2num(parameter{4,1}) < 100)
        raan=[0:180/leo_plane:180/leo_plane*(leo_plane-1)];
    else
        raan=[0:360/leo_plane:360/leo_plane*(leo_plane-1)];
    end
    meanAnomaly1 = [0:360/no:360/no*(no-1)];
    raan = raan.*dtr;
    No_leo = leo_plane*no;
    disp('LEO:');
    disp(No_leo);
    for i =1:leo_plane
        for j=1:no
            ra = raan(i);
            ma = (mod(meanAnomaly1(j) + 360*F/(leo_plane*no)*(i-1),360))*dtr;
            num = j+no*(i-1);%%index of satellite-ID
            sat_no = strcat('Sat',num2str(num));
            stkNewObj('*/','Satellite',sat_no);
            sat_no = strcat('*/Satellite/',sat_no);
            stkSetPropClassical(sat_no,'J4Perturbation','J2000',0.0,tStop,dT,0,6731000 + Altitude * 10^3,0.0,inc,0.0,ra,ma);
            num_leo(num) = num;
        end
    end
    save('Num_leo.mat','num_leo','leo_plane');
    mkdir(strcat(constellation,'\\delay'))
end


