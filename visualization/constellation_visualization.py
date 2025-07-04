
import xml.etree.ElementTree as ET
import math
import ephem






def add_coverage_circle(satellite, coverage_radius, color="BLUE"):
    """
    添加覆盖范围的圆形
    :param satellite: 卫星对象
    :param coverage_radius: 覆盖范围半径
    :param color: 圆形颜色
    :return: JavaScript代码字符串
    """
    return "var coverageCircle = viewer.entities.add({name : '', position: Cesium.Cartesian3.fromDegrees(" \
           + str(math.degrees(satellite.sublong)) + ", " \
           + str(math.degrees(satellite.sublat)) + ", 0), " \
           + "ellipse : {semiMajorAxis : " + str(coverage_radius) + ", semiMinorAxis : " + str(coverage_radius) + ", " \
           + "material : Cesium.Color." + color + ".withAlpha(0.2),}});\n"







# 该函数用来获取卫星对象列表
def get_satellites_list(
        mean_motion,  # 平均运动率，即卫星每天围绕地球转动的次数
        altitude,
        number_of_orbit,
        number_of_satellite_per_orbit,
        inclination,
        phase_shift = True,  # 相邻轨道之间的相位差
        eccentricity = 0.0000001,  # 轨道偏心率
        arg_perigee = 0.0,   # 轨道近地点角
        epoch = "1949-10-01 00:00:00" # 基准时间
        ):
    satellites = [None] * (number_of_orbit * number_of_satellite_per_orbit)
    count = 0
    sat_id = 1
    for orbit in range(0, number_of_orbit):
        raan = orbit * 360 / number_of_orbit
        orbit_wise_shift = 0
        if orbit % 2 == 1:
            if phase_shift:
                orbit_wise_shift = 360 / (number_of_satellite_per_orbit * 2)

        for n_sat in range(0, number_of_satellite_per_orbit):
            mean_anomaly = orbit_wise_shift + (n_sat * 360 / number_of_satellite_per_orbit)

            sat = ephem.EarthSatellite()  # 生成卫星对象
            sat._epoch = epoch  # 设置卫星基准时间
            sat._inc = ephem.degrees(inclination)  # 设置卫星的轨道倾角
            sat._e = eccentricity  # 轨道偏心率
            sat._raan = ephem.degrees(raan)  # 升交点赤经
            sat._ap = arg_perigee  # 轨道近地点角
            sat._M = ephem.degrees(mean_anomaly)  # 卫星在轨道内相对近地点的偏移角度，即轨内偏移
            sat._n = mean_motion  # 平均运动率

            satellites[count] = {
                "satellite": sat,
                "altitude": altitude,
                "orbit": orbit,
                "orbit_satellite_id": n_sat,
                "sat_id":sat_id
            }
            sat_id += 1
            count += 1

    return satellites




# 获取卫星的临近卫星
def get_neighbor_satellite(
        sat1_orb,sat1_rel_id,sat2_orb,sat2_rel_id,satellite,
        number_of_orbit, number_of_satellite_per_orbit):
    neighbor_abs_orb = (sat1_orb + sat2_orb) % number_of_orbit
    neighbor_abs_pos = (sat1_rel_id + sat2_rel_id) % number_of_satellite_per_orbit
    sel_sat_id = -1
    for i in range(0, len(satellite)):
        if (satellite[i]["orbit"] == neighbor_abs_orb and
                satellite[i]["orbit_satellite_id"] == neighbor_abs_pos):
            sel_sat_id = i
            break
    return sel_sat_id





# 获取卫星之间的ISL
def get_ISL(satellite, number_of_orbit, number_of_satellite_per_orbit):
    links = {}
    count = 0
    for i in range(0, len(satellite)):
        sel_sat_id = get_neighbor_satellite(satellite[i]["orbit"],
                                            satellite[i]["orbit_satellite_id"],
                                            0, 1, satellite,
                                            number_of_orbit, number_of_satellite_per_orbit)
        links[count] = {
            "sat1": i,
            "sat2": sel_sat_id,
            "dist": -1.0
        }
        count += 1
    return links


def xml_to_dict(element):
    if len(element) == 0:
        return element.text
    result = {}
    for child in element:
        child_data = xml_to_dict(child)
        if child.tag in result:
            if type(result[child.tag]) is list:
                result[child.tag].append(child_data)
            else:
                result[child.tag] = [result[child.tag], child_data]
        else:
            result[child.tag] = child_data
    return result

def read_xml_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return {root.tag: xml_to_dict(root)}





