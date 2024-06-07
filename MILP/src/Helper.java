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
import java.util.HashMap;
import java.util.Map;

public class Helper {

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

    public static int nStations(List<List<String>> lines) {
        int count = 0;

        for (int i = 1; i < lines.size(); i++) {
            if (lines.get(i).get(1).equals("f")) {
                count += 1;
            }
        }
        return count;
    }

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

    public static List<Integer> getDemands(List<List<String>> data) {
        List<Integer> demands = new ArrayList<>();
        for (int i = 0; i < data.size(); i++) {
            int demand = Integer.parseInt(data.get(i).get(4));
            demands.add(demand);
        }
        return demands;
    }

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

    public static List<Integer> getServiceTimes(List<List<String>> data) {
        List<Integer> serviceTimes = new ArrayList<>();
        for (int i = 0; i < data.size(); i++) {
            int serviceTime = Integer.parseInt(data.get(i).get(7));
            serviceTimes.add(serviceTime);
        }
        return serviceTimes;
    }

    public static double getBatteryCapacity(List<List<String>> data) {
        return Double.parseDouble(data.get(1).get(0));
    }

    public static double getLoadCapacity(List<List<String>> data) {
        return Double.parseDouble(data.get(1).get(1));
    }

    public static double getBatteryConsumptionRate(List<List<String>> data) {
        return Double.parseDouble(data.get(1).get(2));
    }

    public static double getRechargingRate(List<List<String>> data) {
        return Double.parseDouble(data.get(1).get(3));
    }

    public static double getVelocity(List<List<String>> data) {
        return Double.parseDouble(data.get(1).get(4));
    }


    /**
     * Calculates the distance between two points i and j
     * @param i location i coordinates (x, y)
     * @param j location j coordinates (x, y)
     * @return the distance between i and j
     */
    public static double distance(int[] i, int[] j) {
        return Math.sqrt(Math.pow((i[0] - j[0]), 2) + Math.pow((i[1] - j[1]), 2));
    }

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

    public static Map<Integer, Integer> indexConverter(List<List<String>> data) {
        Map<Integer, Integer> dict = new HashMap<>();
        int nDummies = nStations(data);
        int nStations = (int) Math.sqrt(nDummies);
        int N = data.size();
        int shift = nDummies - nStations;

        dict.put(0, 0);

        for (int i = 1; i <= nDummies ; i++) {
            dict.put(i, (i + 2) / nStations);
        }

        for (int i = nDummies + 1; i < N - 1; i++) {
            dict.put(i, i - shift);
        }

        dict.put(N - 1, 0);
        return dict;
    }

    /**
     * Prints an array for inspection.
     * @param array To be printed
     */
    public static void print2DArray(double[][] array) {
        for (double[] ints : array) {
            for (double anInt : ints) {
                System.out.print(anInt + " ");
            }
            System.out.println();
        }
    }
}
