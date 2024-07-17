\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  0 x,0,0 + 24.02082429892863 x,0,3 + 24.02082429892863 x,0,4 + 10 x,0,5
   + 30.80584360149873 x,0,6 + 12.8062484748657 x,0,7 + 35 x,0,8 + 15 x,0,9
   + 0 x,1,0 + 0 x,1,1 + 24.02082429892863 x,1,3 + 24.02082429892863 x,1,4
   + 10 x,1,5 + 30.80584360149873 x,1,6 + 12.8062484748657 x,1,7 + 35 x,1,8
   + 15 x,1,9 + 0 x,2,0 + 0 x,2,2 + 24.02082429892863 x,2,3
   + 24.02082429892863 x,2,4 + 10 x,2,5 + 30.80584360149873 x,2,6
   + 12.8062484748657 x,2,7 + 35 x,2,8 + 15 x,2,9 + 0 x,3,0
   + 24.02082429892863 x,3,1 + 24.02082429892863 x,3,2 + 0 x,3,3
   + 25.63201123595259 x,3,5 + 52.55473337388365 x,3,6
   + 16.64331697709324 x,3,7 + 11.04536101718726 x,3,8
   + 27.78488797889961 x,3,9 + 24.02082429892863 x,3,10 + 0 x,4,0
   + 24.02082429892863 x,4,1 + 24.02082429892863 x,4,2 + 0 x,4,4
   + 25.63201123595259 x,4,5 + 52.55473337388365 x,4,6
   + 16.64331697709324 x,4,7 + 11.04536101718726 x,4,8
   + 27.78488797889961 x,4,9 + 24.02082429892863 x,4,10 + 0 x,5,0
   + 10 x,5,1 + 10 x,5,2 + 25.63201123595259 x,5,3
   + 25.63201123595259 x,5,4 + 0 x,5,5 + 37.53664875824692 x,5,6
   + 20.591260281974 x,5,7 + 36.40054944640259 x,5,8 + 5 x,5,9 + 10 x,5,10
   + 0 x,6,0 + 30.80584360149873 x,6,1 + 30.80584360149873 x,6,2
   + 52.55473337388365 x,6,3 + 52.55473337388365 x,6,4
   + 37.53664875824692 x,6,5 + 0 x,6,6 + 36.40054944640259 x,6,7
   + 62.6418390534633 x,6,8 + 41.4004830889689 x,6,9
   + 30.80584360149873 x,6,10 + 0 x,7,0 + 12.8062484748657 x,7,1
   + 12.8062484748657 x,7,2 + 16.64331697709324 x,7,3
   + 16.64331697709324 x,7,4 + 20.591260281974 x,7,5
   + 36.40054944640259 x,7,6 + 0 x,7,7 + 26.24880949681338 x,7,8
   + 25.07987240796891 x,7,9 + 12.8062484748657 x,7,10 + 0 x,8,0 + 35 x,8,1
   + 35 x,8,2 + 11.04536101718726 x,8,3 + 11.04536101718726 x,8,4
   + 36.40054944640259 x,8,5 + 62.6418390534633 x,8,6
   + 26.24880949681338 x,8,7 + 0 x,8,8 + 38.07886552931954 x,8,9
   + 35 x,8,10 + 0 x,9,0 + 15 x,9,1 + 15 x,9,2 + 27.78488797889961 x,9,3
   + 27.78488797889961 x,9,4 + 5 x,9,5 + 41.4004830889689 x,9,6
   + 25.07987240796891 x,9,7 + 38.07886552931954 x,9,8 + 0 x,9,9
   + 15 x,9,10 + 0 x,10,0 + 0 x,10,1 + 0 x,10,2 + 0 x,10,3 + 0 x,10,4
   + 0 x,10,5 + 0 x,10,6 + 0 x,10,7 + 0 x,10,8 + 0 x,10,9 + 0 x,10,10
