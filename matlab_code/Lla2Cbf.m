function position_cbf=Lla2Cbf(position)
%load('satData.mat');
R=6371*10^3;
%     No=length(position);
%     position_cbf=cell(No,1);
%     for s=1:No
%         tmp_pos=position{s};
%         r=R+ tmp_pos(3,:);% Altitude in m above the earth
%         Theta=pi/2-tmp_pos(1,:);
%         Phi=2*pi+tmp_pos(2,:);
%         X=(r.*sin(Theta)).*cos(Phi);
%         Y=(r.*sin(Theta)).*sin(Phi);
%         Z=r.*cos(Theta);
%         position_cbf{s}=[X; Y; Z];
%     end
%     position_cbf{1}(:,1:100);
%     position_cbf{2}(:,1:100);

r=R+ position(3,:);% Altitude in m above the earth
Theta=pi/2-position(1,:)*pi/180;
Phi=2*pi+position(2,:)*pi/180;
X=(r.*sin(Theta)).*cos(Phi);
Y=(r.*sin(Theta)).*sin(Phi);
Z=r.*cos(Theta);
position_cbf=[X; Y; Z];
end
