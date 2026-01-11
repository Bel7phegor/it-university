import java.io.*;
import java.net.*;
import java.util.Scanner;

public class client {
    public static void main(String[] args) {
        final String SERVER_IP = "localhost";
        final int PORT = 12345;
        
        try (Socket socket = new Socket(SERVER_IP, PORT);
             PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
             BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             Scanner scanner = new Scanner(System.in)) {
            
            System.out.println("Connected to server");
            
            // Get input from user
            System.out.print("Nhập số thứ nhất: ");
            double a = scanner.nextDouble();
            
            System.out.print("Nhập số thứ hai: ");
            double b = scanner.nextDouble();
            
            System.out.print("Nhập phép toán (+, -, *, /): ");
            String operator = scanner.next();
            
            // Send data to server
            out.println(a);
            out.println(b);
            out.println(operator);
            
            // Get and display result
            String response = in.readLine();
            System.out.println("Kết quả: " + response);
            
        } catch (UnknownHostException e) {
            System.out.println("Server not found: " + e.getMessage());
        } catch (IOException e) {
            System.out.println("I/O error: " + e.getMessage());
        }
    }
}