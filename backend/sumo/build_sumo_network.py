"""
Generates the CityLink 4-zone SUMO network file: citylink.net.xml
Contains:
- 16 Junctions with Traffic Light Logic (TLS)
- Multi-lane edges with sidewalks for pedestrians
- Connecting expressway corridors
"""

import os

net_xml_path = os.path.join(os.path.dirname(__file__), "network", "citylink.net.xml")

content = """<net version="1.16" junctionCornerDetail="5" limitTurnSpeed="5.50" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/net_file.xsd">
    <location netOffset="120.00,120.00" convBoundary="0.00,0.00,240.00,240.00" origBoundary="-120.00,-120.00,120.00,120.00" projParameter="!"/>

    <!-- Edge Types -->
    <type id="urban.2lane" numLanes="2" speed="13.89"/>
    <type id="urban.3lane" numLanes="3" speed="16.67"/>

    <!-- Nodes / Junctions -->
    <!-- Zone A: Koramangala -->
    <junction id="J_KOR_1" type="traffic_light" x="0.0" y="240.0" incLanes="E_KOR_4_0 E_KOR_4_1" intLanes="" shape="0,240"/>
    <junction id="J_KOR_2" type="traffic_light" x="80.0" y="240.0" incLanes="E_KOR_1_0 E_KOR_1_1" intLanes="" shape="80,240"/>
    <junction id="J_KOR_3" type="traffic_light" x="0.0" y="160.0" incLanes="E_KOR_3_0 E_KOR_3_1" intLanes="" shape="0,160"/>
    <junction id="J_KOR_4" type="traffic_light" x="80.0" y="160.0" incLanes="E_KOR_2_0 E_KOR_2_1" intLanes="" shape="80,160"/>

    <!-- Zone B: HSR Layout -->
    <junction id="J_HSR_1" type="traffic_light" x="160.0" y="240.0" incLanes="E_HSR_4_0 E_HSR_4_1" intLanes="" shape="160,240"/>
    <junction id="J_HSR_2" type="traffic_light" x="240.0" y="240.0" incLanes="E_HSR_1_0 E_HSR_1_1" intLanes="" shape="240,240"/>
    <junction id="J_HSR_3" type="traffic_light" x="160.0" y="160.0" incLanes="E_HSR_3_0 E_HSR_3_1" intLanes="" shape="160,160"/>
    <junction id="J_HSR_4" type="traffic_light" x="240.0" y="160.0" incLanes="E_HSR_2_0 E_HSR_2_1" intLanes="" shape="240,160"/>

    <!-- Zone C: Bellandur -->
    <junction id="J_BEL_1" type="traffic_light" x="160.0" y="80.0" incLanes="E_BEL_4_0 E_BEL_4_1" intLanes="" shape="160,80"/>
    <junction id="J_BEL_2" type="traffic_light" x="240.0" y="80.0" incLanes="E_BEL_1_0 E_BEL_1_1" intLanes="" shape="240,80"/>
    <junction id="J_BEL_3" type="traffic_light" x="160.0" y="0.0" incLanes="E_BEL_3_0 E_BEL_3_1" intLanes="" shape="160,0"/>
    <junction id="J_BEL_4" type="traffic_light" x="240.0" y="0.0" incLanes="E_BEL_2_0 E_BEL_2_1" intLanes="" shape="240,0"/>

    <!-- Zone D: Silk Board -->
    <junction id="J_SLK_1" type="traffic_light" x="0.0" y="80.0" incLanes="E_SLK_4_0 E_SLK_4_1" intLanes="" shape="0,80"/>
    <junction id="J_SLK_2" type="traffic_light" x="80.0" y="80.0" incLanes="E_SLK_1_0 E_SLK_1_1" intLanes="" shape="80,80"/>
    <junction id="J_SLK_3" type="traffic_light" x="0.0" y="0.0" incLanes="E_SLK_3_0 E_SLK_3_1" intLanes="" shape="0,0"/>
    <junction id="J_SLK_4" type="traffic_light" x="80.0" y="0.0" incLanes="E_SLK_2_0 E_SLK_2_1" intLanes="" shape="80,0"/>

    <!-- Edges with Lanes and Sidewalks -->
    <!-- Koramangala Internal Edges -->
    <edge id="E_KOR_1" from="J_KOR_1" to="J_KOR_2" priority="2" numLanes="3" speed="13.89">
        <lane id="E_KOR_1_0" index="0" allow="pedestrian" width="2.00" speed="1.40" length="80.00"/>
        <lane id="E_KOR_1_1" index="1" disallow="pedestrian" speed="13.89" length="80.00"/>
        <lane id="E_KOR_1_2" index="2" disallow="pedestrian" speed="13.89" length="80.00"/>
    </edge>
    <edge id="E_KOR_2" from="J_KOR_2" to="J_KOR_4" priority="2" numLanes="3" speed="13.89">
        <lane id="E_KOR_2_0" index="0" allow="pedestrian" width="2.00" speed="1.40" length="80.00"/>
        <lane id="E_KOR_2_1" index="1" disallow="pedestrian" speed="13.89" length="80.00"/>
        <lane id="E_KOR_2_2" index="2" disallow="pedestrian" speed="13.89" length="80.00"/>
    </edge>
    <edge id="E_KOR_3" from="J_KOR_4" to="J_KOR_3" priority="2" numLanes="3" speed="13.89">
        <lane id="E_KOR_3_0" index="0" allow="pedestrian" width="2.00" speed="1.40" length="80.00"/>
        <lane id="E_KOR_3_1" index="1" disallow="pedestrian" speed="13.89" length="80.00"/>
        <lane id="E_KOR_3_2" index="2" disallow="pedestrian" speed="13.89" length="80.00"/>
    </edge>
    <edge id="E_KOR_4" from="J_KOR_3" to="J_KOR_1" priority="2" numLanes="3" speed="13.89">
        <lane id="E_KOR_4_0" index="0" allow="pedestrian" width="2.00" speed="1.40" length="80.00"/>
        <lane id="E_KOR_4_1" index="1" disallow="pedestrian" speed="13.89" length="80.00"/>
        <lane id="E_KOR_4_2" index="2" disallow="pedestrian" speed="13.89" length="80.00"/>
    </edge>

    <!-- HSR Layout Internal Edges -->
    <edge id="E_HSR_1" from="J_HSR_1" to="J_HSR_2" priority="2" numLanes="3" speed="13.89">
        <lane id="E_HSR_1_0" index="0" allow="pedestrian" width="2.00" speed="1.40" length="80.00"/>
        <lane id="E_HSR_1_1" index="1" disallow="pedestrian" speed="13.89" length="80.00"/>
        <lane id="E_HSR_1_2" index="2" disallow="pedestrian" speed="13.89" length="80.00"/>
    </edge>
    <edge id="E_HSR_2" from="J_HSR_2" to="J_HSR_4" priority="2" numLanes="3" speed="13.89">
        <lane id="E_HSR_2_0" index="0" allow="pedestrian" width="2.00" speed="1.40" length="80.00"/>
        <lane id="E_HSR_2_1" index="1" disallow="pedestrian" speed="13.89" length="80.00"/>
        <lane id="E_HSR_2_2" index="2" disallow="pedestrian" speed="13.89" length="80.00"/>
    </edge>
    <edge id="E_HSR_3" from="J_HSR_4" to="J_HSR_3" priority="2" numLanes="3" speed="13.89">
        <lane id="E_HSR_3_0" index="0" allow="pedestrian" width="2.00" speed="1.40" length="80.00"/>
        <lane id="E_HSR_3_1" index="1" disallow="pedestrian" speed="13.89" length="80.00"/>
        <lane id="E_HSR_3_2" index="2" disallow="pedestrian" speed="13.89" length="80.00"/>
    </edge>
    <edge id="E_HSR_4" from="J_HSR_3" to="J_HSR_1" priority="2" numLanes="3" speed="13.89">
        <lane id="E_HSR_4_0" index="0" allow="pedestrian" width="2.00" speed="1.40" length="80.00"/>
        <lane id="E_HSR_4_1" index="1" disallow="pedestrian" speed="13.89" length="80.00"/>
        <lane id="E_HSR_4_2" index="2" disallow="pedestrian" speed="13.89" length="80.00"/>
    </edge>

    <!-- Bellandur Internal Edges -->
    <edge id="E_BEL_1" from="J_BEL_1" to="J_BEL_2" priority="2" numLanes="3" speed="13.89">
        <lane id="E_BEL_1_0" index="0" allow="pedestrian" width="2.00" speed="1.40" length="80.00"/>
        <lane id="E_BEL_1_1" index="1" disallow="pedestrian" speed="13.89" length="80.00"/>
        <lane id="E_BEL_1_2" index="2" disallow="pedestrian" speed="13.89" length="80.00"/>
    </edge>
    <edge id="E_BEL_2" from="J_BEL_2" to="J_BEL_4" priority="2" numLanes="3" speed="13.89">
        <lane id="E_BEL_2_0" index="0" allow="pedestrian" width="2.00" speed="1.40" length="80.00"/>
        <lane id="E_BEL_2_1" index="1" disallow="pedestrian" speed="13.89" length="80.00"/>
        <lane id="E_BEL_2_2" index="2" disallow="pedestrian" speed="13.89" length="80.00"/>
    </edge>
    <edge id="E_BEL_3" from="J_BEL_4" to="J_BEL_3" priority="2" numLanes="3" speed="13.89">
        <lane id="E_BEL_3_0" index="0" allow="pedestrian" width="2.00" speed="1.40" length="80.00"/>
        <lane id="E_BEL_3_1" index="1" disallow="pedestrian" speed="13.89" length="80.00"/>
        <lane id="E_BEL_3_2" index="2" disallow="pedestrian" speed="13.89" length="80.00"/>
    </edge>
    <edge id="E_BEL_4" from="J_BEL_3" to="J_BEL_1" priority="2" numLanes="3" speed="13.89">
        <lane id="E_BEL_4_0" index="0" allow="pedestrian" width="2.00" speed="1.40" length="80.00"/>
        <lane id="E_BEL_4_1" index="1" disallow="pedestrian" speed="13.89" length="80.00"/>
        <lane id="E_BEL_4_2" index="2" disallow="pedestrian" speed="13.89" length="80.00"/>
    </edge>

    <!-- Silk Board Internal Edges -->
    <edge id="E_SLK_1" from="J_SLK_1" to="J_SLK_2" priority="2" numLanes="3" speed="13.89">
        <lane id="E_SLK_1_0" index="0" allow="pedestrian" width="2.00" speed="1.40" length="80.00"/>
        <lane id="E_SLK_1_1" index="1" disallow="pedestrian" speed="13.89" length="80.00"/>
        <lane id="E_SLK_1_2" index="2" disallow="pedestrian" speed="13.89" length="80.00"/>
    </edge>
    <edge id="E_SLK_2" from="J_SLK_2" to="J_SLK_4" priority="2" numLanes="3" speed="13.89">
        <lane id="E_SLK_2_0" index="0" allow="pedestrian" width="2.00" speed="1.40" length="80.00"/>
        <lane id="E_SLK_2_1" index="1" disallow="pedestrian" speed="13.89" length="80.00"/>
        <lane id="E_SLK_2_2" index="2" disallow="pedestrian" speed="13.89" length="80.00"/>
    </edge>
    <edge id="E_SLK_3" from="J_SLK_4" to="J_SLK_3" priority="2" numLanes="3" speed="13.89">
        <lane id="E_SLK_3_0" index="0" allow="pedestrian" width="2.00" speed="1.40" length="80.00"/>
        <lane id="E_SLK_3_1" index="1" disallow="pedestrian" speed="13.89" length="80.00"/>
        <lane id="E_SLK_3_2" index="2" disallow="pedestrian" speed="13.89" length="80.00"/>
    </edge>
    <edge id="E_SLK_4" from="J_SLK_3" to="J_SLK_1" priority="2" numLanes="3" speed="13.89">
        <lane id="E_SLK_4_0" index="0" allow="pedestrian" width="2.00" speed="1.40" length="80.00"/>
        <lane id="E_SLK_4_1" index="1" disallow="pedestrian" speed="13.89" length="80.00"/>
        <lane id="E_SLK_4_2" index="2" disallow="pedestrian" speed="13.89" length="80.00"/>
    </edge>

    <!-- Inter-Zone Arterial Connectors -->
    <edge id="E_INTER_HSR_KOR" from="J_HSR_1" to="J_KOR_2" priority="3" numLanes="3" speed="16.67">
        <lane id="E_INTER_HSR_KOR_0" index="0" allow="pedestrian" width="2.00" speed="1.40" length="80.00"/>
        <lane id="E_INTER_HSR_KOR_1" index="1" disallow="pedestrian" speed="16.67" length="80.00"/>
        <lane id="E_INTER_HSR_KOR_2" index="2" disallow="pedestrian" speed="16.67" length="80.00"/>
    </edge>
    <edge id="E_INTER_BEL_HSR" from="J_BEL_1" to="J_HSR_3" priority="3" numLanes="3" speed="16.67">
        <lane id="E_INTER_BEL_HSR_0" index="0" allow="pedestrian" width="2.00" speed="1.40" length="80.00"/>
        <lane id="E_INTER_BEL_HSR_1" index="1" disallow="pedestrian" speed="16.67" length="80.00"/>
        <lane id="E_INTER_BEL_HSR_2" index="2" disallow="pedestrian" speed="16.67" length="80.00"/>
    </edge>
    <edge id="E_INTER_SLK_BEL" from="J_SLK_2" to="J_BEL_3" priority="3" numLanes="3" speed="16.67">
        <lane id="E_INTER_SLK_BEL_0" index="0" allow="pedestrian" width="2.00" speed="1.40" length="80.00"/>
        <lane id="E_INTER_SLK_BEL_1" index="1" disallow="pedestrian" speed="16.67" length="80.00"/>
        <lane id="E_INTER_SLK_BEL_2" index="2" disallow="pedestrian" speed="16.67" length="80.00"/>
    </edge>
    <edge id="E_INTER_KOR_SLK" from="J_KOR_3" to="J_SLK_1" priority="3" numLanes="3" speed="16.67">
        <lane id="E_INTER_KOR_SLK_0" index="0" allow="pedestrian" width="2.00" speed="1.40" length="80.00"/>
        <lane id="E_INTER_KOR_SLK_1" index="1" disallow="pedestrian" speed="16.67" length="80.00"/>
        <lane id="E_INTER_KOR_SLK_2" index="2" disallow="pedestrian" speed="16.67" length="80.00"/>
    </edge>

    <!-- Traffic Light Logic (TLS) -->
    <tlLogic id="J_SLK_2" type="static" programID="0" offset="0">
        <phase duration="28" state="GGgrrrGGgrrr"/>
        <phase duration="4"  state="yyyrrryyyrrr"/>
        <phase duration="28" state="rrrGGgrrrGGg"/>
        <phase duration="4"  state="rrryyyrrryyy"/>
    </tlLogic>
    <tlLogic id="J_BEL_1" type="static" programID="0" offset="0">
        <phase duration="26" state="GGgrrrGGgrrr"/>
        <phase duration="4"  state="yyyrrryyyrrr"/>
        <phase duration="26" state="rrrGGgrrrGGg"/>
        <phase duration="4"  state="rrryyyrrryyy"/>
    </tlLogic>
</net>
"""

with open(net_xml_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Generated SUMO network file at: {net_xml_path}")
