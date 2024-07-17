/**
 * @author 621819es
 * @author 611700bz
 *
 * Helper methods for formatting parameters
 */

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Helper {

    /**
     * reads a csv file into a two_layer list
     * @param path: the path to the csv file
     * @return a list, where each list inside is a separate row
     * and each string in a that list is a separate value (in the column order)
     */
    public static List<List<String>> readFile(String path) {
        String delimiter = ",";
        String line;
        List<List<String>> lines = new ArrayList();
        try (BufferedReader br = new BufferedReader(new FileReader(path))) {
            while((line = br.readLine()) != null){
                List<String> values = Arrays.asList(line.split(delimiter));
                lines.add(values);
            }
        } catch (FileNotFoundException e){
            System.out.println("File could not be found.");
        } catch (IOException e) {
            System.out.println("An error occurred while reading the file.");
            e.printStackTrace();
        }

        return lines;
    }

    /**
     * returns the number of stations in the instance
     * @param lines: instance data as the output of readFile()
     * @return the number of stations as int
     */
    public static int nStations(List<List<String>> lines) {
        int count = 0;

        for (int i = 1; i < lines.size(); i++) {
            if (lines.get(i).get(1).equals("f")) {
                count += 1;
            }
        }
        return count;
    }

    /**
     * expands the output from readFile() by copying each list representing a station k times
     * k = nStations (e.g. if instance had 3 stations, each station is replaced by 3 dummies, so 9 station dummies)
     * @param path: he path to the csv file containing the locations sata
     * @return expanded version of the data that includes dummies for the stations
     */
    public static List<List<String>> expandDummies(String path) {
        List<List<String>> lines = readFile(path);
        List<List<String>> data = new ArrayList<>();
        int nStations = nStations(lines);
        // depot as location 0
        data.add(lines.get(1));

        // stations added multiple times as dummies
        for (int i = 2; i < nStations + 2; i++) {
            for (int j = 0; j < nStations; j++) {
                data.add(lines.get(i));
            }
        }

        // customers
        for (int i = nStations + 2; i < lines.size(); i++) {
            data.add(lines.get(i));
        }

        // depot as location N+1
        data.add(lines.get(1));

        return data;
    }

    /**
     * returns coordinates of all locations
     * @param data: instance data as the output of expandDummies()
     * @return all coordinates as a list of arrays,
     * where the first element of an array is x coordinate and the second is the y coordinate
     */
    public static List<int[]> getCoordinates(List<List<String>> data) {
        List<int[]> coordinates = new ArrayList<>();
        for (int i = 0; i < data.size(); i++) {
            List<String> line = data.get(i);
            int x = Integer.parseInt(line.get(2));
            int y = Integer.parseInt(line.get(3));
            int[] coordinate = new int[] {x, y};
            coordinates.add(coordinate);
        }
        return coordinates;
    }

    /**
     * returns demands of all locations
     * @param data: instance data as the output of expandDummies()
     * @return all demands as a list of integers
     */
    public static List<Integer> getDemands(List<List<String>> data) {
        List<Integer> demands = new ArrayList<>();
        for (int i = 0; i < data.size(); i++) {
            int demand = Integer.parseInt(data.get(i).get(4));
            demands.add(demand);
        }
        return demands;
    }

    /**
     * returns time windows of all locations
     * @param data: instance data as the output of expandDummies()
     * @return all time windows as a list of arrays,
     * where first element in the array is ready time and the second is the due time
     */
    public static List<int[]> getTimeWindows(List<List<String>> data) {
        List<int[]> timeWindows = new ArrayList<>();
        for (int i = 0; i < data.size(); i++) {
            List<String> line = data.get(i);
            int ready = Integer.parseInt(line.get(5));
            int due = Integer.parseInt(line.get(6));
            int[] window = new int[] {ready, due};
            timeWindows.add(window);
        }
        return timeWindows;
    }

    /**
     * returns service timea of all locations
     * @param data: instance data as the output of expandDummies()
     * @return all service times as a list of integers
     */
    public static List<Integer> getServiceTimes(List<List<String>> data) {
        List<Integer> serviceTimes = new ArrayList<>();
        for (int i = 0; i < data.size(); i++) {
            int serviceTime = Integer.parseInt(data.get(i).get(7));
            serviceTimes.add(serviceTime);
        }
        return serviceTimes;
    }

    /**
     * returns the battery capacity of the vehicle
     * @param data: instance data as the output of expandDummies()
     * @return battery capacity as a double
     */
    public static double getBatteryCapacity(List<List<String>> data) {
        return Double.parseDouble(data.get(1).get(0));
    }

    /**
     * returns the load capacity of the vehicle
     * @param data: instance data as the output of expandDummies()
     * @return load capacity as a double
     */
    public static double getLoadCapacity(List<List<String>> data) {
        return Double.parseDouble(data.get(1).get(1));
    }

    /**
     * returns the battery consumption rate of the vehicle
     * @param data: instance data as the output of expandDummies()
     * @return battery consumption rate as a double
     */
    public static double getBatteryConsumptionRate(List<List<String>> data) {
        return Double.parseDouble(data.get(1).get(2));
    }

    /**
     * returns the battery recharging rate of the vehicle
     * @ data: instance data as the output of expandDummies()
     * @return battery recharging rate as a double
     */
    public static double getRechargingRate(List<List<String>> data) {
        return Double.parseDouble(data.get(1).get(3));
    }

    /**
     * returns the velocity of the vehicle
     * @param data: instance data as the output of expandDummies()
     * @return velocity as a double
     */
    public static double getVelocity(List<List<String>> data) {
        return Double.parseDouble(data.get(1).get(4));
    }


    /**
     * Calculates the Euclidean distance between two points i and j
     * @param i: location i coordinates (x, y)
     * @param j: location j coordinates (x, y)
     * @return the distance between i and j
     */
    public static double distance(int[] i, int[] j) {

        return Math.sqrt(Math.pow((i[0] - j[0]), 2) + Math.pow((i[1] - j[1]), 2));
    }

    /**
     * constructs a distance matrix
     * @param data: instance data as the output of expandDummies()
     * @return a 2D array, where the i,j th element is the distance between locations indexed i and j
     */
    public static double[][] getDistanceMatrix(List<List<String>> data) {
        List<int[]> coordinates = getCoordinates(data);
        int N = coordinates.size();
        double[][] distances = new double[N][N];
        int[] iLoc;
        int[] jLoc;

        for (int i = 0; i < N; i++) {
            iLoc = coordinates.get(i);
            for (int j = 0; j < N; j++) {
                jLoc = coordinates.get(j);
                double dist = distance(iLoc, jLoc);
                distances[i][j] = dist;
            }
        }

        return distances;
    }

    /**
     * converts the distance matrix into a travel time matrix
     * @param distances: the distance matrix as returned by getDistanceMatrix()
     * @param velocity: the velocity of the vehicle
     * @return a 2D array, where the i,j th element is the travel time between locations indexed i and j
     */
    public static double[][] getTravelTimeMatrix(double[][] distances, double velocity) {
        int N = distances.length;
        double[][] travelTimes = new double[N][N];

        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                travelTimes[i][j] = distances[i][j] / velocity;
            }
        }
        return travelTimes;
    }

    /**
     * from the file of decision variables, constructs a binary arc traversal matrix,
     * where 1 in position i, j indicates that an arc between locations i and j is traversed
     * @param file: the name of the instance
     * @param n: the number of locations (dummies included)
     * @return a binary arc traversal matrix
     */
    public static int[][] getArcTraversalMatrix(String file, int n) {
        String path = "./decision_variables/" + file + ".csv";
        String delimiter = ",";
        String line;
        int[][] matrix = new int[n + 2][n + 2];
        try (BufferedReader br = new BufferedReader(new FileReader(path))) {
            while((line = br.readLine()) != null){
                List<String> values = Arrays.asList(line.split(delimiter));
                if (values.get(0).equals("x")) {
                    if (Math.abs(Double.parseDouble(values.get(3))) > 1e-5) {
                        int i = Integer.parseInt(values.get(1));
                        int j = Integer.parseInt(values.get(2));
                        matrix[i][j] = 1;
                    }
                }
            }
        } catch (FileNotFoundException e){
            System.out.println("File could not be found.");
        } catch (IOException e) {
            System.out.println("An error occurred while reading the file.");
            e.printStackTrace();
        }

        return matrix;
    }
}
