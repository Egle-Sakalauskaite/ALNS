///**
// * @author 621819es
// * @author 611700bz
// *
// * Main method for Assignment 1. Defines gurobi models and solves them.
// */
//import java.util.Arrays;
//import java.util.List;
//import com.gurobi.gurobi.*;
//
//public class Main1 {
//    public static void main(String[] args) throws GRBException {
//        String inputPath = "./Metropolica_coordinates.csv";
//        exercise3(inputPath);
////        exercise3Alternative(inputPath);
//        int[] capacities = new int[] {25, 20, 15, 10, 5};
//        for (Integer capacity : capacities) {
//            System.out.println("================   For capacity " + capacity + "   ================ ");
//            exercise6(inputPath, capacity);
//        }
//        for (double i = 0; i <= 1.05; i+=0.05) {
//            System.out.println("======================    alpha = " + i + "    ===========================");
//            exercise8(inputPath, i);
//        }
//
//        for (double i = 0; i <= 1.05; i+=0.05) {
//            System.out.println("======================    beta = " + i + "    ===========================");
//            bonusExercise(inputPath, i);
//        }
//
//    }
//
//    /**
//     * Solves the model in exercise 3. There are no extensions.
//     *
//     * @param inputPath The path name of the input file containing coordinates of locations.
//     * @throws GRBException Whenever an error occurs with the Gurobi solver.
//     */
//    public static void exercise3(String inputPath) throws GRBException {
//        int costNormal = 11;
//        int costAdvanced = 35;
//        int timeConstraint = 22;
//
//        // creating an environment
//        GRBEnv env = new GRBEnv();
//        env.start();
//        // creating an empty model
//        GRBModel model = new GRBModel(env);
//        // creating the parameters
//        List<double[]> locationCoordinates = Helper.getCoordinates(inputPath);
//        int nLocations = locationCoordinates.size();
//        int[][] normalICanCoverJ = Helper.getParameterMatrix(false, timeConstraint);
//        int[][] advancedICanCoverJ = Helper.getParameterMatrix(true, timeConstraint);
//        // creating the decision variables
//        GRBVar[] normalOpen = new GRBVar[nLocations];
//        GRBVar[] advancedOpen = new GRBVar[nLocations];
//        for (int i = 0; i < nLocations ; i++) {
//            normalOpen[i] = model.addVar(0, 1, 0.0, GRB.BINARY,
//                    "e(" + i+ ")");
//            advancedOpen[i] = model.addVar(0, 1, 0.0, GRB.BINARY,
//                    "a(" + i + ")");
//        }
//        // creating the constraints
//        for (int j = 0; j < nLocations; j++) {
//            GRBLinExpr sumOverI = new GRBLinExpr();
//            for (int i = 0; i < nLocations; i++) {
//                sumOverI.addTerm(normalICanCoverJ[i][j], normalOpen[i]);
//                sumOverI.addTerm(advancedICanCoverJ[i][j], advancedOpen[i]);
//            }
//            model.addConstr(sumOverI, GRB.GREATER_EQUAL, 1, "coverage(" + j + ")");
//        }
//        // creating the objective
//        GRBLinExpr objective = new GRBLinExpr();
//        for (int i = 0; i < nLocations; i++) {
//            objective.addTerm(costNormal, normalOpen[i]);
//            objective.addTerm(costAdvanced, advancedOpen[i]);
//        }
//
//        model.setObjective(objective, GRB.MINIMIZE);
//        model.optimize();
//
//        // results
//        if (model.get(GRB.IntAttr.Status) == GRB.Status.OPTIMAL) {
//            System.out.println("Found optimal solution!");
//            System.out.println("Objective = " + model.get(GRB.DoubleAttr.ObjVal));
//            System.out.println("Normal evacuation centers built at: ");
//            for (int i = 0; i < nLocations; i++) {
//                if (normalOpen[i].get(GRB.DoubleAttr.X) >= 0.90) {
//                    System.out.println("Location " + i + " at " + Arrays.toString(locationCoordinates.get(i)));
//                }
//            }
//            System.out.println("Advanced evacuation centers built at: ");
//            for (int i = 0; i < nLocations; i++) {
//                if (advancedOpen[i].get(GRB.DoubleAttr.X) >= 0.90) {
//                    System.out.println("Location " + i + " at " + Arrays.toString(locationCoordinates.get(i)));
//                }
//            }
//        } else {
//            System.out.println(" No optimal solution found ") ;
//            model.write("Model.lp") ;
//        }
//        model.dispose();
//        env.dispose();
//    }
//
//    /**
//     * Solves the model in exercise 3. This is an alternative model with more variables and constraints.
//     *
//     * @param inputPath The path name of the input file containing coordinates of locations.
//     * @throws GRBException Whenever an error occurs with the Gurobi solver.
//     */
//    public static void exercise3Alternative(String inputPath) throws GRBException {
//        int costNormal = 11;
//        int costAdvanced = 35;
//        int timeConstraint = 22;
//
//        GRBEnv env = new GRBEnv();
//        env.start();
//        GRBModel model = new GRBModel(env);
//        List<double[]> locationCoordinates = Helper.getCoordinates(inputPath);
//        int nLocations = locationCoordinates.size();
//        int[][] normalICanCoverJ = Helper.getParameterMatrix(false, timeConstraint);
//        int[][] advancedICanCoverJ = Helper.getParameterMatrix(true, timeConstraint);
//        GRBVar[] normalOpen = new GRBVar[nLocations];
//        GRBVar[] advancedOpen = new GRBVar[nLocations];
//        GRBVar[][] normalICoversJ = new GRBVar[nLocations][nLocations];
//        GRBVar[][] advancedICoversJ = new GRBVar[nLocations][nLocations];
//        for (int i = 0; i < nLocations ; i++) {
//            normalOpen[i] = model.addVar(0 , 1 , 0.0 , GRB.BINARY ,
//                    "Normal center at location " + i);
//            advancedOpen[i] = model.addVar(0 , 1 , 0.0 , GRB.BINARY ,
//                    "Advanced center at location " + i);
//
//            for (int j = 0; j < nLocations; j++) {
//                normalICoversJ[i][j] = model.addVar(0 , 1 , 0.0 , GRB.BINARY ,
//                        "Normal center " + i + " covers location " + j);
//                advancedICoversJ[i][j] = model.addVar(0 , 1 , 0.0 , GRB.BINARY ,
//                        "Advanced center " + i + " covers location " + j);
//                model.addConstr(normalICoversJ[i][j], GRB.LESS_EQUAL, normalOpen[i], "");
//                model.addConstr(advancedICoversJ[i][j], GRB.LESS_EQUAL, advancedOpen[i], "");
//                model.addConstr(normalICoversJ[i][j], GRB.LESS_EQUAL, normalICanCoverJ[i][j], "");
//                model.addConstr(advancedICoversJ[i][j], GRB.LESS_EQUAL, advancedICanCoverJ[i][j], "");
//            }
//        }
//
//        for (int j = 0; j < nLocations; j++) {
//            GRBLinExpr sumOverI = new GRBLinExpr();
//            for (int i = 0; i < nLocations; i++) {
//                sumOverI.addTerm(1, normalICoversJ[i][j]);
//                sumOverI.addTerm(1, advancedICoversJ[i][j]);
//            }
//            model.addConstr(sumOverI, GRB.GREATER_EQUAL, 1, "Location " + j + " is covered");
//        }
//
//        GRBLinExpr objective = new GRBLinExpr();
//        for (int i = 0; i < nLocations; i++) {
//            objective.addTerm(costNormal, normalOpen[i]);
//            objective.addTerm(costAdvanced, advancedOpen[i]);
//        }
//
//        model.setObjective(objective, GRB.MINIMIZE);
//        model.optimize();
//
//        if (model.get(GRB.IntAttr.Status) == GRB.Status.OPTIMAL) {
//            System.out.println("Found optimal solution for alternative!");
//            System.out.println("Objective = " + model.get(GRB.DoubleAttr.ObjVal));
//            System.out.println("Normal evacuation centers built at: ");
//            for (int i = 0; i < nLocations; i++) {
//                if (normalOpen[i].get(GRB.DoubleAttr.X) >= 0.90) {
//                    System.out.println("Location " + i + " at " + Arrays.toString(locationCoordinates.get(i)));
//                }
//            }
//            System.out.println("Advanced evacuation centers built at: ");
//            for (int i = 0; i < nLocations; i++) {
//                if (advancedOpen[i].get(GRB.DoubleAttr.X) >= 0.90) {
//                    System.out.println("Location " + i + " at " + Arrays.toString(locationCoordinates.get(i)));
//                }
//            }
//        } else {
//            System.out.println(" No optimal solution found ") ;
//        }
//
//        model.dispose();
//        env.dispose();
//    }
//
//    /**
//     * Solves the model in exercise 6. The original model is extended with capacity constraints.
//     *
//     * @param inputPath The path name of the input file containing coordinates of locations.
//     * @throws GRBException Whenever an error occurs with the Gurobi solver.
//     */
//    public static void exercise6(String inputPath, int capacity) throws GRBException {
//        int costNormal = 11;
//        int costAdvanced = 35;
//        int timeConstraint = 22;
//
//        // create an environment
//        GRBEnv env = new GRBEnv();
//        env.start();
//        // create an empty model
//        GRBModel model = new GRBModel(env);
//        // create the parameters
//        List<double[]> locationCoordinates = Helper.getCoordinates(inputPath);
//        int nLocations = locationCoordinates.size();
//        int[][] normalICanCoverJ = Helper.getParameterMatrix(false, timeConstraint);
//        int[][] advancedICanCoverJ = Helper.getParameterMatrix(true, timeConstraint);
//        // create the decision variables
//        GRBVar[] normalOpen = new GRBVar[nLocations];
//        GRBVar[] advancedOpen = new GRBVar[nLocations];
//        GRBVar[][] normalICoversJ = new GRBVar[nLocations][nLocations];
//        GRBVar[][] advancedICoversJ = new GRBVar[nLocations][nLocations];
//        for (int i = 0; i < nLocations ; i++) {
//            normalOpen[i] = model.addVar(0 , 1 , 0.0 , GRB.BINARY ,
//                    "Normal center at location " + i);
//            advancedOpen[i] = model.addVar(0 , 1 , 0.0 , GRB.BINARY ,
//                    "Advanced center at location " + i);
//
//            for (int j = 0; j < nLocations; j++) {
//                normalICoversJ[i][j] = model.addVar(0 , 1 , 0.0 , GRB.BINARY ,
//                        "Normal center " + i + " covers location " + j);
//                advancedICoversJ[i][j] = model.addVar(0 , 1 , 0.0 , GRB.BINARY ,
//                        "Advanced center " + i + " covers location " + j);
//            }
//        }
//        // creating the constraints
//        for (int i = 0; i < nLocations; i++) {
//            for (int j = 0; j < nLocations; j++) {
//                model.addConstr(normalICoversJ[i][j], GRB.LESS_EQUAL, normalOpen[i], "");
//                model.addConstr(advancedICoversJ[i][j], GRB.LESS_EQUAL, advancedOpen[i], "");
//                model.addConstr(normalICoversJ[i][j], GRB.LESS_EQUAL, normalICanCoverJ[i][j], "");
//                model.addConstr(advancedICoversJ[i][j], GRB.LESS_EQUAL, advancedICanCoverJ[i][j], "");
//            }
//        }
//
//        for (int j = 0; j < nLocations; j++) {
//            GRBLinExpr sumOverI = new GRBLinExpr();
//            for (int i = 0; i < nLocations; i++) {
//                sumOverI.addTerm(1, normalICoversJ[i][j]);
//                sumOverI.addTerm(1, advancedICoversJ[i][j]);
//            }
//            model.addConstr(sumOverI, GRB.EQUAL, 1, "Location " + j + " is covered");
//        }
//
//        for (int i = 0; i < nLocations; i++) {
//            GRBLinExpr normalSumOverJ = new GRBLinExpr();
//            GRBLinExpr advancedSumOverJ = new GRBLinExpr();
//            for (int j = 0; j < nLocations; j++) {
//                normalSumOverJ.addTerm(1, normalICoversJ[i][j]);
//                advancedSumOverJ.addTerm(1, advancedICoversJ[i][j]);
//            }
//            model.addConstr(normalSumOverJ, GRB.LESS_EQUAL, capacity, "Capacity of evacuation center at " + i);
//            model.addConstr(advancedSumOverJ, GRB.LESS_EQUAL, capacity, "Capacity of advanced center at " + i);
//        }
//
//        // creating the objective
//        GRBLinExpr objective = new GRBLinExpr();
//        for (int i = 0; i < nLocations; i++) {
//            objective.addTerm(costNormal, normalOpen[i]);
//            objective.addTerm(costAdvanced, advancedOpen[i]);
//        }
//
//        model.setObjective(objective, GRB.MINIMIZE);
//        model.optimize();
//
//        // results
//        if (model.get(GRB.IntAttr.Status) == GRB.Status.OPTIMAL) {
//            System.out.println("Found optimal solution !");
//            System.out.println("Objective = " + model.get(GRB.DoubleAttr.ObjVal));
//            System.out.println("Normal evacuation centers built at: ");
//            for (int i = 0; i < nLocations; i++) {
//                if (normalOpen[i].get(GRB.DoubleAttr.X) >= 0.90) {
//                    String coordinates = Arrays.toString(locationCoordinates.get(i));
//                    int totalServed = 0;
//                    for (int j = 0; j < nLocations; j++) {
//                        totalServed += (int) normalICoversJ[i][j].get(GRB.DoubleAttr.X);
//                    }
//                    System.out.println("Location " + i + " at " + coordinates + "   Residencies served: " + totalServed);
//                }
//            }
//            System.out.println("Advanced evacuation centers built at: ");
//            for (int i = 0; i < nLocations; i++) {
//                if (advancedOpen[i].get(GRB.DoubleAttr.X) >= 0.90) {
//                    String coordinates = Arrays.toString(locationCoordinates.get(i));
//                    int totalServed = 0;
//                    for (int j = 0; j < nLocations; j++) {
//                        totalServed += (int) advancedICoversJ[i][j].get(GRB.DoubleAttr.X);
//                    }
//                    System.out.println("Location " + i + " at " + coordinates + "   Residencies served: " + totalServed);
//                }
//            }
//        } else {
//            System.out.println(" No optimal solution found ") ;
//        }
//
//        model.dispose();
//        env.dispose();
//    }
//
//    /**
//     * Solves the model in exercise 8. The original model is extended with relaxation on time constraints.
//     *
//     * @param inputPath The path name of the input file containing coordinates of locations.
//     * @throws GRBException Whenever an error occurs with the Gurobi solver.
//     */
//    public static void exercise8(String inputPath, double fraction) throws GRBException {
//        int costNormal = 11;
//        int costAdvanced = 35;
//        int timeConstraint = 22;
//        // create environment
//        GRBEnv env = new GRBEnv();
//        env.start();
//        // create empty model
//        GRBModel model = new GRBModel(env);
//        // create the parameters
//        List<double[]> locationCoordinates = Helper.getCoordinates(inputPath);
//        int nLocations = locationCoordinates.size();
//        int[][] normalICanCoverJ = Helper.getParameterMatrix(false, timeConstraint);
//        int[][] advancedICanCoverJ = Helper.getParameterMatrix(true, timeConstraint);
//        int[][] normalICanCoverJ2T = Helper.getParameterMatrix(false, timeConstraint * 2);
//        int[][] advancedICanCoverJ2T = Helper.getParameterMatrix(true, timeConstraint * 2);
//        // create the decision variables
//        GRBVar[] normalOpen = new GRBVar[nLocations];
//        GRBVar[] advancedOpen = new GRBVar[nLocations];
//        GRBVar[][] normalICoversJ = new GRBVar[nLocations][nLocations];
//        GRBVar[][] advancedICoversJ = new GRBVar[nLocations][nLocations];
//        GRBVar[][] normalICoversJ2T = new GRBVar[nLocations][nLocations];
//        GRBVar[][] advancedICoversJ2T = new GRBVar[nLocations][nLocations];
//        for (int i = 0; i < nLocations ; i++) {
//            normalOpen[i] = model.addVar(0 , 1 , 0.0 , GRB.BINARY ,
//                    "Normal center at location " + i);
//            advancedOpen[i] = model.addVar(0 , 1 , 0.0 , GRB.BINARY ,
//                    "Advanced center at location " + i);
//
//            for (int j = 0; j < nLocations; j++) {
//                normalICoversJ[i][j] = model.addVar(0 , 1 , 0.0 , GRB.BINARY ,
//                        "Normal center " + i + " covers location " + j);
//                advancedICoversJ[i][j] = model.addVar(0 , 1 , 0.0 , GRB.BINARY ,
//                        "Advanced center " + i + " covers location " + j);
//                normalICoversJ2T[i][j] = model.addVar(0, 1, 0.0, GRB.BINARY,
//                        "Normal center " + i + " covers location " + j + " at 2T");
//                advancedICoversJ2T[i][j] = model.addVar(0 , 1 , 0.0 , GRB.BINARY ,
//                        "Advanced center " + i + " covers location " + j + " at 2T");
//            }
//        }
//        // create the constraints
//        for (int i = 0; i < nLocations; i++) {
//            for (int j = 0; j < nLocations; j++) {
//                model.addConstr(normalICoversJ[i][j], GRB.LESS_EQUAL, normalICanCoverJ[i][j], "");
//                model.addConstr(advancedICoversJ[i][j], GRB.LESS_EQUAL, advancedICanCoverJ[i][j], "");
//                model.addConstr(normalICoversJ2T[i][j], GRB.LESS_EQUAL, normalICanCoverJ2T[i][j], "");
//                model.addConstr(advancedICoversJ2T[i][j], GRB.LESS_EQUAL, advancedICanCoverJ2T[i][j], "");
//
//                GRBLinExpr normal = new GRBLinExpr();
//                normal.addTerm(1, normalICoversJ[i][j]);
//                normal.addTerm(1, normalICoversJ2T[i][j]);
//                GRBLinExpr advanced = new GRBLinExpr();
//                advanced.addTerm(1, advancedICoversJ[i][j]);
//                advanced.addTerm(1, advancedICoversJ2T[i][j]);
//                model.addConstr(normal, GRB.LESS_EQUAL, normalOpen[i], "");
//                model.addConstr(advanced, GRB.LESS_EQUAL, advancedOpen[i], "");
//            }
//        }
//
//        for (int j = 0; j < nLocations; j++) {
//            GRBLinExpr sumOverI = new GRBLinExpr();
//            for (int i = 0; i < nLocations; i++) {
//                sumOverI.addTerm(1, normalICoversJ[i][j]);
//                sumOverI.addTerm(1, advancedICoversJ[i][j]);
//                sumOverI.addTerm(1, normalICoversJ2T[i][j]);
//                sumOverI.addTerm(1, advancedICoversJ2T[i][j]);
//            }
//            model.addConstr(sumOverI, GRB.EQUAL, 1, "Location " + j + " is covered");
//        }
//
//        GRBLinExpr sumIJ = new GRBLinExpr();
//        for (int i = 0; i < nLocations; i++) {
//            for (int j = 0; j < nLocations; j++) {
//                sumIJ.addTerm(1, normalICoversJ[i][j]);
//                sumIJ.addTerm(1, advancedICoversJ[i][j]);
//            }
//        }
//
//        model.addConstr(sumIJ, GRB.GREATER_EQUAL, (1 - fraction) * nLocations, "");
//
//        // create the objective function
//        GRBLinExpr objective = new GRBLinExpr();
//        for (int i = 0; i < nLocations; i++) {
//            objective.addTerm(costNormal, normalOpen[i]);
//            objective.addTerm(costAdvanced, advancedOpen[i]);
//        }
//
//        model.setObjective(objective, GRB.MINIMIZE);
//        model.optimize();
//
//        // results
//        if (model.get(GRB.IntAttr.Status) == GRB.Status.OPTIMAL) {
//            System.out.println("Found optimal solution for alternative!");
//            System.out.println("Objective = " + model.get(GRB.DoubleAttr.ObjVal));
//            System.out.println("Normal evacuation centers built at: ");
//            for (int i = 0; i < nLocations; i++) {
//                if (normalOpen[i].get(GRB.DoubleAttr.X) >= 0.90) {
//                    System.out.println("Location " + i + " at " + Arrays.toString(locationCoordinates.get(i)));
//                }
//            }
//            System.out.println("Advanced evacuation centers built at: ");
//            for (int i = 0; i < nLocations; i++) {
//                if (advancedOpen[i].get(GRB.DoubleAttr.X) >= 0.90) {
//                    System.out.println("Location " + i + " at " + Arrays.toString(locationCoordinates.get(i)));
//                }
//            }
//        } else {
//            System.out.println(" No optimal solution found ") ;
//        }
//
//        model.dispose();
//        env.dispose();
//    }
//
//    /**
//     * Solves the model in the bonus exercise. The original model is extended with a probability distribution
//     * for the travel time of residents.
//     *
//     * @param inputPath The path name of the input file containing coordinates of locations.
//     * @throws GRBException Whenever an error occurs with the Gurobi solver.
//     */
//    public static void bonusExercise(String inputPath, double beta) throws GRBException {
//        int costNormal = 11;
//        int costAdvanced = 35;
//        int timeConstraint = 22;
//
//        // creating an environment
//        GRBEnv env = new GRBEnv();
//        env.start();
//        // creating an empty model
//        GRBModel model = new GRBModel(env);
//        // creating the parameters
//        List<double[]> locationCoordinates = Helper.getCoordinates(inputPath);
//        int nLocations = locationCoordinates.size();
//        int[][] normalICanCoverJ2T = Helper.getParameterMatrix(false, timeConstraint * 2);
//        int[][] advancedICanCoverJ2T = Helper.getParameterMatrix(true, timeConstraint * 2);
//        int[][] normalICanCoverJBeta = Helper.getParameterMatrix(false, timeConstraint, beta);
//        int[][] advancedICanCoverJBeta = Helper.getParameterMatrix(true, timeConstraint, beta);
//        // creating the decision variables
//        GRBVar[] normalOpen = new GRBVar[nLocations];
//        GRBVar[] advancedOpen = new GRBVar[nLocations];
//        for (int i = 0; i < nLocations ; i++) {
//            normalOpen[i] = model.addVar(0, 1, 0.0, GRB.BINARY,
//                    "e(" + i+ ")");
//            advancedOpen[i] = model.addVar(0, 1, 0.0, GRB.BINARY,
//                    "a(" + i + ")");
//        }
//        // creating the constraints
//        for (int j = 0; j < nLocations; j++) {
//            GRBLinExpr sumOverI2T = new GRBLinExpr();
//            GRBLinExpr sumOverIBeta = new GRBLinExpr();
//            for (int i = 0; i < nLocations; i++) {
//                sumOverI2T.addTerm(normalICanCoverJ2T[i][j], normalOpen[i]);
//                sumOverI2T.addTerm(advancedICanCoverJ2T[i][j], advancedOpen[i]);
//
//                sumOverIBeta.addTerm(normalICanCoverJBeta[i][j], normalOpen[i]);
//                sumOverIBeta.addTerm(advancedICanCoverJBeta[i][j], advancedOpen[i]);
//            }
//            model.addConstr(sumOverI2T, GRB.GREATER_EQUAL, 1, "coverage2T(" + j + ")");
//            model.addConstr(sumOverIBeta, GRB.GREATER_EQUAL, 1, "coverageBeta(" + j + ")");
//        }
//        // creating the objective
//        GRBLinExpr objective = new GRBLinExpr();
//        for (int i = 0; i < nLocations; i++) {
//            objective.addTerm(costNormal, normalOpen[i]);
//            objective.addTerm(costAdvanced, advancedOpen[i]);
//        }
//
//        model.setObjective(objective, GRB.MINIMIZE);
//        model.optimize();
//
//        // results
//        if (model.get(GRB.IntAttr.Status) == GRB.Status.OPTIMAL) {
//            System.out.println("Found optimal solution!");
//            System.out.println("Objective = " + model.get(GRB.DoubleAttr.ObjVal));
//            System.out.println("Normal evacuation centers built at: ");
//            for (int i = 0; i < nLocations; i++) {
//                if (normalOpen[i].get(GRB.DoubleAttr.X) >= 0.90) {
//                    System.out.println("Location " + i + " at " + Arrays.toString(locationCoordinates.get(i)));
//                }
//            }
//            System.out.println("Advanced evacuation centers built at: ");
//            for (int i = 0; i < nLocations; i++) {
//                if (advancedOpen[i].get(GRB.DoubleAttr.X) >= 0.90) {
//                    System.out.println("Location " + i + " at " + Arrays.toString(locationCoordinates.get(i)));
//                }
//            }
//        } else {
//            System.out.println(" No optimal solution found ") ;
//            model.write("Model.lp") ;
//        }
//        model.dispose();
//        env.dispose();
//    }
//}
