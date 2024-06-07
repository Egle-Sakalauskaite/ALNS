/**
 * @author 621819es
 * Main method for MILP
 */


import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import com.gurobi.gurobi.*;


public class Main {
    public static void main(String[] args) throws GRBException, IOException {
        List<String> files = new ArrayList<>();
//        files.add("c101C5");
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
//        files.add("rc204C5");
//        files.add("rc208C5");
//        files.add("rc102C10");
//        files.add("rc108C10");
//        files.add("rc201C10");
//        files.add("rc205C10");
        files.add("rc103C15");
        files.add("rc108C15");
        files.add("rc202C15");
        files.add("rc204C15");
        for (String file: files) {
            solve(file);
        }
    }

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

        // results
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
}