def visualization_constellation_without_ISL(constellation_information, satellite_color = "BLACK", coverage_radius = 500000):

    content_string = ""
    for shell in constellation_information:

        mean_motion_rev_per_day = shell[0]
        altitude = shell[1]
        number_of_orbit = shell[2]
        number_of_satellite_per_orbit = shell[3]
        inclination = shell[4]
        base_id = shell[5]



        satellites = get_satellites_list(mean_motion_rev_per_day,altitude,number_of_orbit
                                         ,number_of_satellite_per_orbit,inclination)

        for j in range(len(satellites)):
            satellites[j]["satellite"].compute("1949-10-01 00:00:00")
            content_string += "var redSphere = viewer.entities.add({name : '', position: Cesium.Cartesian3.fromDegrees(" \
                        + str(math.degrees(satellites[j]["satellite"].sublong)) + ", " \
                        + str(math.degrees(satellites[j]["satellite"].sublat)) + ", " + str(
                satellites[j]["altitude"] * 1000) + "), " \
                        + "ellipsoid : {radii : new Cesium.Cartesian3(30000.0, 30000.0, 30000.0), " \
                        + "material : Cesium.Color." + satellite_color + ".withAlpha(1),}});\n"
            # 调用封装的覆盖范围函数
            content_string += add_coverage_circle(satellites[j]["satellite"], coverage_radius, satellite_color)
    return content_string



def visualization_constellation_with_ISL(constellation_information):
    content_string = ""
    count = 0
    for shell in constellation_information:
        mean_motion_rev_per_day = shell[0]
        altitude = shell[1]
        number_of_orbit = shell[2]
        number_of_satellite_per_orbit = shell[3]
        inclination = shell[4]
        base_id = shell[5]

        satellites = get_satellites_list(mean_motion_rev_per_day, altitude, number_of_orbit
                                         , number_of_satellite_per_orbit, inclination)



        sat_id=1
        flag=1
        for j in range(len(satellites)):
            satellites[j]["satellite"].compute("1949-10-01 00:00:00")
            if flag==1:
                content_string += (
                    "var redSphere = viewer.entities.add({name : '', position: Cesium.Cartesian3.fromDegrees(" \
                    + str(math.degrees(satellites[j]["satellite"].sublong)) + ", " \
                    + str(math.degrees(satellites[j]["satellite"].sublat)) + ", "
                    + str(satellites[j]["altitude"] * 1000) + "), " \
                    + "ellipsoid : {radii : new Cesium.Cartesian3(30000.0, 30000.0, 30000.0), " \
                    + "material : Cesium.Color.BLACK.withAlpha(1),}});\n")
                flag += 1
            elif flag==2:
                content_string += (
                        "var redSphere = viewer.entities.add({name : '', position: Cesium.Cartesian3.fromDegrees(" \
                        + str(math.degrees(satellites[j]["satellite"].sublong)) + ", " \
                        + str(math.degrees(satellites[j]["satellite"].sublat)) + ", "
                        + str(satellites[j]["altitude"] * 1000) + "), " \
                        + "ellipsoid : {radii : new Cesium.Cartesian3(30000.0, 30000.0, 30000.0), " \
                        + "material : Cesium.Color.BLACK.withAlpha(0),}});\n")
                flag += 1
            elif flag == 3:
                content_string += (
                        "var redSphere = viewer.entities.add({name : '', position: Cesium.Cartesian3.fromDegrees(" \
                        + str(math.degrees(satellites[j]["satellite"].sublong)) + ", " \
                        + str(math.degrees(satellites[j]["satellite"].sublat)) + ", "
                        + str(satellites[j]["altitude"] * 1000) + "), " \
                        + "ellipsoid : {radii : new Cesium.Cartesian3(30000.0, 30000.0, 30000.0), " \
                        + "material : Cesium.Color.BLACK.withAlpha(0),}});\n")
                flag = 1



            sat_id += 1

        orbit_links = get_ISL(satellites, number_of_orbit, number_of_satellite_per_orbit)
        # Starlink color = ['AQUA', 'BLUE', 'MEDIUMAQUAMARINE', 'RED','YELLOW']
        # Kuiper color = ['MEDIUMVIOLETRED','ORANGE','YELLOW','LIGHTCORAL']
        # Telesat color = ['GREEN', 'DEEPSKYBLUE', 'LAWNGREEN', 'MEDIUMSEAGREEN']
        color = ['MEDIUMVIOLETRED','ORANGERED','RED','PALEVIOLETRED']

        for key in orbit_links:
            sat1 = orbit_links[key]["sat1"]
            sat2 = orbit_links[key]["sat2"]
            content_string += (
                    "viewer.entities.add({name : '', polyline: { positions: Cesium.Cartesian3.fromDegreesArrayHeights([" \
                    + str(math.degrees(satellites[sat1]["satellite"].sublong)) + "," \
                    + str(math.degrees(satellites[sat1]["satellite"].sublat)) + "," \
                    + str(satellites[sat1]["altitude"] * 1000) + "," \
                    + str(math.degrees(satellites[sat2]["satellite"].sublong)) + "," \
                    + str(math.degrees(satellites[sat2]["satellite"].sublat)) + "," \
                    + str(satellites[sat2]["altitude"] * 1000) + "]), " \
                    + "width: 2, arcType: Cesium.ArcType.NONE, " \
                    + "material: new Cesium.PolylineOutlineMaterialProperty({ " \
                    + "color: Cesium.Color." + color[count]
                    + ".withAlpha(0.4), outlineWidth: 0, outlineColor: Cesium.Color.BLACK})}});")
        count += 1
    return content_string


