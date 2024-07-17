/**
 * @author 621819es
 * Main method for MILP
 */


import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import com.gurobi.gurobi.*;


public class Main {
    /**
     * main function for running Gurobi optimization
     * to run:
     * 1. remove comment markers from the desired instances
     * 2. set price_idx to 0, 1 or 2
     * 3. run solve() for EVRPTW, solve_extension() for EVRPTW-BD
     * or solve_BD_cost_for_existing_solution() to calculate the BD costs for already existing EVRPTW solution
     */
    public static void main(String[] args) throws GRBException, IOException {
        List<String> files = new ArrayList<>();
        files.add("c101C5");
//        files.add("c103C5");
//        files.add("c101C10");
//        files.add("c104C10");
//        files.add("c103C15");
//        files.add("c106C15");
//        files.add("c206C5");
//        files.add("c208C5");
//        files.add("c202C10");
//        files.add("c205C10");
//        files.add("c202C15");
//        files.add("c208C15");
//        files.add("r104C5");
//        files.add("r105C5");
//        files.add("r102C10");
//        files.add("r103C10");
//        files.add("r102C15");
//        files.add("r105C15");
//        files.add("r202C5");
//        files.add("r203C5");
//        files.add("r201C10");
//        files.add("r203C10");
//        files.add("r202C15");
//        files.add("r209C15");
//        files.add("rc105C5");
//        files.add("rc108C5");
//        files.add("rc102C10");
//        files.add("rc108C10");
//        files.add("rc103C15");
//        files.add("rc108C15");
//        files.add("rc204C5");
//        files.add("rc208C5");
//        files.add("rc201C10");
//        files.add("rc205C10");
//        files.add("rc202C15");
//        files.add("rc204C15");

         double[] WLs = {0.1, 0.5, 2.5};
         double[] WHs = {0.2, 1, 5};
         int price_idx = 0;

        for (String file: files) {
            solve(file);
//            solve_extension(file, WLs[price_idx], WHs[price_idx]);
//            solve_BD_cost_for_existing_solution(file, WLs[price_idx], WHs[price_idx]);
        }
    }

