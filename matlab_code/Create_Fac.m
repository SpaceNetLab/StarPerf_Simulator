function Create_Fac(conid)
disp('settings of Fac');
global No_fac Lat Long;
Long = [116.3 -74 -0.10 150.53];
Lat = [39.9 40.42 51.30 -33.55];
No_fac=length(Long);
for i=1:No_fac
    info_facility=strcat('Fac',num2str(i));
    stkNewObj('*/','Facility',info_facility);
    lat=Lat(i);
    long=Long(i);
    info_facility=strcat('Scenario/Matlab_Basic/Facility/',info_facility);
    stkSetFacPosLLA(info_facility, [lat*pi/180; long*pi/180; 0]);
    stkConnect(conid,'SetConstraint',info_facility,'ElevationAngle Min 20');
    num_fac(i)=i;
    
end
save('Num_fac.mat','num_fac');
end