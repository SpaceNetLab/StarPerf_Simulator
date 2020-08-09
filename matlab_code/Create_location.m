function [position, position_cbf]=Create_location(dT)
global No_leo  No_fac tStart tStop No_snap Lat Long;
load('Num_leo.mat');
load('Num_fac.mat');
index=1;
position = cell(No_leo + No_fac,1);
position_cbf = cell(No_leo + No_fac,1);
for i=1:No_leo
    leo_info=strcat('*/Satellite/Sat',num2str(num_leo(i)));
    [secData, secName] = stkReport(leo_info,'LLA Position',tStart, tStop, dT);
    lat = stkFindData(secData{1}, 'Lat');
    long = stkFindData(secData{1}, 'Lon');
    alt = stkFindData(secData{1}, 'Alt');
    llapos = zeros(3,No_snap);%%[lat long high]'
    for j = 1:No_snap
        llapos(1,j) = llapos(1,j)+ lat(j)*180/pi;%%lat
        llapos(2,j) = llapos(2,j)+ long(j)*180/pi;%%long
        llapos(3,j) = llapos(3,j) + alt(j);
    end
    position{index} = llapos;
    position_cbf{index} = Lla2Cbf(position{index,1});
    index=index+1;
    
end
for i=1:No_fac
    llapos = zeros(3,No_snap);
    llapos(1,:) = llapos(1,:)+Lat(i);
    llapos(2,:) = llapos(2,:)+Long(i);
    position{index} = llapos;
    position_cbf{index} = Lla2Cbf(position{index,1});
    index=index+1;
end
end