Subject To
 customer_connectivity(5): x,5,1 + x,5,2 + x,5,3 + x,5,4 + x,5,6 + x,5,7
   + x,5,8 + x,5,9 + x,5,10 = 1
 customer_connectivity(6): x,6,1 + x,6,2 + x,6,3 + x,6,4 + x,6,5 + x,6,7
   + x,6,8 + x,6,9 + x,6,10 = 1
 customer_connectivity(7): x,7,1 + x,7,2 + x,7,3 + x,7,4 + x,7,5 + x,7,6
   + x,7,8 + x,7,9 + x,7,10 = 1
 customer_connectivity(8): x,8,1 + x,8,2 + x,8,3 + x,8,4 + x,8,5 + x,8,6
   + x,8,7 + x,8,9 + x,8,10 = 1
 customer_connectivity(9): x,9,1 + x,9,2 + x,9,3 + x,9,4 + x,9,5 + x,9,6
   + x,9,7 + x,9,8 + x,9,10 = 1
 station_connectivity(1): x,1,2 + x,1,3 + x,1,4 + x,1,5 + x,1,6 + x,1,7
   + x,1,8 + x,1,9 + x,1,10 <= 1
 station_connectivity(2): x,2,1 + x,2,3 + x,2,4 + x,2,5 + x,2,6 + x,2,7
   + x,2,8 + x,2,9 + x,2,10 <= 1
 station_connectivity(3): x,3,1 + x,3,2 + x,3,4 + x,3,5 + x,3,6 + x,3,7
   + x,3,8 + x,3,9 + x,3,10 <= 1
 station_connectivity(4): x,4,1 + x,4,2 + x,4,3 + x,4,5 + x,4,6 + x,4,7
   + x,4,8 + x,4,9 + x,4,10 <= 1
 flow_conservation(1): x,0,1 - x,1,2 - x,1,3 - x,1,4 - x,1,5 - x,1,6
   - x,1,7 - x,1,8 - x,1,9 - x,1,10 + x,2,1 + x,3,1 + x,4,1 + x,5,1 + x,6,1
   + x,7,1 + x,8,1 + x,9,1 = 0
 flow_conservation(2): x,0,2 + x,1,2 - x,2,1 - x,2,3 - x,2,4 - x,2,5
   - x,2,6 - x,2,7 - x,2,8 - x,2,9 - x,2,10 + x,3,2 + x,4,2 + x,5,2 + x,6,2
   + x,7,2 + x,8,2 + x,9,2 = 0
 flow_conservation(3): x,0,3 + x,1,3 + x,2,3 - x,3,1 - x,3,2 - x,3,4
   - x,3,5 - x,3,6 - x,3,7 - x,3,8 - x,3,9 - x,3,10 + x,4,3 + x,5,3 + x,6,3
   + x,7,3 + x,8,3 + x,9,3 = 0
 flow_conservation(4): x,0,4 + x,1,4 + x,2,4 + x,3,4 - x,4,1 - x,4,2
   - x,4,3 - x,4,5 - x,4,6 - x,4,7 - x,4,8 - x,4,9 - x,4,10 + x,5,4 + x,6,4
   + x,7,4 + x,8,4 + x,9,4 = 0
 flow_conservation(5): x,0,5 + x,1,5 + x,2,5 + x,3,5 + x,4,5 - x,5,1
   - x,5,2 - x,5,3 - x,5,4 - x,5,6 - x,5,7 - x,5,8 - x,5,9 - x,5,10 + x,6,5
   + x,7,5 + x,8,5 + x,9,5 = 0
 flow_conservation(6): x,0,6 + x,1,6 + x,2,6 + x,3,6 + x,4,6 + x,5,6
   - x,6,1 - x,6,2 - x,6,3 - x,6,4 - x,6,5 - x,6,7 - x,6,8 - x,6,9 - x,6,10
   + x,7,6 + x,8,6 + x,9,6 = 0
 flow_conservation(7): x,0,7 + x,1,7 + x,2,7 + x,3,7 + x,4,7 + x,5,7
   + x,6,7 - x,7,1 - x,7,2 - x,7,3 - x,7,4 - x,7,5 - x,7,6 - x,7,8 - x,7,9
   - x,7,10 + x,8,7 + x,9,7 = 0
 flow_conservation(8): x,0,8 + x,1,8 + x,2,8 + x,3,8 + x,4,8 + x,5,8
   + x,6,8 + x,7,8 - x,8,1 - x,8,2 - x,8,3 - x,8,4 - x,8,5 - x,8,6 - x,8,7
   - x,8,9 - x,8,10 + x,9,8 = 0
 flow_conservation(9): x,0,9 + x,1,9 + x,2,9 + x,3,9 + x,4,9 + x,5,9
   + x,6,9 + x,7,9 + x,8,9 - x,9,1 - x,9,2 - x,9,3 - x,9,4 - x,9,5 - x,9,6
   - x,9,7 - x,9,8 - x,9,10 = 0
 time_feasibility(0,1): 1236 x,0,1 + tau,0 - tau,1 <= 1236
 time_feasibility(2,1): - tau,1 + 1505.7925 x,2,1 + tau,2 - 3.47 y,2
   + 3.47 Y,2 <= 1505.7925
 time_feasibility(3,1): - tau,1 + 1529.813324298929 x,3,1 + tau,3
   - 3.47 y,3 + 3.47 Y,3 <= 1505.7925
 time_feasibility(4,1): - tau,1 + 1529.813324298929 x,4,1 + tau,4
   - 3.47 y,4 + 3.47 Y,4 <= 1505.7925
 time_feasibility(5,1): - tau,1 + 1336 x,5,1 + tau,5 <= 1236
 time_feasibility(6,1): - tau,1 + 1356.805843601499 x,6,1 + tau,6 <= 1236
 time_feasibility(7,1): - tau,1 + 1338.806248474866 x,7,1 + tau,7 <= 1236
 time_feasibility(8,1): - tau,1 + 1361 x,8,1 + tau,8 <= 1236
 time_feasibility(9,1): - tau,1 + 1341 x,9,1 + tau,9 <= 1236
 time_feasibility(0,2): 1236 x,0,2 + tau,0 - tau,2 <= 1236
 time_feasibility(1,2): 1505.7925 x,1,2 + tau,1 - 3.47 y,1 + 3.47 Y,1
   - tau,2 <= 1505.7925
 time_feasibility(3,2): - tau,2 + 1529.813324298929 x,3,2 + tau,3
   - 3.47 y,3 + 3.47 Y,3 <= 1505.7925
 time_feasibility(4,2): - tau,2 + 1529.813324298929 x,4,2 + tau,4
   - 3.47 y,4 + 3.47 Y,4 <= 1505.7925
 time_feasibility(5,2): - tau,2 + 1336 x,5,2 + tau,5 <= 1236
 time_feasibility(6,2): - tau,2 + 1356.805843601499 x,6,2 + tau,6 <= 1236
 time_feasibility(7,2): - tau,2 + 1338.806248474866 x,7,2 + tau,7 <= 1236
 time_feasibility(8,2): - tau,2 + 1361 x,8,2 + tau,8 <= 1236
 time_feasibility(9,2): - tau,2 + 1341 x,9,2 + tau,9 <= 1236
 time_feasibility(0,3): 1260.020824298929 x,0,3 + tau,0 - tau,3 <= 1236
 time_feasibility(1,3): 1529.813324298929 x,1,3 + tau,1 - 3.47 y,1
   + 3.47 Y,1 - tau,3 <= 1505.7925
 time_feasibility(2,3): 1529.813324298929 x,2,3 + tau,2 - 3.47 y,2
   + 3.47 Y,2 - tau,3 <= 1505.7925
 time_feasibility(4,3): - tau,3 + 1505.7925 x,4,3 + tau,4 - 3.47 y,4
   + 3.47 Y,4 <= 1505.7925
 time_feasibility(5,3): - tau,3 + 1351.632011235953 x,5,3 + tau,5 <= 1236
 time_feasibility(6,3): - tau,3 + 1378.554733373884 x,6,3 + tau,6 <= 1236
 time_feasibility(7,3): - tau,3 + 1342.643316977093 x,7,3 + tau,7 <= 1236
 time_feasibility(8,3): - tau,3 + 1337.045361017187 x,8,3 + tau,8 <= 1236
 time_feasibility(9,3): - tau,3 + 1353.7848879789 x,9,3 + tau,9 <= 1236
 time_feasibility(0,4): 1260.020824298929 x,0,4 + tau,0 - tau,4 <= 1236
 time_feasibility(1,4): 1529.813324298929 x,1,4 + tau,1 - 3.47 y,1
   + 3.47 Y,1 - tau,4 <= 1505.7925
 time_feasibility(2,4): 1529.813324298929 x,2,4 + tau,2 - 3.47 y,2
   + 3.47 Y,2 - tau,4 <= 1505.7925
 time_feasibility(3,4): 1505.7925 x,3,4 + tau,3 - 3.47 y,3 + 3.47 Y,3
   - tau,4 <= 1505.7925
 time_feasibility(5,4): - tau,4 + 1351.632011235953 x,5,4 + tau,5 <= 1236
 time_feasibility(6,4): - tau,4 + 1378.554733373884 x,6,4 + tau,6 <= 1236
 time_feasibility(7,4): - tau,4 + 1342.643316977093 x,7,4 + tau,7 <= 1236
 time_feasibility(8,4): - tau,4 + 1337.045361017187 x,8,4 + tau,8 <= 1236
 time_feasibility(9,4): - tau,4 + 1353.7848879789 x,9,4 + tau,9 <= 1236
 time_feasibility(0,5): 1246 x,0,5 + tau,0 - tau,5 <= 1236
 time_feasibility(1,5): 1515.7925 x,1,5 + tau,1 - 3.47 y,1 + 3.47 Y,1
   - tau,5 <= 1505.7925
 time_feasibility(2,5): 1515.7925 x,2,5 + tau,2 - 3.47 y,2 + 3.47 Y,2
   - tau,5 <= 1505.7925
 time_feasibility(3,5): 1531.424511235953 x,3,5 + tau,3 - 3.47 y,3
   + 3.47 Y,3 - tau,5 <= 1505.7925
 time_feasibility(4,5): 1531.424511235953 x,4,5 + tau,4 - 3.47 y,4
   + 3.47 Y,4 - tau,5 <= 1505.7925
 time_feasibility(6,5): - tau,5 + 1363.536648758247 x,6,5 + tau,6 <= 1236
 time_feasibility(7,5): - tau,5 + 1346.591260281974 x,7,5 + tau,7 <= 1236
 time_feasibility(8,5): - tau,5 + 1362.400549446403 x,8,5 + tau,8 <= 1236
 time_feasibility(9,5): - tau,5 + 1331 x,9,5 + tau,9 <= 1236
 time_feasibility(0,6): 1266.805843601499 x,0,6 + tau,0 - tau,6 <= 1236
 time_feasibility(1,6): 1536.598343601499 x,1,6 + tau,1 - 3.47 y,1
   + 3.47 Y,1 - tau,6 <= 1505.7925
 time_feasibility(2,6): 1536.598343601499 x,2,6 + tau,2 - 3.47 y,2
   + 3.47 Y,2 - tau,6 <= 1505.7925
 time_feasibility(3,6): 1558.347233373884 x,3,6 + tau,3 - 3.47 y,3
   + 3.47 Y,3 - tau,6 <= 1505.7925
 time_feasibility(4,6): 1558.347233373884 x,4,6 + tau,4 - 3.47 y,4
   + 3.47 Y,4 - tau,6 <= 1505.7925
 time_feasibility(5,6): 1363.536648758247 x,5,6 + tau,5 - tau,6 <= 1236
 time_feasibility(7,6): - tau,6 + 1362.400549446403 x,7,6 + tau,7 <= 1236
 time_feasibility(8,6): - tau,6 + 1388.641839053463 x,8,6 + tau,8 <= 1236
 time_feasibility(9,6): - tau,6 + 1367.400483088969 x,9,6 + tau,9 <= 1236
 time_feasibility(0,7): 1248.806248474866 x,0,7 + tau,0 - tau,7 <= 1236
 time_feasibility(1,7): 1518.598748474866 x,1,7 + tau,1 - 3.47 y,1
   + 3.47 Y,1 - tau,7 <= 1505.7925
 time_feasibility(2,7): 1518.598748474866 x,2,7 + tau,2 - 3.47 y,2
   + 3.47 Y,2 - tau,7 <= 1505.7925
 time_feasibility(3,7): 1522.435816977093 x,3,7 + tau,3 - 3.47 y,3
   + 3.47 Y,3 - tau,7 <= 1505.7925
 time_feasibility(4,7): 1522.435816977093 x,4,7 + tau,4 - 3.47 y,4
   + 3.47 Y,4 - tau,7 <= 1505.7925
 time_feasibility(5,7): 1346.591260281974 x,5,7 + tau,5 - tau,7 <= 1236
 time_feasibility(6,7): 1362.400549446403 x,6,7 + tau,6 - tau,7 <= 1236
 time_feasibility(8,7): - tau,7 + 1352.248809496813 x,8,7 + tau,8 <= 1236
 time_feasibility(9,7): - tau,7 + 1351.079872407969 x,9,7 + tau,9 <= 1236
 time_feasibility(0,8): 1271 x,0,8 + tau,0 - tau,8 <= 1236
 time_feasibility(1,8): 1540.7925 x,1,8 + tau,1 - 3.47 y,1 + 3.47 Y,1
   - tau,8 <= 1505.7925
 time_feasibility(2,8): 1540.7925 x,2,8 + tau,2 - 3.47 y,2 + 3.47 Y,2
   - tau,8 <= 1505.7925
 time_feasibility(3,8): 1516.837861017187 x,3,8 + tau,3 - 3.47 y,3
   + 3.47 Y,3 - tau,8 <= 1505.7925
 time_feasibility(4,8): 1516.837861017187 x,4,8 + tau,4 - 3.47 y,4
   + 3.47 Y,4 - tau,8 <= 1505.7925
 time_feasibility(5,8): 1362.400549446403 x,5,8 + tau,5 - tau,8 <= 1236
 time_feasibility(6,8): 1388.641839053463 x,6,8 + tau,6 - tau,8 <= 1236
 time_feasibility(7,8): 1352.248809496813 x,7,8 + tau,7 - tau,8 <= 1236
 time_feasibility(9,8): - tau,8 + 1364.07886552932 x,9,8 + tau,9 <= 1236
 time_feasibility(0,9): 1251 x,0,9 + tau,0 - tau,9 <= 1236
 time_feasibility(1,9): 1520.7925 x,1,9 + tau,1 - 3.47 y,1 + 3.47 Y,1
   - tau,9 <= 1505.7925
 time_feasibility(2,9): 1520.7925 x,2,9 + tau,2 - 3.47 y,2 + 3.47 Y,2
   - tau,9 <= 1505.7925
 time_feasibility(3,9): 1533.5773879789 x,3,9 + tau,3 - 3.47 y,3 + 3.47 Y,3
   - tau,9 <= 1505.7925
 time_feasibility(4,9): 1533.5773879789 x,4,9 + tau,4 - 3.47 y,4 + 3.47 Y,4
   - tau,9 <= 1505.7925
 time_feasibility(5,9): 1331 x,5,9 + tau,5 - tau,9 <= 1236
 time_feasibility(6,9): 1367.400483088969 x,6,9 + tau,6 - tau,9 <= 1236
 time_feasibility(7,9): 1351.079872407969 x,7,9 + tau,7 - tau,9 <= 1236
 time_feasibility(8,9): 1364.07886552932 x,8,9 + tau,8 - tau,9 <= 1236
 time_feasibility(0,10): 1236 x,0,10 + tau,0 - tau,10 <= 1236
 time_feasibility(1,10): 1505.7925 x,1,10 + tau,1 - 3.47 y,1 + 3.47 Y,1
   - tau,10 <= 1505.7925
 time_feasibility(2,10): 1505.7925 x,2,10 + tau,2 - 3.47 y,2 + 3.47 Y,2
   - tau,10 <= 1505.7925
 time_feasibility(3,10): 1529.813324298929 x,3,10 + tau,3 - 3.47 y,3
   + 3.47 Y,3 - tau,10 <= 1505.7925
 time_feasibility(4,10): 1529.813324298929 x,4,10 + tau,4 - 3.47 y,4
   + 3.47 Y,4 - tau,10 <= 1505.7925
 time_feasibility(5,10): 1336 x,5,10 + tau,5 - tau,10 <= 1236
 time_feasibility(6,10): 1356.805843601499 x,6,10 + tau,6 - tau,10 <= 1236
 time_feasibility(7,10): 1338.806248474866 x,7,10 + tau,7 - tau,10 <= 1236
 time_feasibility(8,10): 1361 x,8,10 + tau,8 - tau,10 <= 1236
 time_feasibility(9,10): 1341 x,9,10 + tau,9 - tau,10 <= 1236
 demand_satisfaction(0,1): - 200 x,0,1 + u,0 - u,1 >= -200
 demand_satisfaction(0,2): - 200 x,0,2 + u,0 - u,2 >= -200
 demand_satisfaction(0,3): - 200 x,0,3 + u,0 - u,3 >= -200
 demand_satisfaction(0,4): - 200 x,0,4 + u,0 - u,4 >= -200
 demand_satisfaction(0,5): - 200 x,0,5 + u,0 - u,5 >= -200
 demand_satisfaction(0,6): - 200 x,0,6 + u,0 - u,6 >= -200
 demand_satisfaction(0,7): - 200 x,0,7 + u,0 - u,7 >= -200
 demand_satisfaction(0,8): - 200 x,0,8 + u,0 - u,8 >= -200
 demand_satisfaction(0,9): - 200 x,0,9 + u,0 - u,9 >= -200
 demand_satisfaction(0,10): - 200 x,0,10 + u,0 - u,10 >= -200
 demand_satisfaction(1,2): - 200 x,1,2 + u,1 - u,2 >= -200
 demand_satisfaction(1,3): - 200 x,1,3 + u,1 - u,3 >= -200
 demand_satisfaction(1,4): - 200 x,1,4 + u,1 - u,4 >= -200
 demand_satisfaction(1,5): - 200 x,1,5 + u,1 - u,5 >= -200
 demand_satisfaction(1,6): - 200 x,1,6 + u,1 - u,6 >= -200
 demand_satisfaction(1,7): - 200 x,1,7 + u,1 - u,7 >= -200
 demand_satisfaction(1,8): - 200 x,1,8 + u,1 - u,8 >= -200
 demand_satisfaction(1,9): - 200 x,1,9 + u,1 - u,9 >= -200
 demand_satisfaction(1,10): - 200 x,1,10 + u,1 - u,10 >= -200
 demand_satisfaction(2,1): - u,1 - 200 x,2,1 + u,2 >= -200
 demand_satisfaction(2,3): - 200 x,2,3 + u,2 - u,3 >= -200
 demand_satisfaction(2,4): - 200 x,2,4 + u,2 - u,4 >= -200
 demand_satisfaction(2,5): - 200 x,2,5 + u,2 - u,5 >= -200
 demand_satisfaction(2,6): - 200 x,2,6 + u,2 - u,6 >= -200
 demand_satisfaction(2,7): - 200 x,2,7 + u,2 - u,7 >= -200
 demand_satisfaction(2,8): - 200 x,2,8 + u,2 - u,8 >= -200
 demand_satisfaction(2,9): - 200 x,2,9 + u,2 - u,9 >= -200
 demand_satisfaction(2,10): - 200 x,2,10 + u,2 - u,10 >= -200
 demand_satisfaction(3,1): - u,1 - 200 x,3,1 + u,3 >= -200
 demand_satisfaction(3,2): - u,2 - 200 x,3,2 + u,3 >= -200
 demand_satisfaction(3,4): - 200 x,3,4 + u,3 - u,4 >= -200
 demand_satisfaction(3,5): - 200 x,3,5 + u,3 - u,5 >= -200
 demand_satisfaction(3,6): - 200 x,3,6 + u,3 - u,6 >= -200
 demand_satisfaction(3,7): - 200 x,3,7 + u,3 - u,7 >= -200
 demand_satisfaction(3,8): - 200 x,3,8 + u,3 - u,8 >= -200
 demand_satisfaction(3,9): - 200 x,3,9 + u,3 - u,9 >= -200
 demand_satisfaction(3,10): - 200 x,3,10 + u,3 - u,10 >= -200
 demand_satisfaction(4,1): - u,1 - 200 x,4,1 + u,4 >= -200
 demand_satisfaction(4,2): - u,2 - 200 x,4,2 + u,4 >= -200
 demand_satisfaction(4,3): - u,3 - 200 x,4,3 + u,4 >= -200
 demand_satisfaction(4,5): - 200 x,4,5 + u,4 - u,5 >= -200
 demand_satisfaction(4,6): - 200 x,4,6 + u,4 - u,6 >= -200
 demand_satisfaction(4,7): - 200 x,4,7 + u,4 - u,7 >= -200
 demand_satisfaction(4,8): - 200 x,4,8 + u,4 - u,8 >= -200
 demand_satisfaction(4,9): - 200 x,4,9 + u,4 - u,9 >= -200
 demand_satisfaction(4,10): - 200 x,4,10 + u,4 - u,10 >= -200
 demand_satisfaction(5,1): - u,1 - 210 x,5,1 + u,5 >= -200
 demand_satisfaction(5,2): - u,2 - 210 x,5,2 + u,5 >= -200
 demand_satisfaction(5,3): - u,3 - 210 x,5,3 + u,5 >= -200
 demand_satisfaction(5,4): - u,4 - 210 x,5,4 + u,5 >= -200
 demand_satisfaction(5,6): - 210 x,5,6 + u,5 - u,6 >= -200
 demand_satisfaction(5,7): - 210 x,5,7 + u,5 - u,7 >= -200
 demand_satisfaction(5,8): - 210 x,5,8 + u,5 - u,8 >= -200
 demand_satisfaction(5,9): - 210 x,5,9 + u,5 - u,9 >= -200
 demand_satisfaction(5,10): - 210 x,5,10 + u,5 - u,10 >= -200
 demand_satisfaction(6,1): - u,1 - 220 x,6,1 + u,6 >= -200
 demand_satisfaction(6,2): - u,2 - 220 x,6,2 + u,6 >= -200
 demand_satisfaction(6,3): - u,3 - 220 x,6,3 + u,6 >= -200
 demand_satisfaction(6,4): - u,4 - 220 x,6,4 + u,6 >= -200
 demand_satisfaction(6,5): - u,5 - 220 x,6,5 + u,6 >= -200
 demand_satisfaction(6,7): - 220 x,6,7 + u,6 - u,7 >= -200
 demand_satisfaction(6,8): - 220 x,6,8 + u,6 - u,8 >= -200
 demand_satisfaction(6,9): - 220 x,6,9 + u,6 - u,9 >= -200
 demand_satisfaction(6,10): - 220 x,6,10 + u,6 - u,10 >= -200
 demand_satisfaction(7,1): - u,1 - 210 x,7,1 + u,7 >= -200
 demand_satisfaction(7,2): - u,2 - 210 x,7,2 + u,7 >= -200
 demand_satisfaction(7,3): - u,3 - 210 x,7,3 + u,7 >= -200
 demand_satisfaction(7,4): - u,4 - 210 x,7,4 + u,7 >= -200
 demand_satisfaction(7,5): - u,5 - 210 x,7,5 + u,7 >= -200
 demand_satisfaction(7,6): - u,6 - 210 x,7,6 + u,7 >= -200
 demand_satisfaction(7,8): - 210 x,7,8 + u,7 - u,8 >= -200
 demand_satisfaction(7,9): - 210 x,7,9 + u,7 - u,9 >= -200
 demand_satisfaction(7,10): - 210 x,7,10 + u,7 - u,10 >= -200
 demand_satisfaction(8,1): - u,1 - 240 x,8,1 + u,8 >= -200
 demand_satisfaction(8,2): - u,2 - 240 x,8,2 + u,8 >= -200
 demand_satisfaction(8,3): - u,3 - 240 x,8,3 + u,8 >= -200
 demand_satisfaction(8,4): - u,4 - 240 x,8,4 + u,8 >= -200
 demand_satisfaction(8,5): - u,5 - 240 x,8,5 + u,8 >= -200
 demand_satisfaction(8,6): - u,6 - 240 x,8,6 + u,8 >= -200
 demand_satisfaction(8,7): - u,7 - 240 x,8,7 + u,8 >= -200
 demand_satisfaction(8,9): - 240 x,8,9 + u,8 - u,9 >= -200
 demand_satisfaction(8,10): - 240 x,8,10 + u,8 - u,10 >= -200
 demand_satisfaction(9,1): - u,1 - 210 x,9,1 + u,9 >= -200
 demand_satisfaction(9,2): - u,2 - 210 x,9,2 + u,9 >= -200
 demand_satisfaction(9,3): - u,3 - 210 x,9,3 + u,9 >= -200
 demand_satisfaction(9,4): - u,4 - 210 x,9,4 + u,9 >= -200
 demand_satisfaction(9,5): - u,5 - 210 x,9,5 + u,9 >= -200
 demand_satisfaction(9,6): - u,6 - 210 x,9,6 + u,9 >= -200
 demand_satisfaction(9,7): - u,7 - 210 x,9,7 + u,9 >= -200
 demand_satisfaction(9,8): - u,8 - 210 x,9,8 + u,9 >= -200
 demand_satisfaction(9,10): - 210 x,9,10 + u,9 - u,10 >= -200
 battery_consistency(0,1): - 77.75 x,0,1 + Y,0 - y,1 >= -77.75
 battery_consistency(2,1): - y,1 - 77.75 x,2,1 + Y,2 >= -77.75
 battery_consistency(3,1): - y,1 - 101.7708242989286 x,3,1 + Y,3 >= -77.75
 battery_consistency(4,1): - y,1 - 101.7708242989286 x,4,1 + Y,4 >= -77.75
 battery_consistency(5,1): - y,1 - 87.75 x,5,1 + y,5 >= -77.75
 battery_consistency(6,1): - y,1 - 108.5558436014987 x,6,1 + y,6 >= -77.75
 battery_consistency(7,1): - y,1 - 90.5562484748657 x,7,1 + y,7 >= -77.75
 battery_consistency(8,1): - y,1 - 112.75 x,8,1 + y,8 >= -77.75
 battery_consistency(9,1): - y,1 - 92.75 x,9,1 + y,9 >= -77.75
 battery_consistency(0,2): - 77.75 x,0,2 + Y,0 - y,2 >= -77.75
 battery_consistency(1,2): - 77.75 x,1,2 + Y,1 - y,2 >= -77.75
 battery_consistency(3,2): - y,2 - 101.7708242989286 x,3,2 + Y,3 >= -77.75
 battery_consistency(4,2): - y,2 - 101.7708242989286 x,4,2 + Y,4 >= -77.75
 battery_consistency(5,2): - y,2 - 87.75 x,5,2 + y,5 >= -77.75
 battery_consistency(6,2): - y,2 - 108.5558436014987 x,6,2 + y,6 >= -77.75
 battery_consistency(7,2): - y,2 - 90.5562484748657 x,7,2 + y,7 >= -77.75
 battery_consistency(8,2): - y,2 - 112.75 x,8,2 + y,8 >= -77.75
 battery_consistency(9,2): - y,2 - 92.75 x,9,2 + y,9 >= -77.75
 battery_consistency(0,3): - 101.7708242989286 x,0,3 + Y,0 - y,3 >= -77.75
 battery_consistency(1,3): - 101.7708242989286 x,1,3 + Y,1 - y,3 >= -77.75
 battery_consistency(2,3): - 101.7708242989286 x,2,3 + Y,2 - y,3 >= -77.75
 battery_consistency(4,3): - y,3 - 77.75 x,4,3 + Y,4 >= -77.75
 battery_consistency(5,3): - y,3 - 103.3820112359526 x,5,3 + y,5 >= -77.75
 battery_consistency(6,3): - y,3 - 130.3047333738837 x,6,3 + y,6 >= -77.75
 battery_consistency(7,3): - y,3 - 94.39331697709324 x,7,3 + y,7 >= -77.75
 battery_consistency(8,3): - y,3 - 88.79536101718726 x,8,3 + y,8 >= -77.75
 battery_consistency(9,3): - y,3 - 105.5348879788996 x,9,3 + y,9 >= -77.75
 battery_consistency(0,4): - 101.7708242989286 x,0,4 + Y,0 - y,4 >= -77.75
 battery_consistency(1,4): - 101.7708242989286 x,1,4 + Y,1 - y,4 >= -77.75
 battery_consistency(2,4): - 101.7708242989286 x,2,4 + Y,2 - y,4 >= -77.75
 battery_consistency(3,4): - 77.75 x,3,4 + Y,3 - y,4 >= -77.75
 battery_consistency(5,4): - y,4 - 103.3820112359526 x,5,4 + y,5 >= -77.75
 battery_consistency(6,4): - y,4 - 130.3047333738837 x,6,4 + y,6 >= -77.75
 battery_consistency(7,4): - y,4 - 94.39331697709324 x,7,4 + y,7 >= -77.75
 battery_consistency(8,4): - y,4 - 88.79536101718726 x,8,4 + y,8 >= -77.75
 battery_consistency(9,4): - y,4 - 105.5348879788996 x,9,4 + y,9 >= -77.75
 battery_consistency(0,5): - 87.75 x,0,5 + Y,0 - y,5 >= -77.75
 battery_consistency(1,5): - 87.75 x,1,5 + Y,1 - y,5 >= -77.75
 battery_consistency(2,5): - 87.75 x,2,5 + Y,2 - y,5 >= -77.75
 battery_consistency(3,5): - 103.3820112359526 x,3,5 + Y,3 - y,5 >= -77.75
 battery_consistency(4,5): - 103.3820112359526 x,4,5 + Y,4 - y,5 >= -77.75
 battery_consistency(6,5): - y,5 - 115.2866487582469 x,6,5 + y,6 >= -77.75
 battery_consistency(7,5): - y,5 - 98.341260281974 x,7,5 + y,7 >= -77.75
 battery_consistency(8,5): - y,5 - 114.1505494464026 x,8,5 + y,8 >= -77.75
 battery_consistency(9,5): - y,5 - 82.75 x,9,5 + y,9 >= -77.75
 battery_consistency(0,6): - 108.5558436014987 x,0,6 + Y,0 - y,6 >= -77.75
 battery_consistency(1,6): - 108.5558436014987 x,1,6 + Y,1 - y,6 >= -77.75
 battery_consistency(2,6): - 108.5558436014987 x,2,6 + Y,2 - y,6 >= -77.75
 battery_consistency(3,6): - 130.3047333738837 x,3,6 + Y,3 - y,6 >= -77.75
 battery_consistency(4,6): - 130.3047333738837 x,4,6 + Y,4 - y,6 >= -77.75
 battery_consistency(5,6): - 115.2866487582469 x,5,6 + y,5 - y,6 >= -77.75
 battery_consistency(7,6): - y,6 - 114.1505494464026 x,7,6 + y,7 >= -77.75
 battery_consistency(8,6): - y,6 - 140.3918390534633 x,8,6 + y,8 >= -77.75
 battery_consistency(9,6): - y,6 - 119.1504830889689 x,9,6 + y,9 >= -77.75
 battery_consistency(0,7): - 90.5562484748657 x,0,7 + Y,0 - y,7 >= -77.75
 battery_consistency(1,7): - 90.5562484748657 x,1,7 + Y,1 - y,7 >= -77.75
 battery_consistency(2,7): - 90.5562484748657 x,2,7 + Y,2 - y,7 >= -77.75
 battery_consistency(3,7): - 94.39331697709324 x,3,7 + Y,3 - y,7 >= -77.75
 battery_consistency(4,7): - 94.39331697709324 x,4,7 + Y,4 - y,7 >= -77.75
 battery_consistency(5,7): - 98.341260281974 x,5,7 + y,5 - y,7 >= -77.75
 battery_consistency(6,7): - 114.1505494464026 x,6,7 + y,6 - y,7 >= -77.75
 battery_consistency(8,7): - y,7 - 103.9988094968134 x,8,7 + y,8 >= -77.75
 battery_consistency(9,7): - y,7 - 102.8298724079689 x,9,7 + y,9 >= -77.75
 battery_consistency(0,8): - 112.75 x,0,8 + Y,0 - y,8 >= -77.75
 battery_consistency(1,8): - 112.75 x,1,8 + Y,1 - y,8 >= -77.75
 battery_consistency(2,8): - 112.75 x,2,8 + Y,2 - y,8 >= -77.75
 battery_consistency(3,8): - 88.79536101718726 x,3,8 + Y,3 - y,8 >= -77.75
 battery_consistency(4,8): - 88.79536101718726 x,4,8 + Y,4 - y,8 >= -77.75
 battery_consistency(5,8): - 114.1505494464026 x,5,8 + y,5 - y,8 >= -77.75
 battery_consistency(6,8): - 140.3918390534633 x,6,8 + y,6 - y,8 >= -77.75
 battery_consistency(7,8): - 103.9988094968134 x,7,8 + y,7 - y,8 >= -77.75
 battery_consistency(9,8): - y,8 - 115.8288655293195 x,9,8 + y,9 >= -77.75
 battery_consistency(0,9): - 92.75 x,0,9 + Y,0 - y,9 >= -77.75
 battery_consistency(1,9): - 92.75 x,1,9 + Y,1 - y,9 >= -77.75
 battery_consistency(2,9): - 92.75 x,2,9 + Y,2 - y,9 >= -77.75
 battery_consistency(3,9): - 105.5348879788996 x,3,9 + Y,3 - y,9 >= -77.75
 battery_consistency(4,9): - 105.5348879788996 x,4,9 + Y,4 - y,9 >= -77.75
 battery_consistency(5,9): - 82.75 x,5,9 + y,5 - y,9 >= -77.75
 battery_consistency(6,9): - 119.1504830889689 x,6,9 + y,6 - y,9 >= -77.75
 battery_consistency(7,9): - 102.8298724079689 x,7,9 + y,7 - y,9 >= -77.75
 battery_consistency(8,9): - 115.8288655293195 x,8,9 + y,8 - y,9 >= -77.75
 battery_consistency(0,10): - 77.75 x,0,10 + Y,0 - y,10 >= -77.75
 battery_consistency(1,10): - 77.75 x,1,10 + Y,1 - y,10 >= -77.75
 battery_consistency(2,10): - 77.75 x,2,10 + Y,2 - y,10 >= -77.75
 battery_consistency(3,10): - 101.7708242989286 x,3,10 + Y,3 - y,10
   >= -77.75
 battery_consistency(4,10): - 101.7708242989286 x,4,10 + Y,4 - y,10
   >= -77.75
 battery_consistency(5,10): - 87.75 x,5,10 + y,5 - y,10 >= -77.75
 battery_consistency(6,10): - 108.5558436014987 x,6,10 + y,6 - y,10
   >= -77.75
 battery_consistency(7,10): - 90.5562484748657 x,7,10 + y,7 - y,10
   >= -77.75
 battery_consistency(8,10): - 112.75 x,8,10 + y,8 - y,10 >= -77.75
 battery_consistency(9,10): - 92.75 x,9,10 + y,9 - y,10 >= -77.75
 battery_after_recharge(0): y,0 - Y,0 <= 0
 battery_after_recharge(1): y,1 - Y,1 <= 0
 battery_after_recharge(2): y,2 - Y,2 <= 0
 battery_after_recharge(3): y,3 - Y,3 <= 0
 battery_after_recharge(4): y,4 - Y,4 <= 0