# ISL参数是一个布尔变量，用来控制是否可视化ISL
def constellation_visualization(constellation_name , xml_file_path ,output_file_path,
                                head_html_file , tail_html_file ,ISL = False, satellite_color = "BLACK", coverage_radius = 500000):


    # 读取星座配置信息
    constellation_configuration_information = read_xml_file(xml_file_path)
    # 卫星层数量
    number_of_shells = int(constellation_configuration_information['constellation']['number_of_shells'])

    constellation_information = []
    for count in range(1, number_of_shells + 1, 1):
        altitude = int(constellation_configuration_information['constellation']['shell' + str(count)]['altitude'])
        orbit_cycle = int(constellation_configuration_information['constellation']['shell' + str(count)]['orbit_cycle'])
        inclination = float(
            constellation_configuration_information['constellation']['shell' + str(count)]['inclination'])
        number_of_orbit = int(
            constellation_configuration_information['constellation']['shell' + str(count)]['number_of_orbit'])
        number_of_satellite_per_orbit = int(
            constellation_configuration_information['constellation']['shell' + str(count)]
            ['number_of_satellite_per_orbit'])

        # 平均运动率，即卫星每天围绕地球转动的次数，计算方法是用卫星轨道周期的秒数除以一天总共的秒数（24*60*60=86400）
        mean_motion_rev_per_day = 1.0 * 86400 / orbit_cycle

        constellation_information.append(
            [mean_motion_rev_per_day, altitude, number_of_orbit, number_of_satellite_per_orbit,
             inclination])

    # 向每一层信息中添加base_id信息，即每一层第一颗卫星的编号
    for index in range(len(constellation_information)):
        if index == 0:
            constellation_information[index].append(0)
        else:
            constellation_information[index].append(constellation_information[index - 1][5] +
                                                    constellation_information[index - 1][2] *
                                                    constellation_information[index - 1][3])


    if ISL:
        # 可视化星座中的卫星和ISL
        visualization_content = visualization_constellation_with_ISL(constellation_information)
        writer_html = open(output_file_path + constellation_name + "_with_ISL.html", 'w')
        with open(head_html_file, 'r') as fi:
            writer_html.write(fi.read())
        writer_html.write(visualization_content)
        with open(tail_html_file, 'r') as fb:
            writer_html.write(fb.read())
        writer_html.close()
    else:
        # 只可视化星座中的卫星，不可视化ISL
        visualization_content = visualization_constellation_without_ISL(constellation_information, satellite_color, coverage_radius)
        writer_html = open(output_file_path + constellation_name + "_without_ISL.html", 'w')
        with open(head_html_file, 'r') as fi:
            writer_html.write(fi.read())
        writer_html.write(visualization_content)
        with open(tail_html_file, 'r') as fb:
            writer_html.write(fb.read())
        writer_html.close()


def visualization_example():
    constellation_name = "Telesat"
    xml_file_path = "./config/XML_constellation/" + constellation_name + ".xml"
    output_file_path = "./visualization/CesiumAPP/"
    head_html_file = "./visualization/html_head_tail/head.html"
    tail_html_file = "./visualization/html_head_tail/tail.html"
    constellation_visualization(constellation_name, xml_file_path, output_file_path,
                                head_html_file, tail_html_file, False, satellite_color="RED", coverage_radius=600000)


if __name__ == '__main__':
    visualization_example()