    /**
     * solves EVRPTW problem (without considering BD costs) for a specified instance
     * @param file: name of the instance
     */
    public static void solve (String file) throws GRBException, IOException {
        // creating the parameters
        long startTime = System.currentTimeMillis();
        String path = "./evrptw_instances/" + file;
        List<List<String>> locationData = Helper.expandDummies(path + "_locations.csv");
        List<List<String>> otherData = Helper.readFile(path + "_other.csv");
        List<Integer> demands = Helper.getDemands(locationData);
        List<int[]> timeWindows = Helper.getTimeWindows(locationData);
        List<Integer> serviceTimes = Helper.getServiceTimes(locationData);
        double Q = Helper.getBatteryCapacity(otherData);
        double C = Helper.getLoadCapacity(otherData);
        double h = Helper.getBatteryConsumptionRate(otherData);
        double g = Helper.getRechargingRate(otherData);
        double v = Helper.getVelocity(otherData);
        double[][] distance = Helper.getDistanceMatrix(locationData);
        double[][] travelTimes = Helper.getTravelTimeMatrix(distance, v);
        int nDummies = Helper.nStations(locationData);
        int n = locationData.size() - 2;

        // creating an environment
        GRBEnv env = new GRBEnv();
        env.start();
        // creating an empty model
        GRBModel model = new GRBModel(env);
        // setting the runtime limit
        double timeLimit = 7200;
        model.set(GRB.DoubleParam.TimeLimit, timeLimit);

        // creating the decision variables
        GRBVar[][] isArcTraversed = new GRBVar[n + 2][n + 2];
        GRBVar[] arrivalTime = new GRBVar[n + 2];
        GRBVar[] cargoUponArrival = new GRBVar[n + 2];
        GRBVar[] batteryUponArrival = new GRBVar[n + 2];
        GRBVar[] batteryUponDeparture = new GRBVar[nDummies + 1];

        for (int i = 0; i <= n + 1; i++) {
            for (int j = 0; j <= n + 1; j++) {
                isArcTraversed[i][j] = model.addVar(0, 1, 0.0, GRB.BINARY,
                        "x," + i + "," + j);
            }
            arrivalTime[i] = model.addVar(timeWindows.get(i)[0], timeWindows.get(i)[1], 0.0, GRB.CONTINUOUS,
                    "tau," + i);
            cargoUponArrival[i] = model.addVar(0, C, 0.0, GRB.CONTINUOUS,
                    "u," + i);
            batteryUponArrival[i] = model.addVar(0, Q, 0.0, GRB.CONTINUOUS,
                    "y," + i);
            if (i <= nDummies) {
                batteryUponDeparture[i] = model.addVar(0, Q, 0.0, GRB.CONTINUOUS,
                        "Y," + i);
            }
        }

        // creating the constraints
        for (int i = nDummies + 1; i <= n; i++) {
            GRBLinExpr sumOverJ = new GRBLinExpr();
            for (int j = 1; j <= n + 1; j++) {
                if (i == j) {
                    continue;
                }
                sumOverJ.addTerm(1, isArcTraversed[i][j]);
            }
            model.addConstr(sumOverJ, GRB.EQUAL, 1,
                    "customer connectivity(" + i + ")");
        }

        for (int i = 1; i <= nDummies; i++) {
            GRBLinExpr sumOverJ = new GRBLinExpr();
            for (int j = 1; j <= n + 1; j++) {
                if (i == j) {
                    continue;
                }

                sumOverJ.addTerm(1, isArcTraversed[i][j]);
            }
            model.addConstr(sumOverJ, GRB.LESS_EQUAL, 1,
                    "station connectivity(" + i + ")");
        }

        for (int j = 1; j <= n; j++) {
            GRBLinExpr flowBalance = new GRBLinExpr();
            for (int i = 0; i <= n; i++) {
                if (i == j) {
                    continue;
                }
                flowBalance.addTerm(1, isArcTraversed[i][j]);
            }
            for (int i = 1; i <= n + 1; i++) {
                if (i == j) {
                    continue;
                }
                flowBalance.addTerm(-1, isArcTraversed[j][i]);
            }
            model.addConstr(flowBalance, GRB.EQUAL, 0,
                    "flow conservation(" + j + ")");
        }

        for (int j = 1; j <= n + 1; j++) {
            for (int i = 0; i <= n; i++) {
                if (i == j) {
                    continue;
                }
                GRBLinExpr common = new GRBLinExpr();
                common.addTerm(1, arrivalTime[i]);
                common.addTerm(travelTimes[i][j], isArcTraversed[i][j]);
                common.addConstant(-timeWindows.get(0)[1]);
                common.addTerm(timeWindows.get(0)[1], isArcTraversed[i][j]);
                if (i >= 1 && i <= nDummies) {
                    GRBLinExpr station = new GRBLinExpr();
                    station.add(common);
                    station.addTerm(g, batteryUponDeparture[i]);
                    station.addTerm(-g, batteryUponArrival[i]);
                    station.addConstant(-g * Q);
                    station.addTerm(g * Q, isArcTraversed[i][j]);
                    model.addConstr(station, GRB.LESS_EQUAL, arrivalTime[j],
                            "time feasibility(" + i + "," + j + ")");
                } else {
                    GRBLinExpr customer0 = new GRBLinExpr();
                    customer0.add(common);
                    customer0.addTerm(serviceTimes.get(i), isArcTraversed[i][j]);
                    model.addConstr(customer0, GRB.LESS_EQUAL, arrivalTime[j],
                            "time feasibility(" + i + "," + j + ")");
                }
            }
        }

        for (int i = 0; i <= n; i++) {
            for (int j = 1; j <= n + 1; j++) {
                if (i == j) {
                    continue;
                }
                GRBLinExpr expr = new GRBLinExpr();
                expr.addTerm(1, cargoUponArrival[i]);
                expr.addTerm(-demands.get(i), isArcTraversed[i][j]);
                expr.addConstant(C);
                expr.addTerm(-C, isArcTraversed[i][j]);
                model.addConstr(expr, GRB.GREATER_EQUAL, cargoUponArrival[j],
                        "demand satisfaction(" + i + "," + j + ")");
            }
        }

        for (int j = 1; j <= n + 1; j++) {
            for (int i = 0; i <= n; i++) {
                if (i == j) {
                    continue;
                }
                GRBLinExpr common = new GRBLinExpr();
                common.addTerm(-h * distance[i][j], isArcTraversed[i][j]);
                common.addConstant(Q);
                common.addTerm(-Q, isArcTraversed[i][j]);
                if (i <= nDummies) {
                    GRBLinExpr station0 = new GRBLinExpr();
                    station0.add(common);
                    station0.addTerm(1, batteryUponDeparture[i]);
                    model.addConstr(station0, GRB.GREATER_EQUAL, batteryUponArrival[j],
                            "battery consistency(" + i + "," + j + ")");
                } else {
                    GRBLinExpr customer = new GRBLinExpr();
                    customer.add(common);
                    customer.addTerm(1, batteryUponArrival[i]);
                    model.addConstr(customer, GRB.GREATER_EQUAL, batteryUponArrival[j],
                            "battery consistency(" + i + "," + j + ")");
                }
            }
        }

        for (int i = 0; i <= nDummies; i++) {
            model.addConstr(batteryUponArrival[i], GRB.LESS_EQUAL, batteryUponDeparture[i],
                    "battery after recharge(" + i + ")");
        }

        // creating the objective
        GRBLinExpr objective = new GRBLinExpr();
        for (int i = 0; i <= n; i++) {
            for (int j = 1; j <= n + 1; j++) {
                if (i == j) {
                    continue;
                }
                objective.addTerm(distance[i][j], isArcTraversed[i][j]);
            }
        }

        model.setObjective(objective, GRB.MINIMIZE);
        model.optimize();
        model.write(file + ".lp");
        long endTime = System.currentTimeMillis();
        long elapsedTime = (endTime - startTime);

        // print and save the results (if feasible solution found)
        int status = model.get(GRB.IntAttr.Status);
        if (status == GRB.Status.OPTIMAL || status == GRB.Status.TIME_LIMIT) {
            System.out.println("Objective = " + model.get(GRB.DoubleAttr.ObjVal));
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(file + ".csv"))) {
                writer.write("objective," + model.get(GRB.DoubleAttr.ObjVal) + "\n");
                writer.write("runtime (milliseconds)," + elapsedTime + "\n");

                for (GRBVar var : model.getVars()) {
                    if (var.get(GRB.DoubleAttr.X) != 0) {
                        System.out.println(var.get(GRB.StringAttr.VarName) + ": " + var.get(GRB.DoubleAttr.X));
                        writer.write(var.get(GRB.StringAttr.VarName) + "," + var.get(GRB.DoubleAttr.X));
                        writer.newLine();
                    }
                }

                writer.flush();
            }
            catch (IOException e) {
                System.err.println("Error writing to file: " + e.getMessage());
            }
        } else {
            System.out.println("No optimal solution found");
        }

        model.dispose();
        env.dispose();
    }

    /**
     * solves EVRPTW-BD (with battery degradation) for a specified instance
     * @param file: name of the instance
     * @param WL: low SoC BD cost
     * @param WH: high SoC BD cost
     */
    public static void solve_extension (String file, double WL, double WH) throws GRBException, IOException {
        long startTime = System.currentTimeMillis();
        String model_path = "./models/" + file + ".lp";
        // creating an environment
        GRBEnv env = new GRBEnv();
        env.start();
        // creating a copy of initial model
        GRBModel model = new GRBModel(env, model_path);
        // setting the time limit
        double timeLimit = 7200;
        model.set(GRB.DoubleParam.TimeLimit, timeLimit);

        // creating parameters
        String data_path = "./evrptw_instances/" + file;
        List<List<String>> locationData = Helper.expandDummies(data_path + "_locations.csv");
        List<List<String>> otherData = Helper.readFile(data_path + "_other.csv");
        double[][] distance = Helper.getDistanceMatrix(locationData);
        double Q = Helper.getBatteryCapacity(otherData);
        int n = locationData.size() - 2;
        int nDummies = Helper.nStations(locationData);
        double LB = 0.25;
        double UB = 0.85;

        // creating additional  decision variables
        GRBVar[] chargeBelowLB = new GRBVar[n + 1];
        GRBVar[] chargeAboveUB = new GRBVar[n + 1];

        GRBVar[] chargesFromDepot = new GRBVar[n + 1];
        GRBVar[] chargesToDepot = new GRBVar[n + 1];

        for (int i = 1; i <= n; i++) {
            chargesFromDepot[i] = model.addVar(0, Q*(1 - UB), 0.0, GRB.CONTINUOUS,
                    "zH," + 0 + "," + i);
            chargesToDepot[i] = model.addVar(0, Q*LB, 0.0, GRB.CONTINUOUS,
                    "zL," + i + "," + (n + 1));
        }

        for (int i = 1; i <= nDummies; i++) {
            chargeBelowLB[i] = model.addVar(0, Q*LB, 0.0, GRB.CONTINUOUS,
                    "zL," + i);
            chargeAboveUB[i] = model.addVar(0, Q*(1 - UB), 0.0, GRB.CONTINUOUS,
                    "zH," + i);
        }

        // creating additional constraints
        for (int i = 1; i <= n; i++) {
            GRBLinExpr fromDepot1 = new GRBLinExpr();
            fromDepot1.addTerm(1, model.getVarByName(("y," + i)));
            fromDepot1.addConstant(distance[0][i] - UB*Q - Q);
            fromDepot1.addTerm(Q, model.getVarByName("x," + 0 + "," + i));
            model.addConstr(chargesFromDepot[i], GRB.GREATER_EQUAL, fromDepot1,
                    "1:charge above UB before visiting " + i);
            GRBLinExpr fromDepot2 = new GRBLinExpr();
            fromDepot2.addTerm(1, model.getVarByName(("y," + i)));
            fromDepot2.addConstant(distance[0][i] - UB*Q + Q);
            fromDepot2.addTerm(-Q, model.getVarByName("x," + 0 + "," + i));
            model.addConstr(chargesFromDepot[i], GRB.LESS_EQUAL, fromDepot2,
                    "2:charge above UB before visiting " + i);
            GRBLinExpr toDepot1 = new GRBLinExpr();
            toDepot1.addConstant(LB*Q + distance[i][n+1] - Q);
            if (i <= nDummies) {
                toDepot1.addTerm(-1, model.getVarByName(("Y," + i)));
            }
            else {
                toDepot1.addTerm(-1, model.getVarByName(("y," + i)));
            }
            toDepot1.addTerm(Q, model.getVarByName("x," + i + "," + (n + 1)));
            model.addConstr(chargesToDepot[i], GRB.GREATER_EQUAL, toDepot1,
                    "1: charge below LB after visiting " + i);
            GRBLinExpr toDepot2 = new GRBLinExpr();
            toDepot2.addConstant(LB*Q + distance[i][n+1] + Q);
            if (i <= nDummies) {
                toDepot2.addTerm(-1, model.getVarByName(("Y," + i)));
            }
            else {
                toDepot2.addTerm(-1, model.getVarByName(("y," + i)));
            }
            toDepot2.addTerm(-Q, model.getVarByName("x," + i + "," + (n + 1)));
            model.addConstr(chargesToDepot[i], GRB.LESS_EQUAL, toDepot2,
                    "1: charge below LB after visiting " + i);
        }

        for (int i = 1; i <= nDummies; i++) {
            GRBLinExpr rhsL = new GRBLinExpr();
            rhsL.addConstant(LB*Q);
            rhsL.addTerm(-1, model.getVarByName("y," + i));
            model.addConstr(chargeBelowLB[i], GRB.GREATER_EQUAL, rhsL,
                    "charge below LB " + i);
            GRBLinExpr rhsH = new GRBLinExpr();
            rhsH.addTerm(1, model.getVarByName("Y," + i));
            rhsH.addConstant(-(UB * Q));
            model.addConstr(chargeAboveUB[i], GRB.GREATER_EQUAL, rhsH,
                    "charge above UB " + i);
        }

        // creating the objective
        GRBLinExpr objective = new GRBLinExpr();

        for (int i = 0; i <= n; i++) {
            for (int j = 1; j <= n + 1; j++) {
                if (i == j) {
                    continue;
                }
                objective.addTerm(distance[i][j], model.getVarByName("x," + i + "," + j));
            }
        }

        for (int i = 1; i <= nDummies; i++) {
            objective.addTerm(WL, chargeBelowLB[i]);
            objective.addTerm(WH, chargeAboveUB[i]);
        }

        for (int i = 1; i <= n; i++) {
            objective.addTerm(WL, chargesToDepot[i]);
            objective.addTerm(WH, chargesFromDepot[i]);
        }

        model.setObjective(objective, GRB.MINIMIZE);
        model.optimize();
        long endTime = System.currentTimeMillis();
        long elapsedTime = (endTime - startTime);
        int status = model.get(GRB.IntAttr.Status);

        // print and save the results (if feasible solution found)
        if (status == GRB.Status.OPTIMAL || status == GRB.Status.TIME_LIMIT) {
            System.out.println("Objective = " + model.get(GRB.DoubleAttr.ObjVal));
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(file + "_" + WH + ".csv"))) {
                writer.write("objective," + model.get(GRB.DoubleAttr.ObjVal) + "\n");
                writer.write("runtime (milliseconds)," + elapsedTime + "\n");

                for (GRBVar var : model.getVars()) {
                    if (var.get(GRB.DoubleAttr.X) != 0) {
                        System.out.println(var.get(GRB.StringAttr.VarName) + ": " + var.get(GRB.DoubleAttr.X));
                        writer.write(var.get(GRB.StringAttr.VarName) + "," + var.get(GRB.DoubleAttr.X));
                        writer.newLine();
                    }
                }

                writer.flush();
            }
            catch (IOException e) {
                System.err.println("Error writing to file: " + e.getMessage());
            }
        } else {
            System.out.println("No optimal solution found");
        }

        model.dispose();
        env.dispose();
    }

    /**
     * optimizes battery levels on arrival and departure for an existing EVRPTW to minimize BD costs
     * @param file: name of the instance
     * @param WL: low SoC BD cost
     * @param WH: high SoC BD cost
     */
    public static void solve_BD_cost_for_existing_solution (String file, double WL, double WH) throws GRBException, IOException {
        // creating the parameters
        long startTime = System.currentTimeMillis();
        String path = "./evrptw_instances/" + file;
        List<List<String>> locationData = Helper.expandDummies(path + "_locations.csv");
        List<List<String>> otherData = Helper.readFile(path + "_other.csv");
        List<Integer> demands = Helper.getDemands(locationData);
        List<int[]> timeWindows = Helper.getTimeWindows(locationData);
        List<Integer> serviceTimes = Helper.getServiceTimes(locationData);
        double Q = Helper.getBatteryCapacity(otherData);
        double C = Helper.getLoadCapacity(otherData);
        double h = Helper.getBatteryConsumptionRate(otherData);
        double g = Helper.getRechargingRate(otherData);
        double v = Helper.getVelocity(otherData);
        double[][] distance = Helper.getDistanceMatrix(locationData);
        double[][] travelTimes = Helper.getTravelTimeMatrix(distance, v);
        int nDummies = Helper.nStations(locationData);
        int n = locationData.size() - 2;
        double LB = 0.25;
        double UB = 0.85;
        int[][] isArcTraversed = Helper.getArcTraversalMatrix(file, n);

        // creating an environment
        GRBEnv env = new GRBEnv();
        env.start();
        // creating an empty model
        GRBModel model = new GRBModel(env);
        // setting the runtime limit
        double timeLimit = 7200;
        model.set(GRB.DoubleParam.TimeLimit, timeLimit);

        // creating the decision variables
        GRBVar[] arrivalTime = new GRBVar[n + 2];
        GRBVar[] cargoUponArrival = new GRBVar[n + 2];
        GRBVar[] batteryUponArrival = new GRBVar[n + 2];
        GRBVar[] batteryUponDeparture = new GRBVar[nDummies + 1];
        GRBVar[] chargeBelowLB = new GRBVar[n + 1];
        GRBVar[] chargeAboveUB = new GRBVar[n + 1];
        GRBVar[] chargesFromDepot = new GRBVar[n + 1];
        GRBVar[] chargesToDepot = new GRBVar[n + 1];

        for (int i = 0; i <= n + 1; i++) {
            arrivalTime[i] = model.addVar(timeWindows.get(i)[0], timeWindows.get(i)[1], 0.0, GRB.CONTINUOUS,
                    "tau," + i);
            cargoUponArrival[i] = model.addVar(0, C, 0.0, GRB.CONTINUOUS,
                    "u," + i);
            batteryUponArrival[i] = model.addVar(0, Q, 0.0, GRB.CONTINUOUS,
                    "y," + i);
            if (i <= nDummies) {
                batteryUponDeparture[i] = model.addVar(0, Q, 0.0, GRB.CONTINUOUS,
                        "Y," + i);
            }
        }

        for (int i = 1; i <= n; i++) {
            chargesFromDepot[i] = model.addVar(0, Q*(1 - UB), 0.0, GRB.CONTINUOUS,
                    "zH," + 0 + "," + i);
            chargesToDepot[i] = model.addVar(0, Q*LB, 0.0, GRB.CONTINUOUS,
                    "zL," + i + "," + (n + 1));
        }

        for (int i = 1; i <= nDummies; i++) {
            chargeBelowLB[i] = model.addVar(0, Q*LB, 0.0, GRB.CONTINUOUS,
                    "zL," + i);
            chargeAboveUB[i] = model.addVar(0, Q*(1 - UB), 0.0, GRB.CONTINUOUS,
                    "zH," + i);
        }

        // creating the constraints
        for (int j = 1; j <= n + 1; j++) {
            for (int i = 0; i <= n; i++) {
                if (i == j) {
                    continue;
                }
                GRBLinExpr common = new GRBLinExpr();
                common.addTerm(1, arrivalTime[i]);
                common.addConstant(travelTimes[i][j] * isArcTraversed[i][j]);
                common.addConstant(-timeWindows.get(0)[1]);
                common.addConstant(timeWindows.get(0)[1] * isArcTraversed[i][j]);
                if (i >= 1 && i <= nDummies) {
                    GRBLinExpr station = new GRBLinExpr();
                    station.add(common);
                    station.addTerm(g, batteryUponDeparture[i]);
                    station.addTerm(-g, batteryUponArrival[i]);
                    station.addConstant(-g * Q);
                    station.addConstant(g * Q * isArcTraversed[i][j]);
                    model.addConstr(station, GRB.LESS_EQUAL, arrivalTime[j],
                            "time feasibility(" + i + "," + j + ")");
                } else {
                    GRBLinExpr customer0 = new GRBLinExpr();
                    customer0.add(common);
                    customer0.addConstant(serviceTimes.get(i) * isArcTraversed[i][j]);
                    model.addConstr(customer0, GRB.LESS_EQUAL, arrivalTime[j],
                            "time feasibility(" + i + "," + j + ")");
                }
            }
        }

        for (int j = 1; j <= n + 1; j++) {
            for (int i = 0; i <= n; i++) {
                if (i == j) {
                    continue;
                }
                GRBLinExpr common = new GRBLinExpr();
                common.addConstant(-h * distance[i][j] * isArcTraversed[i][j]);
                common.addConstant(Q);
                common.addConstant(-Q * isArcTraversed[i][j]);
                if (i <= nDummies) {
                    GRBLinExpr station0 = new GRBLinExpr();
                    station0.add(common);
                    station0.addTerm(1, batteryUponDeparture[i]);
                    model.addConstr(station0, GRB.GREATER_EQUAL, batteryUponArrival[j],
                            "battery consistency(" + i + "," + j + ")");
                } else {
                    GRBLinExpr customer = new GRBLinExpr();
                    customer.add(common);
                    customer.addTerm(1, batteryUponArrival[i]);
                    model.addConstr(customer, GRB.GREATER_EQUAL, batteryUponArrival[j],
                            "battery consistency(" + i + "," + j + ")");
                }
            }
        }

        for (int i = 0; i <= nDummies; i++) {
            model.addConstr(batteryUponArrival[i], GRB.LESS_EQUAL, batteryUponDeparture[i],
                    "battery after recharge(" + i + ")");
        }

        for (int i = 1; i <= n; i++) {
            GRBLinExpr fromDepot1 = new GRBLinExpr();
            fromDepot1.addTerm(1, batteryUponArrival[i]);
            fromDepot1.addConstant(distance[0][i] - UB*Q - Q);
            fromDepot1.addConstant(Q * isArcTraversed[0][i]);
            model.addConstr(chargesFromDepot[i], GRB.GREATER_EQUAL, fromDepot1,
                    "1:charge above UB before visiting " + i);
            GRBLinExpr fromDepot2 = new GRBLinExpr();
            fromDepot2.addTerm(1, batteryUponArrival[i]);
            fromDepot2.addConstant(distance[0][i] - UB*Q + Q);
            fromDepot2.addConstant(-Q * isArcTraversed[0][i]);
            model.addConstr(chargesFromDepot[i], GRB.LESS_EQUAL, fromDepot2,
                    "2:charge above UB before visiting " + i);
            GRBLinExpr toDepot1 = new GRBLinExpr();
            toDepot1.addConstant(LB*Q + distance[i][n+1] - Q);
            if (i <= nDummies) {
                toDepot1.addTerm(-1, batteryUponDeparture[i]);
            } else {
                toDepot1.addTerm(-1, batteryUponArrival[i]);
            }
            toDepot1.addConstant(Q * isArcTraversed[i][n + 1]);
            model.addConstr(chargesToDepot[i], GRB.GREATER_EQUAL, toDepot1,
                    "1: charge below LB after visiting " + i);
            GRBLinExpr toDepot2 = new GRBLinExpr();
            toDepot2.addConstant(LB*Q + distance[i][n+1] + Q);
            if (i <= nDummies) {
                toDepot1.addTerm(-1, batteryUponDeparture[i]);
            } else {
                toDepot1.addTerm(-1, batteryUponArrival[i]);
            }
            toDepot2.addConstant(-Q * isArcTraversed[i][n + 1]);
            model.addConstr(chargesToDepot[i], GRB.LESS_EQUAL, toDepot2,
                    "1: charge below LB after visiting " + i);
        }

        for (int i = 1; i <= nDummies; i++) {
            GRBLinExpr rhsL = new GRBLinExpr();
            rhsL.addConstant(LB*Q);
            rhsL.addTerm(-1, batteryUponArrival[i]);
            model.addConstr(chargeBelowLB[i], GRB.GREATER_EQUAL, rhsL,
                    "charge below LB " + i);
            GRBLinExpr rhsH = new GRBLinExpr();
            rhsH.addTerm(1, batteryUponDeparture[i]);
            rhsH.addConstant(-(UB * Q));
            model.addConstr(chargeAboveUB[i], GRB.GREATER_EQUAL, rhsH,
                    "charge above UB " + i);
        }

        // creating the objective
        GRBLinExpr objective = new GRBLinExpr();

        for (int i = 1; i <= nDummies; i++) {
            objective.addTerm(WL, chargeBelowLB[i]);
            objective.addTerm(WH, chargeAboveUB[i]);
        }

        for (int i = 1; i <= n; i++) {
            objective.addTerm(WL, chargesToDepot[i]);
            objective.addTerm(WH, chargesFromDepot[i]);
        }

        model.setObjective(objective, GRB.MINIMIZE);
        model.optimize();
        long endTime = System.currentTimeMillis();
        long elapsedTime = (endTime - startTime);

        // print and save the results (if feasible solution found)
        int status = model.get(GRB.IntAttr.Status);
        if (status == GRB.Status.OPTIMAL || status == GRB.Status.TIME_LIMIT) {
            System.out.println("Objective = " + model.get(GRB.DoubleAttr.ObjVal));
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(file + "_" + WH + ".csv"))) {
                writer.write("objective," + model.get(GRB.DoubleAttr.ObjVal) + "\n");
                writer.write("runtime (milliseconds)," + elapsedTime + "\n");

                for (GRBVar var : model.getVars()) {
                    if (var.get(GRB.DoubleAttr.X) != 0) {
                        System.out.println(var.get(GRB.StringAttr.VarName) + ": " + var.get(GRB.DoubleAttr.X));
                        writer.write(var.get(GRB.StringAttr.VarName) + "," + var.get(GRB.DoubleAttr.X));
                        writer.newLine();
                    }
                }

                writer.flush();
            }
            catch (IOException e) {
                System.err.println("Error writing to file: " + e.getMessage());
            }
        } else {
            System.out.println("No optimal solution found");
        }

        model.dispose();
        env.dispose();
    }
}