Bounds
 tau,0 <= 1236
 u,0 <= 200
 y,0 <= 77.75
 Y,0 <= 77.75
 tau,1 <= 1236
 u,1 <= 200
 y,1 <= 77.75
 Y,1 <= 77.75
 tau,2 <= 1236
 u,2 <= 200
 y,2 <= 77.75
 Y,2 <= 77.75
 tau,3 <= 1236
 u,3 <= 200
 y,3 <= 77.75
 Y,3 <= 77.75
 tau,4 <= 1236
 u,4 <= 200
 y,4 <= 77.75
 Y,4 <= 77.75
 tau,5 <= 1136
 u,5 <= 200
 y,5 <= 77.75
 tau,6 <= 1115
 u,6 <= 200
 y,6 <= 77.75
 67 <= tau,7 <= 139
 u,7 <= 200
 y,7 <= 77.75
 989 <= tau,8 <= 1063
 u,8 <= 200
 y,8 <= 77.75
 tau,9 <= 1131
 u,9 <= 200
 y,9 <= 77.75
 tau,10 <= 1236
 u,10 <= 200
 y,10 <= 77.75
Binaries
 x,0,0 x,0,1 x,0,2 x,0,3 x,0,4 x,0,5 x,0,6 x,0,7 x,0,8 x,0,9 x,0,10 x,1,0
 x,1,1 x,1,2 x,1,3 x,1,4 x,1,5 x,1,6 x,1,7 x,1,8 x,1,9 x,1,10 x,2,0 x,2,1
 x,2,2 x,2,3 x,2,4 x,2,5 x,2,6 x,2,7 x,2,8 x,2,9 x,2,10 x,3,0 x,3,1 x,3,2
 x,3,3 x,3,4 x,3,5 x,3,6 x,3,7 x,3,8 x,3,9 x,3,10 x,4,0 x,4,1 x,4,2 x,4,3
 x,4,4 x,4,5 x,4,6 x,4,7 x,4,8 x,4,9 x,4,10 x,5,0 x,5,1 x,5,2 x,5,3 x,5,4
 x,5,5 x,5,6 x,5,7 x,5,8 x,5,9 x,5,10 x,6,0 x,6,1 x,6,2 x,6,3 x,6,4 x,6,5
 x,6,6 x,6,7 x,6,8 x,6,9 x,6,10 x,7,0 x,7,1 x,7,2 x,7,3 x,7,4 x,7,5 x,7,6
 x,7,7 x,7,8 x,7,9 x,7,10 x,8,0 x,8,1 x,8,2 x,8,3 x,8,4 x,8,5 x,8,6 x,8,7
 x,8,8 x,8,9 x,8,10 x,9,0 x,9,1 x,9,2 x,9,3 x,9,4 x,9,5 x,9,6 x,9,7 x,9,8
 x,9,9 x,9,10 x,10,0 x,10,1 x,10,2 x,10,3 x,10,4 x,10,5 x,10,6 x,10,7
 x,10,8 x,10,9 x,10,10
End
