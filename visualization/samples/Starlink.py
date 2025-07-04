

import visualization.constellation_visualization as constellation_visualization



def Starlink():
    # 星座名称
    constellation_name = "Starlink"
    xml_file_path = "config/XML_constellation/" + constellation_name + ".xml"
    output_file_path = "visualization/CesiumAPP/"
    head_html_file = "visualization/html_head_tail/head.html"
    tail_html_file = "visualization/html_head_tail/tail.html"
    constellation_visualization.constellation_visualization(constellation_name, xml_file_path,
                                                            output_file_path,
                                                            head_html_file,
                                                            tail_html_file,
                                                            True)